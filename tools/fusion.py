#!/usr/bin/env python3
"""Controlled updater for the connectivity-safe Shadowrocket module.

Only exact DOMAIN reject rules can enter the managed block. Scripts, MITM,
rewrites, remote rule sets, broad matchers, and protected service domains are
rejected before Module.sgmodule is changed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "Module.sgmodule"
SOURCES = ROOT / "sources.json"
REPORTS = ROOT / "reports"
STATUS = REPORTS / "status.md"
INTERFACE_REPORT = REPORTS / "interface-updates.md"
WATCH_STATE = REPORTS / "watch-state.json"

AUTO_BEGIN = "# BEGIN CONTROLLED AUTO RULES"
AUTO_END = "# END CONTROLLED AUTO RULES"
UA = "Shadowrocket-Fusion-Personal/controlled-v6"
TIMEOUT = 25
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

DOMAIN_RULE_RE = re.compile(
    r"^DOMAIN\s*,\s*([^,\s]+)\s*,\s*REJECT(?:\s*,.*)?$", re.I
)
HOST_RE = re.compile(
    r"(?=.{1,253}\Z)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z"
)

FORBIDDEN_TOKENS = (
    "rule-set,", "domain-keyword,", "domain-suffix,",
    "url-regex,", "ip-cidr,", "pangolin-sdk-toutiao", "wxs.qq.com",
    "httpdns", "googlevideo.com", "youtube.com", "pan.baidu.com",
)

PROTECTED_SUFFIXES = {
    "apple.com", "icloud.com", "mzstatic.com", "qq.com", "weixin.qq.com",
    "wechat.com", "wxs.qq.com", "baidu.com", "baidubce.com", "bdstatic.com",
    "youtube.com", "youtu.be", "googlevideo.com", "googleapis.com",
    "google.com", "gstatic.com", "biliapi.com", "biliapi.net",
    "bilibili.com", "iqiyi.com", "meituan.com", "dianping.com",
    "taobao.com", "alicdn.com", "tmall.com", "jd.com", "pinduoduo.com",
    "163.com", "126.net", "netease.com", "microsoft.com", "windows.com",
    "office.com", "github.com", "githubusercontent.com", "adobe.com",
}

BLOCKED_LABELS = {
    "httpdns", "dns", "api", "gateway", "gw", "push", "login", "auth",
    "account", "pay", "wallet", "security", "static", "config", "update",
    "upgrade", "download", "image", "images", "video", "music", "live",
    "chat",
}

AD_LABELS = {"ad", "ads", "adx", "advert", "mobad", "splash"}
AD_PREFIXES = (
    "adserver", "adservice", "adserving", "adtrack", "adstat", "adlog",
    "adlaunch", "admarket", "admarketing", "admonitor", "adproxy",
    "adreport", "adreq", "adcdn", "adclick", "adexpo", "adfile", "adnew",
    "adpai", "adsapi", "adsdk", "adse", "adsmind", "adsstatic", "adui",
    "advertise", "advertising", "adxapi", "adxlog", "mobad", "splash",
)

ALLOWED_MAP_LOCAL = {
    r'^https:\/\/api\.douban\.com\/v\d\/app_ads\/splash data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https:\/\/frodo\.douban\.com\/api\/v\d\/erebor\/feed_ad data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https:\/\/m\.douban\.com\/rexxar\/api\/v\d\/market\/products\/ data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https:\/\/frodo\.douban\.com\/api\/v\d\/movie\/ad data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https:\/\/frodo\.douban\.com\/api\/v\d\/home_banner data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https:\/\/frodo\.douban\.com\/api\/v\d\/search\/found_words data-type=text data="{}" status-code=200 header="Content-Type:application/json"',
    r'^https?:\/\/oss\.umetrip\.com\/fs\/advert\/polite data-type=json data="{}" status-code=200',
    r'^https?:\/\/api\.xiaoyuzhoufm\.com\/v\d\/flash data-type=json data="{}" status-code=200',
    r'^https?:\/\/mp\.weixin\.qq\.com\/wapad\/getaddata\?action=getad data-type=text data="" status-code=200',
    r'^https?:\/\/mp\.weixin\.qq\.com\/wapad\/reportaddata\?action=exposure_report data-type=text data="" status-code=200',
}

ALLOWED_URL_REWRITE = {
    r'^https?:\/\/pan\.baidu\.com\/rest\/\d\.\d\/pcs\/(ad|adx) - reject',
    r'^https?:\/\/pan\.baidu\.com\/act\/v\d\/(bchannel|welfare)\/list - reject',
    r'^https?:\/\/pan\.baidu\.com\/act\/api\/activityentry - reject',
    r'^https?:\/\/pan\.baidu\.com\/pmall\/order\/privilege\/info - reject',
    r'^https?:\/\/pan\.baidu\.com\/api\/useractivity\/activity - reject',
    r'^https?:\/\/ndstatic\.cdn\.bcebos\.com\/activity\/welfare - reject',
    r'^https?:\/\/staticsns\.cdn\.bcebos\.com\/amis\/.+/banner\.png - reject',
    r'^https?:\/\/issuecdn\.baidupcs\.com\/issue\/netdisk\/guanggao - reject',
    r'^https?:\/\/update\.pan\.baidu\.com\/statistics - reject',
}

ALLOWED_MITM_LINE = (
    "hostname = %APPEND% api.douban.com, frodo.douban.com, m.douban.com, "
    "app.bilibili.com, grpc.biliapi.net, umerp.umetrip.com, "
    "umerp.umetrip.com.cn, home.umetrip.com, bkclient.umetrip.com.cn, "
    "oss.umetrip.com, api.xiaoyuzhoufm.com, pan.baidu.com, "
    "ndstatic.cdn.bcebos.com, staticsns.cdn.bcebos.com, "
    "issuecdn.baidupcs.com, update.pan.baidu.com, mp.weixin.qq.com"
)

SCRIPT_LINE_TEMPLATES = {
    r"bili-json = type=http-response,pattern=^https:\/\/app\.bilibili\.com\/x\/"
    r"(v2\/(splash\/(list|show)|feed\/index\?)|resource\/show\/tab\/v2),"
    r"requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/"
    r"app2smile/rules/{sha}/js/bilibili-json.js,script-update-interval=0",
    r"bili-proto = type=http-response,pattern=^https:\/\/(grpc\.biliapi\.net|"
    r"app\.bilibili\.com)\/bilibili\.app\.(viewunite\.v1\.View\/View|"
    r"dynamic\.v2\.Dynamic\/DynAll)$,requires-body=1,binary-body-mode=1,"
    r"max-size=0,script-path=https://raw.githubusercontent.com/app2smile/rules/"
    r"{sha}/js/bilibili-proto.js,script-update-interval=0",
    r"umetrip = type=http-response,pattern=^https?:\/\/(bkclient|umerp|home)"
    r"\.umetrip\.com(\.cn){0,1}\/gateway\/api\/umetrip\/native,requires-body=0,"
    r"max-size=0,script-path=https://raw.githubusercontent.com/zirawell/R-Store/"
    r"{sha}/Res/Scripts/AntiAd/umetrip.js",
    r"baidupan-ads = type=http-response,pattern=^https?:\/\/pan\.baidu\.com\/"
    r"api\/getsyscfg\?,requires-body=1,max-size=0,script-path=https://raw."
    r"githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/scripts/"
    r"baidupan_ads_only.js",
}

PINNED_URL_RE = re.compile(
    r"https://raw\.githubusercontent\.com/([^/]+/[^/]+)/([0-9a-f]{40})/([^,\s]+)"
)
FORBIDDEN_SCRIPT_PATTERNS = (
    re.compile(r"(?i)revenuecat"),
    re.compile(r"(?i)vip_type"),
    re.compile(r"(?i)annual_vip"),
    re.compile(r"(?i)due_date\s*[:=]"),
    re.compile(r"(?i)\b(?:crack|unlock)\b"),
)


def load_settings() -> dict:
    data = json.loads(SOURCES.read_text("utf-8"))
    if data.get("mode") != "controlled-auto-update":
        raise ValueError("sources.json is not in controlled-auto-update mode")
    return data


def request_text(url: str) -> str:
    headers = {"User-Agent": UA, "Accept": "text/plain,*/*"}
    if GITHUB_TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    last_error = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                if not 200 <= response.status < 300:
                    raise RuntimeError(f"HTTP {response.status}")
                return response.read().decode("utf-8", errors="replace")
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"source fetch failed: {last_error}")


def normalized_script_line(line: str) -> str:
    return PINNED_URL_RE.sub(
        lambda match: (
            f"https://raw.githubusercontent.com/{match.group(1)}/"
            f"{{sha}}/{match.group(3)}"
        ),
        line,
    )


def valid_script_line(line: str) -> bool:
    return normalized_script_line(line) in SCRIPT_LINE_TEMPLATES


def latest_file_commit(entry: dict) -> str:
    repository = str(entry["repository"])
    branch = str(entry["branch"])
    path = str(entry["path"])
    query = urllib.parse.urlencode({"path": path, "sha": branch, "per_page": 1})
    api = f"https://api.github.com/repos/{repository}/commits?{query}"
    data = json.loads(request_text(api))
    commit = data[0]["sha"] if isinstance(data, list) and data else ""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"{entry['id']}: invalid latest commit")
    return commit


def audit_script_content(entry: dict, content: str) -> None:
    if len(content.encode("utf-8")) > int(entry["max_bytes"]):
        raise ValueError(f"{entry['id']}: script unexpectedly large")
    for required in entry.get("required_tokens", []):
        if required not in content:
            raise ValueError(f"{entry['id']}: required token missing: {required}")
    for pattern in FORBIDDEN_SCRIPT_PATTERNS:
        if pattern.search(content):
            raise ValueError(f"{entry['id']}: forbidden content: {pattern.pattern}")


def update_pinned_scripts(text: str, settings: dict) -> tuple[str, list[dict]]:
    results = []
    for entry in settings.get("pinned_scripts", []):
        repository = str(entry["repository"])
        path = str(entry["path"])
        commit = latest_file_commit(entry)
        raw_url = f"https://raw.githubusercontent.com/{repository}/{commit}/{path}"
        content = request_text(raw_url)
        audit_script_content(entry, content)
        url_pattern = re.compile(
            r"https://raw\.githubusercontent\.com/"
            + re.escape(repository)
            + r"/[0-9a-f]{40}/"
            + re.escape(path)
        )
        text, replacements = url_pattern.subn(raw_url, text)
        if replacements != 1:
            raise ValueError(
                f"{entry['id']}: expected one pinned module reference, got {replacements}"
            )
        results.append({
            "id": entry["id"],
            "commit": commit,
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "bytes": len(content.encode("utf-8")),
        })
    return text, results


def audit_local_scripts(settings: dict) -> list[dict]:
    results = []
    for entry in settings.get("local_scripts", []):
        path = ROOT / str(entry["path"])
        content = path.read_text("utf-8")
        audit_script_content(entry, content)
        results.append({
            "id": entry["id"],
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "bytes": len(content.encode("utf-8")),
        })
    return results


def verify_source_url(entry: dict) -> None:
    parsed = urllib.parse.urlparse(str(entry["url"]))
    parts = [urllib.parse.unquote(part) for part in parsed.path.strip("/").split("/")]
    if parsed.scheme != "https" or parsed.netloc.lower() != "raw.githubusercontent.com":
        raise ValueError(f"{entry['id']}: only raw.githubusercontent.com is allowed")
    if len(parts) < 4:
        raise ValueError(f"{entry['id']}: malformed source URL")
    repository = "/".join(parts[:2]).lower()
    path = "/".join(parts[3:])
    if repository != str(entry["allowed_repository"]).lower():
        raise ValueError(f"{entry['id']}: repository mismatch")
    if path != str(entry["allowed_path"]):
        raise ValueError(f"{entry['id']}: path mismatch")


def normalize_host(value: str) -> str | None:
    host = value.strip().lower().rstrip(".")
    if "*" in host or not HOST_RE.fullmatch(host):
        return None
    return host


def protected(host: str) -> bool:
    return any(host == suffix or host.endswith("." + suffix) for suffix in PROTECTED_SUFFIXES)


def advertising_label(label: str) -> bool:
    if label in AD_LABELS:
        return True
    if re.match(r"^(?:ad|ads|adx|advert|mobad|splash)[-_]", label):
        return True
    if re.search(r"[-_](?:ad|ads|adx)$", label):
        return True
    return any(label == prefix or label.startswith(prefix) for prefix in AD_PREFIXES)


def safe_ad_domain(host: str) -> bool:
    labels = host.split(".")
    if protected(host) or any(label in BLOCKED_LABELS for label in labels):
        return False
    return any(advertising_label(label) for label in labels)


def extract_source(entry: dict, text: str) -> dict:
    lines = text.splitlines()
    if len(lines) > int(entry["max_source_lines"]):
        raise ValueError(f"{entry['id']}: source unexpectedly large")
    exact = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = DOMAIN_RULE_RE.match(line)
        if not match:
            continue
        host = normalize_host(match.group(1))
        if host:
            exact.append(host)
    exact = sorted(set(exact))
    minimum = int(entry["min_exact_rules"])
    maximum = int(entry["max_exact_rules"])
    if not minimum <= len(exact) <= maximum:
        raise ValueError(
            f"{entry['id']}: exact rule count {len(exact)} outside {minimum}..{maximum}"
        )
    filtered = sorted(host for host in exact if safe_ad_domain(host))
    safe_min = int(entry["min_safe_rules"])
    safe_max = int(entry["max_safe_rules"])
    if not safe_min <= len(filtered) <= safe_max:
        raise ValueError(
            f"{entry['id']}: safe rule count {len(filtered)} outside {safe_min}..{safe_max}"
        )
    return {
        "id": entry["id"],
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "exact": len(exact),
        "safe": len(filtered),
        "hosts": filtered,
    }


def split_auto_block(text: str) -> tuple[str, str, str]:
    if text.count(AUTO_BEGIN) != 1 or text.count(AUTO_END) != 1:
        raise ValueError("controlled auto-rule markers are missing or duplicated")
    before, remainder = text.split(AUTO_BEGIN, 1)
    managed, after = remainder.split(AUTO_END, 1)
    return before, managed, after


def hosts_from_text(text: str) -> set[str]:
    hosts = set()
    for raw in text.splitlines():
        match = DOMAIN_RULE_RE.match(raw.strip())
        if match:
            host = normalize_host(match.group(1))
            if host:
                hosts.add(host)
    return hosts


def validate_module(text: str) -> list[str]:
    errors = []
    rules = []
    map_local = set()
    url_rewrite = set()
    scripts = set()
    mitm = set()
    section = ""
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            if section not in {"rule", "map local", "url rewrite", "script", "mitm"}:
                errors.append(f"line {number}: forbidden section [{section}]")
            continue
        if section == "rule":
            compact = line.lower().replace(" ", "")
            token = next((item for item in FORBIDDEN_TOKENS if item in compact), None)
            if token:
                errors.append(f"line {number}: forbidden token {token}")
            match = DOMAIN_RULE_RE.match(line)
            if not match:
                errors.append(f"line {number}: only exact DOMAIN reject rules are allowed")
                continue
            host = normalize_host(match.group(1))
            if not host:
                errors.append(f"line {number}: invalid domain")
            else:
                rules.append(host)
        elif section == "map local":
            if line not in ALLOWED_MAP_LOCAL:
                errors.append(f"line {number}: unapproved Map Local entry")
            map_local.add(line)
        elif section == "url rewrite":
            if line not in ALLOWED_URL_REWRITE:
                errors.append(f"line {number}: unapproved URL Rewrite entry")
            url_rewrite.add(line)
        elif section == "script":
            if not valid_script_line(line):
                errors.append(f"line {number}: unapproved script declaration")
            scripts.add(normalized_script_line(line))
        elif section == "mitm":
            if line != ALLOWED_MITM_LINE:
                errors.append(f"line {number}: unapproved MITM hostname list")
            mitm.add(line)
        else:
            errors.append(f"line {number}: active content outside approved sections")
    duplicates = [host for host, count in Counter(rules).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate domains: {len(duplicates)}")
    if not rules:
        errors.append("no active rules")
    if map_local != ALLOWED_MAP_LOCAL:
        errors.append("approved Map Local set is incomplete")
    if url_rewrite != ALLOWED_URL_REWRITE:
        errors.append("approved URL Rewrite set is incomplete")
    if scripts != SCRIPT_LINE_TEMPLATES:
        errors.append("approved script set is incomplete")
    if mitm != {ALLOWED_MITM_LINE}:
        errors.append("approved MITM list is incomplete")
    return errors


def check_delta(old: set[str], new: set[str], safety: dict) -> tuple[set[str], set[str]]:
    added = new - old
    removed = old - new
    if old:
        if len(added) > int(safety["max_additions_per_run"]):
            raise ValueError(f"too many additions in one run: {len(added)}")
        if len(removed) > int(safety["max_removals_per_run"]):
            raise ValueError(f"too many removals in one run: {len(removed)}")
        ratio = abs(len(new) - len(old)) / len(old)
        if ratio > float(safety["max_count_change_ratio"]):
            raise ValueError(f"auto-rule count changed by {ratio:.1%}")
    elif not safety.get("allow_bootstrap", False):
        raise ValueError("empty managed block cannot bootstrap automatically")
    return added, removed


def build_auto_block(hosts: set[str], results: list[dict]) -> str:
    source_ids = ", ".join(result["id"] for result in results)
    lines = [
        AUTO_BEGIN,
        f"# Sources: {source_ids}",
        "# Generated automatically; exact DOMAIN rules only.",
    ]
    lines.extend(
        f"DOMAIN,{host},REJECT,extended-matching,pre-matching"
        for host in sorted(hosts)
    )
    lines.append(AUTO_END)
    return "\n".join(lines)


def main() -> None:
    settings = load_settings()
    original = MODULE.read_text("utf-8")
    errors = validate_module(original)
    if errors:
        raise SystemExit("Unsafe current module:\n- " + "\n- ".join(errors))
    before, managed, after = split_auto_block(original)
    core_hosts = hosts_from_text(before + after)
    old_auto = hosts_from_text(managed)
    results = []
    combined = set()
    for entry in settings.get("controlled_sources", []):
        if not entry.get("enabled", False):
            continue
        verify_source_url(entry)
        result = extract_source(entry, request_text(entry["url"]))
        results.append(result)
        combined.update(result["hosts"])
    new_auto = combined - core_hosts
    safety = settings["safety"]
    if len(new_auto) > int(safety["max_total_auto_rules"]):
        raise SystemExit(f"auto-rule ceiling exceeded: {len(new_auto)}")
    added, removed = check_delta(old_auto, new_auto, safety)
    rebuilt = before.rstrip() + "\n\n" + build_auto_block(new_auto, results) + after
    if not rebuilt.endswith("\n"):
        rebuilt += "\n"
    rebuilt, script_results = update_pinned_scripts(rebuilt, settings)
    local_script_results = audit_local_scripts(settings)
    errors = validate_module(rebuilt)
    if errors:
        raise SystemExit("Generated module failed validation:\n- " + "\n- ".join(errors))
    if rebuilt != original:
        MODULE.write_text(rebuilt, "utf-8")
    REPORTS.mkdir(parents=True, exist_ok=True)
    total = len(core_hosts) + len(new_auto)
    STATUS.write_text(
        "\n".join([
            "# Fusion Personal health", "", "- Mode: **controlled auto-update**",
            f"- Stable core rules: **{len(core_hosts)}**",
            f"- Controlled auto rules: **{len(new_auto)}**",
            f"- Total exact DOMAIN rules: **{total}**",
            f"- Added this run: **{len(added)}**",
            f"- Removed this run: **{len(removed)}**",
            f"- Script declarations: **{len(SCRIPT_LINE_TEMPLATES)}**",
            f"- URL rewrites: **{len(ALLOWED_URL_REWRITE)}**",
            f"- Map Local entries: **{len(ALLOWED_MAP_LOCAL)}**",
            f"- MITM hosts: **{len(ALLOWED_MITM_LINE.split('=', 1)[1].split(','))}**",
            "- Broad match rules: **0**",
            "- Validation: **PASS**", "",
            "> Upstream content is filtered to exact advertising domains only.",
            "> A fetch, count, delta, or safety-check failure leaves Module.sgmodule unchanged.",
            "",
        ]),
        "utf-8",
    )
    INTERFACE_REPORT.write_text(
        "# Controlled source updates\n\n"
        + "\n".join(
            f"- **{item['id']}**: PASS; {item['exact']} exact → {item['safe']} safe"
            for item in results
        )
        + "\n"
        + "\n".join(
            f"- **{item['id']}**: PASS; pinned {item['commit'][:12]}; {item['bytes']} bytes"
            for item in script_results
        )
        + "\n"
        + "\n".join(
            f"- **{item['id']}**: PASS; local audited; {item['bytes']} bytes"
            for item in local_script_results
        )
        + "\n",
        "utf-8",
    )
    state = {
        item["id"]: {
            "type": "domain-source", "sha256": item["sha256"],
            "exact_rules": item["exact"], "safe_rules": item["safe"],
        }
        for item in results
    }
    state.update({
        item["id"]: {
            "type": "pinned-script", "commit": item["commit"],
            "sha256": item["sha256"], "bytes": item["bytes"],
        }
        for item in script_results
    })
    state.update({
        item["id"]: {
            "type": "local-script", "sha256": item["sha256"],
            "bytes": item["bytes"],
        }
        for item in local_script_results
    })
    WATCH_STATE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        "utf-8",
    )
    print(
        f"Controlled update passed: {len(core_hosts)} core + "
        f"{len(new_auto)} auto = {total} rules"
    )


if __name__ == "__main__":
    main()
