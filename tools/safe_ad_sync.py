#!/usr/bin/env python3
"""Safe daily sync: import only tightly filtered exact ad domains from an approved upstream.

Never sync scripts, HTTP rewriting, MITM, business APIs, suffixes, IPs or proxy rules.
An unexpected source layout/error leaves the published module unchanged.
"""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from fusion import extract_source, safe_ad_domain, verify_source_url

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "Module.sgmodule"
README = ROOT / "README.md"
HISTORY = ROOT / "CHANGELOG.md"
HISTORY_MARKER = "<!-- EFFECTIVE_UPDATES_START -->"
CONFIG = ROOT / "sources.json"
BEGIN = "# BEGIN DAILY SAFE AD DOMAINS"
END = "# END DAILY SAFE AD DOMAINS"
LIMIT_PER_RUN = 10
CEILING = 150


def active_rules(text: str):
    exact, suffix = set(), set()
    for line in text.splitlines():
        m = re.match(r"^DOMAIN,([^,]+),REJECT(?:,|$)", line)
        if m:
            exact.add(m.group(1).lower())
        m = re.match(r"^DOMAIN-SUFFIX,([^,]+),REJECT(?:,|$)", line)
        if m:
            suffix.add(m.group(1).lower())
    return exact, suffix


def covered(host, exact, suffix):
    return host in exact or any(host == s or host.endswith("." + s) for s in suffix)


def main():
    config = json.loads(CONFIG.read_text("utf-8"))
    upstreams = [s for s in config["controlled_sources"] if s.get("enabled")]
    if len(upstreams) != 1 or upstreams[0]["id"] != "fmz200-exact-ad-domains":
        raise SystemExit("Approved source list changed; manual review required")
    item = upstreams[0]
    verify_source_url(item)
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Shadowrocket-Fusion-SafeSync/1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise ValueError("Upstream did not return HTTP 200")
        blob = response.read(1024 * 1024 + 1)
    if len(blob) > 1024 * 1024:
        raise ValueError("Upstream exceeds size budget")
    source = extract_source(item, blob.decode("utf-8"))
    original = MODULE.read_text("utf-8")
    if original.count("[URL Rewrite]") != 1 or original.count("[Rule]") != 1:
        raise ValueError("Module structure has changed")
    if original.count(BEGIN) != original.count(END):
        raise ValueError("Auto block markers unbalanced")
    if original.count(BEGIN) > 1:
        raise ValueError("Duplicate auto block")
    exact, suffix = active_rules(original)
    safe = [h for h in source["hosts"] if safe_ad_domain(h)]
    added = [h for h in safe if not covered(h, exact, suffix)][:LIMIT_PER_RUN]
    if not added:
        print("Upstream checked; no new safe exact hosts")
        return
    new_rules = [f"DOMAIN,{h},REJECT,extended-matching,pre-matching" for h in added]
    if BEGIN in original:
        head, rest = original.split(BEGIN, 1)
        managed, tail = rest.split(END, 1)
        existing = [l for l in managed.splitlines() if l.startswith("DOMAIN,")]
        if len(existing) + len(new_rules) > CEILING:
            raise ValueError("Cumulative daily-rule ceiling reached")
        updated = head + BEGIN + "\n" + "# Source: fmz200 exact-domain allowlisted subset\n" + "\n".join(existing + new_rules) + "\n" + END + tail
    else:
        insert = BEGIN + "\n# Source: fmz200 exact-domain allowlisted subset\n" + "\n".join(new_rules) + "\n" + END + "\n\n"
        updated = original.replace("[URL Rewrite]", insert + "[URL Rewrite]", 1)
    stamp = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    updated = re.sub(r"(?m)^#!desc=仓库更新时间：.*$", f"#!desc=仓库更新时间：{stamp}", updated, count=1)
    # The dated history and README are written only when accepted rules really change.
    # Successful daily checks without a diff leave all published timestamps unchanged.
    history = HISTORY.read_text(encoding="utf-8")
    if history.count(HISTORY_MARKER) != 1:
        raise ValueError("Substantive-update history marker missing or duplicated")
    details = "\n".join(f"- `{h}`" for h in added)
    entry = (
        f"## {stamp}（北京时间）｜自动新增 {len(added)} 条广告域名\n\n"
        "**类型：** 可信上游精确广告域名安全同步（fmz200）。"
        f"**新增：{len(added)} 条；删除：0 条。**\n\n"
        "新增域名：\n" + details + "\n\n"
        "本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。"
        "静态检查不代表 App 端已验证。\n"
    )
    history = history.replace(HISTORY_MARKER, HISTORY_MARKER + "\n\n" + entry, 1)
    readme = README.read_text("utf-8")
    readme = re.sub(r"(?m)^- \*\*最近更新时间：\*\* .*$", f"- **最近更新时间：** {stamp}", readme, count=1)
    readme = re.sub(
        r"(?m)^- \*\*最近实质更新：\*\* .*$",
        f"- **最近实质更新：** {stamp}（自动新增 {len(added)} 条精确广告域名）",
        readme,
        count=1,
    )
    readme = re.sub(r"仓库更新时间：\d{4}-\d{2}-\d{2} \d{2}:\d{2}", f"仓库更新时间：{stamp}", readme)
    MODULE.write_text(updated, encoding="utf-8")
    README.write_text(readme, encoding="utf-8")
    HISTORY.write_text(history, encoding="utf-8")
    print(f"Accepted {len(added)} newly verified exact ad domains. Source safe hosts: {source['safe']}")


if __name__ == "__main__":
    main()
