#!/usr/bin/env python3
"""Observe every configured upstream file; publish only approved ad rules."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fusion import normalize_host, safe_ad_domain, verify_source_url
from validate_personal_rules import PROFILE, sections, validate

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "# BEGIN DAILY SAFE AD DOMAINS"
END = "# END DAILY SAFE AD DOMAINS"
REWRITE_BEGIN = "# BEGIN REVIEWED UPSTREAM AD INTERFACES"
REWRITE_END = "# END REVIEWED UPSTREAM AD INTERFACES"
HISTORY_MARKER = "<!-- EFFECTIVE_UPDATES_START -->"
BT = chr(96)
STATUS_LABELS = {
    "no_upstream_changes": "上游无变化",
    "observed_no_publish": "已检测变化，无需发布规则",
    "auto_updated": "已自动更新",
    "review_required": "有变化待审核",
    "sync_failed": "同步失败",
}
SIMPLE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX)\s*,\s*([^,\s]+)\s*,\s*REJECT(?:\s*,(.*))?$", re.I)
FLAGS = {"extended-matching", "pre-matching"}
LIMIT_BYTES = 1024 * 1024


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical(line):
    match = SIMPLE.fullmatch(line.strip())
    if match:
        flags = sorted(s.strip() for s in (match[3] or "").split(",") if s.strip())
        return ",".join([match[1].upper(), match[2].lower(), "REJECT", *flags])
    return line.strip()


def inventory(text, kind="module"):
    if kind == "script":
        return []
    found, section = {}, "Other"
    aliases = {"rewrite_local": "URL Rewrite", "mitm": "MITM"}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "//", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = aliases.get(line[1:-1].lower(), line[1:-1])
            continue
        if line.startswith("hostname"):
            category = "MITM"
        elif "script-path=" in line or " url script-" in line:
            category = "Script"
        elif line.startswith(("http-request", "http-response")):
            category = "Script"
        elif section in {"Body Rewrite", "Map Local"}:
            category = section
        elif line.startswith(("^http", "https?:", "http:")):
            category = "URL Rewrite"
        elif section == "Rule":
            category = line.split(",", 1)[0].upper()
        else:
            category = section
        item = {"category": category, "line": line}
        found[key(item)] = item
    return [found[k] for k in sorted(found)]


def key(item):
    return item["category"] + "\n" + canonical(item["line"])


def source_list(config):
    sources = []
    for item in config["controlled_sources"]:
        if item.get("enabled"):
            verify_source_url(item)
            sources.append({**item, "kind": "module", "auto": True})
    for item in config.get("pinned_scripts", []):
        sources.append({
            **item, "kind": "script", "auto": False,
            "url": f"https://raw.githubusercontent.com/{item['repository']}/{item['branch']}/{item['path']}",
        })
    for item in config.get("watch_only", []):
        sources.append({**item, "id": item.get("id") or item["name"],
                        "kind": item.get("kind", "module"), "auto": False})
    for item in config.get("upstream_scripts", []):
        sources.append({**item, "kind": "script", "auto": False})
    if len({s["id"] for s in sources}) != len(sources):
        raise ValueError("Duplicate upstream source ID")
    for item in sources:
        parsed = urllib.parse.urlsplit(item["url"])
        if parsed.scheme != "https" or parsed.netloc != "raw.githubusercontent.com" or parsed.username:
            raise ValueError(f"Unapproved upstream URL: {item['id']}")
    return sources


def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Shadowrocket-UpstreamSync/2"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"HTTP {response.status}")
        payload = response.read(LIMIT_BYTES + 1)
    if len(payload) > LIMIT_BYTES:
        raise ValueError("Upstream exceeds size budget")
    return payload.decode("utf-8")


def evidence_domains(text, minimum, maximum):
    # Only simple ABP domain-block entries; exceptions and modifiers are never evidence.
    domains = set()
    for line in text.splitlines():
        match = re.fullmatch(r"\|\|([a-zA-Z0-9.-]+)\^", line.strip())
        if match:
            host = normalize_host(match[1])
            if host: domains.add(host)
    if not minimum <= len(domains) <= maximum:
        raise ValueError(f"交叉来源域名数量异常: {len(domains)}")
    return domains


def evidence_for(host, domains):
    # ABP ||domain^ covers subdomains; only publish the exact candidate host.
    labels = host.split(".")
    return any(".".join(labels[i:]) in domains for i in range(len(labels) - 1))


def covered(item, module):
    match = SIMPLE.fullmatch(item["line"])
    if not match:
        return any(canonical(item["line"]) == canonical(line)
                   for line in sections(module).get(item["category"], []))
    kind, host = match[1].upper(), match[2].lower()
    for rule in sections(module).get("Rule", []):
        other = SIMPLE.fullmatch(rule)
        if not other:
            continue
        other_kind, domain = other[1].upper(), other[2].lower()
        if other_kind == "DOMAIN-SUFFIX" and (host == domain or host.endswith("." + domain)):
            return True
        if kind == other_kind == "DOMAIN" and host == domain:
            return True
    return False


def eligible(item, source, policy):
    """An exact approval permits that exact rule, never an expanded URL pattern."""
    match = SIMPLE.fullmatch(item["line"])
    if match:
        kind, host = match[1].upper(), normalize_host(match[2])
        flags = {s.strip() for s in (match[3] or "").split(",") if s.strip()}
        if not host or not flags <= FLAGS:
            return None, "域名或规则参数需要审核"
        if kind == "DOMAIN" and (safe_ad_domain(host) or host in policy.get("exact_allowlist", [])):
            return f"DOMAIN,{host},REJECT,extended-matching,pre-matching", None
        if kind == "DOMAIN-SUFFIX" and host in policy.get("suffix_allowlist", []):
            return f"DOMAIN-SUFFIX,{host},REJECT,extended-matching,pre-matching", None
        return None, "受保护域名或未经审核的后缀规则"
    if item["category"] == "URL Rewrite":
        for entry in policy.get("reviewed_rewrites", []):
            if entry["source"] == source["id"] and entry["upstream"] == item["line"]:
                if " - " not in entry["publish"] or entry["publish"].split(" - ")[1] not in {"reject", "reject-dict", "reject-200"}:
                    raise ValueError("Approved interface must use a fixed reject action")
                re.compile(entry["publish"].split(" - ")[0])
                return entry["publish"], None
        return None, "广告接口路径或动作需要审核"
    if item["category"] in {"Script", "MITM", "Body Rewrite", "Map Local"}:
        return None, "脚本、响应处理或 HTTPS 解密范围需要审核"
    return None, "不属于可自动导入的规则类型"


def add_block(module, begin, end, lines, section):
    if module.count(begin) != module.count(end) or module.count(begin) > 1:
        raise ValueError("Managed block markers are unbalanced")
    if not lines:
        return module
    if begin in module:
        head, rest = module.split(begin, 1)
        body, tail = rest.split(end, 1)
        existing = [s for s in body.splitlines() if s and not s.startswith("#")]
        return head + begin + "\n" + "\n".join(existing + lines) + "\n" + end + tail
    if module.count(section) != 1:
        raise ValueError(f"Missing or duplicate {section}")
    return module.replace(section, section + "\n\n" + begin + "\n" + "\n".join(lines) + "\n" + end, 1)


def check_batch_growth(candidates, module, policy):
    """Pause a suspicious whole batch; never slice otherwise eligible changes."""
    floor = int(policy.get("unusual_additions_floor", 50))
    growth = float(policy.get("unusual_growth_ratio", 0.25))
    current = sections(module)
    count = len(current.get("Rule", [])) + len(current.get("URL Rewrite", []))
    if len(candidates) > floor and len(candidates) > max(count, 1) * growth:
        raise ValueError(f"异常批量新增 {len(candidates)} 条，现有规则 {count} 条；整批暂停，需核对上游和审批范围")


def validate_candidate(root, module):
    errors = validate((root / PROFILE).read_text("utf-8"), module)
    if errors:
        raise ValueError("; ".join(errors))


def update_metadata(root, module, applied, stamp):
    module = re.sub(r"(?m)^#!desc=仓库更新时间：.*$", f"#!desc=仓库更新时间：{stamp}", module, count=1)
    readme = (root / "README.md").read_text("utf-8")
    readme = re.sub(r"(?m)^- \*\*最近更新时间：\*\* .*$", f"- **最近更新时间：** {stamp}", readme, count=1)
    readme = re.sub(r"(?m)^- \*\*最近实质更新：\*\* .*$",
                    f"- **最近实质更新：** {stamp}（自动同步 {len(applied)} 条已审核广告规则）", readme, count=1)
    history = (root / "CHANGELOG.md").read_text("utf-8")
    if history.count(HISTORY_MARKER) != 1:
        raise ValueError("Substantive-update history marker missing or duplicated")
    details = "\n".join("- " + BT + item["published"] + BT + "（来源：" + "、".join(item.get("evidence", [item["source"]])) + "）" for item in applied)
    entry = (f"\n\n## {stamp}（北京时间）｜自动同步 {len(applied)} 条已审核广告规则\n\n"
             "**类型：** 精确域名及显式批准的后缀/广告接口同步。脚本与解密变更只进入待审核清单。\n\n"
             + details + "\n\n离线检查不代表手机端已验证。\n")
    history = history.replace(HISTORY_MARKER, HISTORY_MARKER + entry, 1)
    return module, readme, history


def read_json(path, default):
    return json.loads(path.read_text("utf-8")) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", "utf-8")
    temporary.replace(path)


def write_reports(root, report, state):
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    write_json(reports / "upstream-state.json", state)
    write_json(reports / "upstream-review.json", report)
    label = STATUS_LABELS[report["status"]]
    module = (root / "Module.sgmodule").read_text("utf-8")
    stamp = re.search(r"(?m)^#!desc=仓库更新时间：(.*)$", module)
    counts = Counter(item["category"] for item in report["pending"])
    summary = (
        "# 广告规则自动同步状态\n\n"
        f"- **最近检查：** {report['checked_at']}（北京时间）\n"
        f"- **检查结果：** {label}\n"
        f"- **规则有效更新时间：** {stamp[1] if stamp else '未设置'}\n"
        f"- **上游文件：** {len(report['sources'])} 个；发生变化 {sum(s.get('changed', False) for s in report['sources'])} 个\n"
        f"- **本次发布：** {len(report['applied'])} 条；因异常或校验失败暂缓 {len(report['deferred'])} 条\n"
        f"- **持续待审核：** {len(report['pending'])} 项；失败 {len(report['errors'])} 项\n\n"
        "每天北京时间 08:30 计划检查，GitHub 调度可能延迟。"
        "只有正式模块内容变化才刷新模块有效更新时间；单纯检查或待审核不会刷新。\n\n"
        "[待审核与本次差异](interface-updates.md) · [完整检查明细](upstream-review.json)\n\n"
        "## 各上游状态\n\n| 上游 | 结果 | 规则变动 | 内容 SHA-256 |\n|---|---|---|---|\n"
    )
    for source in report["sources"]:
        outcome = "失败" if source.get("error") else "首次建立基线" if source.get("baseline") else "检测到变化" if source.get("changed") else "无变化"
        summary += f"| [{source['id']}]({source['url']}) | {outcome} | +{source.get('added', 0)} / −{source.get('removed', 0)} | {BT}{source.get('sha256', '')[:12]}{BT} |\n"
    if report["errors"]:
        summary += "\n## 失败原因\n\n" + "\n".join("- " + e for e in report["errors"]) + "\n"
    (reports / "status.md").write_text(summary, "utf-8")
    detail = (
        "# 上游变化与持续待审核清单\n\n"
        f"最近检查：{report['checked_at']}（北京时间）；结果：**{label}**。\n\n"
        "首次运行建立完整基线，清单包含尚未采用的历史存量，不代表当天新增；首次纳入追踪时间不一定是上游最初发布日期。后续比较新增、删除及内容哈希。"
        "待审核项目会持续保留，不会因第二天没有新变化而消失。"
        "来源规则被删除时，不会擅自删除本地人工规则。\n\n"
        "完整条目、来源、原因、增删和脚本哈希均见 [upstream-review.json](upstream-review.json)。"
        "下方每类最多预览 30 项，JSON 不截断。\n\n"
    )
    groups = {"豆瓣": r"douban|frodo|erebor", "B站": r"bilibili|biliapi|bilivideo|hdslb", "京东": r"jd\.com|360buy|jdcloud", "闲鱼": r"goofish|idlecommerce|idlehome", "高德": r"amap|gaode", "网易云": r"music\.163|music\.126|netease", "中国联通": r"10010"}
    added = {(c["source"], key(item)) for c in report.get("changes", []) if not c.get("baseline") for item in c.get("added", [])}
    detail += "## 常用 App 优先查看\n\n按域名和接口关键词推测归属；共享域名及上游整行主机列表可能误归类，须人工核对。\n\n"
    for name, pattern in groups.items():
        items = sorted([x for x in report["pending"] if len(x["line"]) < 1000 and re.search(pattern, x["line"], re.I)], key=lambda x: (x.get("last_changed", ""), x.get("first_seen", "")), reverse=True)
        fresh = sorted([x for x in items if x.get("first_seen") == report["checked_at"] or x.get("last_changed") == report["checked_at"]], key=lambda x: x.get("first_seen", ""), reverse=True)
        detail += f"### {name}｜本次新增 {len(fresh)} 项，历史待审 {len(items)-len(fresh)} 项\n\n"
        for item in (fresh + [x for x in items if x not in fresh])[:20]:
            tag = "新发现/变化" if item in fresh else "持续待审"
            detail += f"- **{tag}** {item['source']}（首次纳入追踪 {item.get('first_seen', '未知')}，最近变化 {item.get('last_changed', '未知')}）：{BT}{item['line'].replace(BT, chr(39))}{BT}\n"
        detail += "\n"
    detail += "## 本次上游新增与删除\n\n"
    for change in report.get("changes", []):
        if change.get("baseline"): continue
        for action in ("added", "removed"):
            items = change.get(action, [])
            if not items: continue
            detail += f"- {change['source']} {action}：{len(items)} 项；完整明细见 JSON。\n"
    detail += "\n## 按规则类型查看\n\n"
    for category, count in sorted(counts.items()):
        detail += f"## {category}（{count} 项待审核）\n\n"
        for item in [x for x in report["pending"] if x["category"] == category][:30]:
            line = item["line"].replace(BT, "'")
            detail += f"- **{item['source']}** — {item['reason']}\n\n  {BT}{line}{BT}\n\n"
    if not report["pending"]:
        detail += "无待审核项目。\n"
    if report["deferred"]:
        detail += f"\n因异常批量变化或发布校验失败暂缓：{len(report['deferred'])} 条；原因见状态报告。正常更新不按数量分批。\n"
    (reports / "interface-updates.md").write_text(detail, "utf-8")
    action_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if action_summary:
        with open(action_summary, "a", encoding="utf-8") as stream:
            stream.write(summary)


def run(root, config, fetch=fetch_text, check=validate_candidate, stamp=None):
    stamp = stamp or datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    report = {"schema_version": 2, "checked_at": stamp, "status": "no_upstream_changes",
              "sources": [], "applied": [], "pending": [], "deferred": [], "errors": []}
    state = read_json(root / "reports/upstream-state.json", {"schema_version": 2, "sources": {}})
    previous = state.get("sources", {})
    next_sources = dict(previous)
    old_module = (root / "Module.sgmodule").read_text("utf-8")
    policy = config.get("sync_policy", {})
    candidates, attempted, pending_keys = [], set(), set()
    ledger = state.get("pending_ledger", {})
    old_ledger = dict(ledger)
    cross = policy.get("cross_reference")
    evidence = set()
    if cross:
        try:
            parsed = urllib.parse.urlsplit(cross["url"])
            if parsed.scheme != "https" or parsed.netloc != "raw.githubusercontent.com" or parsed.username:
                raise ValueError("交叉来源地址不受信任")
            blob = fetch(cross["url"])
            if len(blob.encode("utf-8")) > int(cross.get("max_bytes", LIMIT_BYTES)):
                raise ValueError("交叉来源文件过大")
            evidence = evidence_domains(blob, int(cross["min_domains"]), int(cross["max_domains"]))
            report["sources"].append({"id":cross["id"], "url":cross["url"], "kind":"evidence", "sha256":sha(blob), "changed":sha(blob) != state.get("evidence_sha256"), "baseline":not bool(state.get("evidence_sha256"))})
        except Exception as error:
            report["errors"].append(f"交叉来源 {cross.get('id')}：{type(error).__name__}: {error}")
            report["sources"].append({"id":cross.get("id"), "url":cross.get("url"), "kind":"evidence", "error":str(error)})

    def pending(source, item, reason, **extra):
        identity = (source, key(item), reason)
        if identity not in pending_keys:
            pending_keys.add(identity)
            ledger_key = sha(source + "\n" + key(item) + "\n" + reason)
            before = old_ledger.get(ledger_key, {})
            seen = before.get("first_seen", stamp)
            changed = before.get("last_changed", stamp)
            signature = extra.get("sha256")
            if before and signature and signature != before.get("signature"): changed = stamp
            ledger[ledger_key] = {"first_seen":seen, "last_changed":changed, "signature":signature, "status":"待审核"}
            report["pending"].append({"source": source, **item, "reason": reason, "first_seen":seen, "last_changed":changed, "review_status":"待审核", **extra})

    for source in source_list(config):
        sid = source["id"]
        prior = previous.get(sid, {})
        item_status = {"id": sid, "url": source["url"], "kind": source["kind"]}
        try:
            content = fetch(source["url"])
            size = len(content.encode("utf-8"))
            if not content.strip() or size > int(source.get("max_bytes", LIMIT_BYTES)):
                raise ValueError("Empty or unexpectedly large upstream")
            if len(content.splitlines()) > int(source.get("max_source_lines", 20000)):
                raise ValueError("Upstream exceeds line budget")
            if content.lstrip().lower().startswith(("<!doctype html", "<html")):
                raise ValueError("Upstream returned an HTML page")
            current_items = inventory(content, source["kind"])
            old_items = prior.get("items", [])
            current = {key(x): x for x in current_items}
            old = {key(x): x for x in old_items}
            if source["auto"]:
                count = sum(1 for x in current_items if x["category"] == "DOMAIN" and SIMPLE.fullmatch(x["line"]))
                if not int(source["min_exact_rules"]) <= count <= int(source["max_exact_rules"]):
                    raise ValueError(f"Unexpected source shape: {count} exact rules")
                if old and len(current) < len(old) * float(policy.get("min_inventory_ratio", 0.5)):
                    raise ValueError("Upstream inventory shrank unexpectedly")
            fingerprint = sha(content)
            changed = fingerprint != prior.get("sha256")
            retired = {key(x): x for x in prior.get("retired", [])}
            retired.update({k: old[k] for k in old.keys() - current.keys()})
            retired = {k: x for k, x in retired.items() if k not in current}
            next_sources[sid] = {
                "sha256": fingerprint, "url": source["url"], "kind": source["kind"],
                "items": current_items, "retired": list(retired.values()),
                "approved_sha256": source.get("reviewed_sha256") or prior.get("approved_sha256"),
                "last_success": stamp,
            }
            item_status.update(sha256=fingerprint, changed=changed, baseline=not bool(prior),
                               added=len(current.keys() - old.keys()), removed=len(old.keys() - current.keys()))
            report.setdefault("changes", []).append({
                "source": sid, "baseline": not bool(prior), "previous_sha256": prior.get("sha256"),
                "sha256": fingerprint, "inventory_count": len(current),
                "added": [current[k] for k in sorted(current.keys() - old.keys())] if prior else [],
                "removed": [old[k] for k in sorted(old.keys() - current.keys())],
            })
            if source["kind"] == "script":
                if fingerprint != next_sources[sid]["approved_sha256"]:
                    pending(sid, {"category": "Script body", "line": source["url"]},
                            "上游脚本内容尚未审核；不自动替换本地脚本",
                            sha256=fingerprint, previous_sha256=prior.get("sha256"))
            for item in current_items:
                if covered(item, old_module):
                    continue
                if not source["auto"]:
                    pending(sid, item, "参考上游变化；不自动导入脚本或解密配置")
                    continue
                publish, reason = eligible(item, source, policy)
                if not publish:
                    pending(sid, item, reason)
                    continue
                domain_match = SIMPLE.fullmatch(item["line"])
                if cross and domain_match and domain_match[1].upper() == "DOMAIN" and domain_match[2].lower() not in policy.get("exact_allowlist", []):
                    if not evidence_for(domain_match[2].lower(), evidence):
                        pending(sid, item, "缺少第二来源交叉收录，暂不自动发布", evidence_source=cross["id"])
                        continue
                target = {**item, "line": publish}
                if covered(target, old_module) or publish in attempted:
                    continue
                attempted.add(publish)
                candidates.append({"source": sid, **item, "published": publish,
                                   "evidence": [sid] + ([cross["id"]] if cross and domain_match and domain_match[1].upper() == "DOMAIN" and evidence_for(domain_match[2].lower(), evidence) else [])})
            for item in retired.values():
                if covered(item, old_module):
                    pending(sid, item, "上游已删除；本地仍在使用，需确认后再移除")
        except Exception as error:
            item_status["error"] = f"{type(error).__name__}: {error}"
            report["errors"].append(sid + ": " + item_status["error"])
            previous_report = read_json(root / "reports/upstream-review.json", {})
            for item in previous_report.get("pending", []):
                if item["source"] == sid:
                    pending(sid, {"category": item["category"], "line": item["line"]}, item["reason"],
                            **{k: v for k, v in item.items() if k not in {"source", "category", "line", "reason", "first_seen", "last_changed", "review_status"}})
        report["sources"].append(item_status)

    chosen = candidates
    try:
        if cross and report["errors"]:
            raise ValueError("关键上游或交叉来源检查失败，整批暂停发布")
        check_batch_growth(chosen, old_module, policy)
        proposal = add_block(old_module, BEGIN, END,
                             [x["published"] for x in chosen if x["category"] in {"DOMAIN", "DOMAIN-SUFFIX"}],
                             "[Rule]")
        proposal = add_block(proposal, REWRITE_BEGIN, REWRITE_END,
                             [x["published"] for x in chosen if x["category"] == "URL Rewrite"],
                             "[URL Rewrite]")
        if proposal != old_module:
            check(root, proposal)
            module, readme, history = update_metadata(root, proposal, chosen, stamp)
            (root / "Module.sgmodule").write_text(module, "utf-8")
            (root / "README.md").write_text(readme, "utf-8")
            (root / "CHANGELOG.md").write_text(history, "utf-8")
            report["applied"] = chosen
    except Exception as error:
        report["errors"].append("Publication blocked: " + str(error))
        report["deferred"] = chosen + report["deferred"]
    if report["errors"]:
        report["status"] = "sync_failed"
    elif report["applied"]:
        report["status"] = "auto_updated"
    elif report["pending"] or report["deferred"]:
        report["status"] = "review_required"
    elif any(s.get("changed") for s in report["sources"]):
        report["status"] = "observed_no_publish"
    write_reports(root, report, {"schema_version": 2, "sources": next_sources, "pending_ledger": ledger,
                                 "evidence_sha256": sha(blob) if cross and evidence else state.get("evidence_sha256")})
    return report


def record_failure(root, reason):
    report = read_json(root / "reports/upstream-review.json",
                       {"schema_version": 2, "sources": [], "pending": [], "deferred": [], "applied": [], "errors": []})
    report.update(status="sync_failed", checked_at=datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M"))
    report["errors"].append(reason)
    report["deferred"] = report.get("applied", []) + report.get("deferred", [])
    report["applied"] = []
    write_reports(root, report, read_json(root / "reports/upstream-state.json", {"schema_version": 2, "sources": {}}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-cache", type=Path, help="Replay previously fetched upstream files; no network")
    parser.add_argument("--record-failure", help="Record a validation failure after generated module changes are restored")
    args = parser.parse_args()
    if args.record_failure:
        record_failure(ROOT, args.record_failure)
        return 1
    try:
        config = read_json(ROOT / "sources.json", {})
        fetch = fetch_text
        if args.input_cache:
            cache = read_json(args.input_cache, {})
            def fetch(url):
                item = cache[url]
                if "error" in item:
                    raise ValueError(item["error"])
                return item["content"]
        report = run(ROOT, config, fetch)
        print(STATUS_LABELS[report["status"]] + f": applied={len(report['applied'])}, pending={len(report['pending'])}, failed={len(report['errors'])}")
        return int(bool(report["errors"]))
    except Exception as error:
        record_failure(ROOT, f"{type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

