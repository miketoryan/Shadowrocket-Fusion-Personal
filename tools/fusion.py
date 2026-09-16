#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Maintain this repository's independent Shadowrocket fusion module.

The bundled Module.sgmodule is the only source of truth. This maintainer never
downloads or replaces it from a parent fusion repository.

Selected upstream modules may update small, explicitly allowlisted blocks. Each
candidate is fetched, safety-scanned and limited to approved repositories and
sections before it can change Module.sgmodule.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "Module.sgmodule"
SOURCES = ROOT / "sources.json"
REPORTS = ROOT / "reports"
STATUS = REPORTS / "status.md"
INTERFACE_REPORT = REPORTS / "interface-updates.md"
WATCH_STATE = REPORTS / "watch-state.json"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
STALE_DAYS = int(os.environ.get("STALE_DAYS", "365"))
MAX_WORKERS = max(1, int(os.environ.get("MAX_WORKERS", "12")))
TIMEOUT = 20
UA = "Shadowrocket-Fusion-Personal/FINAL-v3"

SCRIPT_PATH_RE = re.compile(r"script-path\s*=\s*(https?://[^,\s]+)", re.I)
RULESET_RE = re.compile(r"RULE-SET\s*,\s*(https?://[^,\s]+)", re.I)
LITERAL_URL_RE = re.compile(r"(?<!\\)https?://[^\s,`\"']+", re.I)
REMOTE_RESOURCE_SUFFIXES = {
    ".conf", ".js", ".json", ".list", ".module", ".sgmodule", ".txt"
}

AUTO_BEGIN = "# BEGIN SAFE AUTO-SYNC:"
AUTO_END = "# END SAFE AUTO-SYNC:"

# High-confidence unlock/fake-entitlement signals. These are intentionally
# narrower than a plain "vip" keyword so legitimate ad-cleaning code is kept.
FORBIDDEN_CONTENT_PATTERNS = [
    re.compile(r"(?i)\b(?:crack|unlock)\b"),
    re.compile(r"(?i)revenuecat"),
    re.compile(r"(?i)nanocat\.cloud"),
    re.compile(r"(?i)\.vip_type\s*(?:\|?=|:)\s*[12]\b"),
    re.compile(r"(?i)\bdue_date\s*(?:\|?=|:)\s*[89]\d{11,}\b"),
    re.compile(r"(?i)\brole\s*(?:\|?=|:)\s*15\b"),
    re.compile(r"(?i)\.data\.vip\s*\|="),
    re.compile(r"(?i)spotify[^\n]{0,80}crack"),
]

RISKY_PATH_TOKENS = (
    "/unlock/", "crack", "/vip/", "vip.", "_vip", "-vip",
)


def request(url: str, *, range_probe=False, accept=None):
    headers = {"User-Agent": UA}
    if range_probe:
        headers["Range"] = "bytes=0-0"
    if accept:
        headers["Accept"] = accept
    if GITHUB_TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=TIMEOUT)


def fetch_bytes(url: str) -> bytes:
    last = None
    for attempt in range(3):
        try:
            with request(url, accept="text/plain,*/*") as response:
                return response.read()
        except Exception as exc:
            last = exc
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    raise last


def probe_once(url: str):
    try:
        with request(url, range_probe=True) as response:
            code = getattr(response, "status", None) or response.getcode()
            if 200 <= code < 400:
                return "reachable", int(code), None
            if code in (404, 410):
                return "dead", int(code), None
            return "unknown", int(code), f"HTTP {code}"
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 410):
            return "dead", exc.code, None
        return "unknown", exc.code, f"HTTP {exc.code}"
    except Exception as exc:
        return "unknown", None, f"{type(exc).__name__}: {exc}"


def probe(url: str):
    first = probe_once(url)
    if first[0] != "dead":
        return first
    time.sleep(2)
    second = probe_once(url)
    if second[0] == "dead":
        return second
    return "unknown", second[1], "404/410 was not confirmed on retry"


def parse_raw_github(url: str):
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != "raw.githubusercontent.com":
        return None
    parts = [urllib.parse.unquote(item) for item in parsed.path.strip("/").split("/")]
    if len(parts) < 4:
        return None
    owner, repo = parts[0], parts[1]
    rest = parts[2:]
    if len(rest) >= 5 and rest[0] == "refs" and rest[1] == "heads":
        branch = rest[2]
        path = "/".join(rest[3:])
    else:
        branch = rest[0]
        path = "/".join(rest[1:])
    if not path:
        return None
    return owner, repo, branch, path


def github_last_commit(url: str):
    parsed = parse_raw_github(url)
    if not parsed:
        return None
    owner, repo, branch, path = parsed
    query = urllib.parse.urlencode(
        {"path": path, "sha": branch, "per_page": 1},
        quote_via=urllib.parse.quote,
    )
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits?{query}"
    try:
        with request(api_url, accept="application/vnd.github+json") as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
        if not isinstance(data, list) or not data:
            return None
        stamp = (
            data[0].get("commit", {}).get("committer", {}).get("date")
            or data[0].get("commit", {}).get("author", {}).get("date")
        )
        return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")) if stamp else None
    except Exception:
        return None


def clean_url(url: str) -> str:
    return url.rstrip(".,;|])")


def static_rewrite_resources(line: str):
    resources = []
    for match in LITERAL_URL_RE.finditer(line):
        url = clean_url(match.group(0))
        suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
        if "$" in url or "{{" in url:
            continue
        if suffix in REMOTE_RESOURCE_SUFFIXES:
            resources.append(url)
    return resources


def line_dependencies(section: str, line: str):
    found = []
    match = SCRIPT_PATH_RE.search(line)
    if match:
        found.append(("script-path", clean_url(match.group(1))))
    match = RULESET_RE.search(line)
    if match:
        found.append(("RULE-SET", clean_url(match.group(1))))
    if section.lower() == "url rewrite":
        found.extend(("URL-Rewrite resource", url) for url in static_rewrite_resources(line))
    return found


def extract_dependencies(text: str):
    dependencies = {}
    section = ""
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            continue
        for kind, url in line_dependencies(section, line):
            current = dependencies.setdefault(
                url, {"kinds": set(), "first_line": line_number}
            )
            current["kinds"].add(kind)
    return dependencies


def remove_dead_lines(text: str, dead_urls: set[str]):
    removed = []
    output = []
    section = ""
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            output.append(line)
            continue
        urls = [url for _, url in line_dependencies(section, line)]
        hits = sorted(set(urls) & dead_urls)
        if hits:
            removed.extend(hits)
            continue
        output.append(line)
    return "".join(output), sorted(set(removed))


def classify(url: str, kinds: set[str]):
    state, code, error = probe(url)
    item = {
        "url": url,
        "kind": " / ".join(sorted(kinds)),
        "status": "UNKNOWN",
        "http": code,
        "last_commit": None,
        "error": error,
        "risk": None,
    }
    if state == "dead":
        item["status"] = "DEAD"
        return item
    if state == "unknown":
        return item

    if "script-path" in kinds:
        try:
            script_text = fetch_bytes(url).decode("utf-8", errors="replace")
            risk = forbidden_reason(script_text)
            if risk:
                item["status"] = "RISKY"
                item["risk"] = risk
                return item
        except Exception as exc:
            item["status"] = "UNKNOWN"
            item["error"] = f"Safety scan failed: {type(exc).__name__}: {exc}"
            return item
    last_commit = github_last_commit(url)
    if last_commit is None:
        item["status"] = "REACHABLE"
        return item
    item["last_commit"] = last_commit
    age = dt.datetime.now(dt.timezone.utc) - last_commit.astimezone(dt.timezone.utc)
    item["status"] = "STALE" if age.days > STALE_DAYS else "ACTIVE"
    return item


def fmt_date(value):
    if not value:
        return "-"
    timezone = dt.timezone(dt.timedelta(hours=8))
    return value.astimezone(timezone).strftime("%Y-%m-%d")


def md(value):
    return str(value).replace("|", "\\|")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        data = json.loads(path.read_text("utf-8"))
        return data if isinstance(data, type(default)) else default
    except Exception:
        return default


def forbidden_reason(value: str):
    for pattern in FORBIDDEN_CONTENT_PATTERNS:
        if pattern.search(value):
            return pattern.pattern
    return None


def risky_script_url(url: str):
    decoded = urllib.parse.unquote(url).lower()
    return any(token in decoded for token in RISKY_PATH_TOKENS)


def remove_forbidden_module_lines(text: str):
    """Remove only high-confidence unlock declarations from the local module."""
    output = []
    removed = []
    section = ""
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip().lower()
            output.append(line)
            continue

        reason = None
        if section == "body rewrite":
            reason = forbidden_reason(line)
        elif section == "script":
            match = SCRIPT_PATH_RE.search(line)
            if match and risky_script_url(clean_url(match.group(1))):
                reason = "risky script-path"

        if reason:
            removed.append({"line": line_number, "reason": reason})
            continue
        output.append(line)
    return "".join(output), removed


def parse_module_sections(text: str):
    sections = defaultdict(list)
    section = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            continue
        if section and stripped and not stripped.startswith("#"):
            sections[section.lower()].append(stripped)
    return sections


def allowed_raw_url(url: str, repository: str):
    parsed = parse_raw_github(url)
    if not parsed:
        return False
    owner, repo, _branch, _path = parsed
    return f"{owner}/{repo}".lower() == repository.lower()


def source_payload(entry):
    name = str(entry.get("name", "Unnamed"))
    url = str(entry.get("url", "")).strip()
    repository = str(entry.get("allowed_repository", "")).strip()
    if not url or not repository or not allowed_raw_url(url, repository):
        raise ValueError("source URL is outside allowed_repository")

    body = fetch_bytes(url).decode("utf-8", errors="replace")
    if forbidden_reason(body):
        raise ValueError("source contains forbidden unlock/proxy signals")

    replacements = entry.get("arguments", {})
    if isinstance(replacements, dict):
        for old, new in replacements.items():
            body = body.replace(str(old), str(new))

    parsed = parse_module_sections(body)
    selected = {}
    remote_urls = set()
    for requested in entry.get("sections", []):
        section = str(requested).strip()
        lines = parsed.get(section.lower(), [])
        if section.lower() == "rule":
            lines = [line for line in lines if line.upper().startswith("RULE-SET,")]
        elif section.lower() == "script":
            lines = [line for line in lines if SCRIPT_PATH_RE.search(line)]
        else:
            raise ValueError(f"section not allowlisted: {section}")
        if not lines:
            raise ValueError(f"approved section is empty: {section}")
        for line in lines:
            if forbidden_reason(line):
                raise ValueError(f"forbidden content in {section}")
            urls = [url for _kind, url in line_dependencies(section, line)]
            if not urls:
                raise ValueError(f"no auditable remote dependency in {section}")
            for dependency in urls:
                if not allowed_raw_url(dependency, repository):
                    raise ValueError(f"dependency outside {repository}: {dependency}")
                remote_urls.add(dependency)
        selected[section] = lines

    hosts = []
    if entry.get("merge_mitm_hosts", False):
        for line in parsed.get("mitm", []):
            if not line.lower().startswith("hostname") or "=" not in line:
                continue
            for host in line.split("=", 1)[1].replace("%APPEND%", "").split(","):
                host = host.strip()
                if host and re.fullmatch(r"[-*?.A-Za-z0-9]+", host):
                    hosts.append(host)

    return {
        "name": name,
        "url": url,
        "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "sections": selected,
        "remote_urls": remote_urls,
        "hosts": sorted(set(hosts)),
    }


def remove_source_blocks(text: str, source_id: str):
    begin = f"{AUTO_BEGIN} {source_id}"
    end = f"{AUTO_END} {source_id}"
    output = []
    skipping = False
    for line in text.splitlines(keepends=True):
        marker = line.strip()
        if marker == begin:
            skipping = True
            continue
        if skipping and marker == end:
            skipping = False
            continue
        if not skipping:
            output.append(line)
    return "".join(output)


def remove_duplicate_sync_lines(text: str, remote_urls: set[str]):
    output = []
    section = ""
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip()
            output.append(line)
            continue
        dependencies = {url for _kind, url in line_dependencies(section, line)}
        if dependencies & remote_urls:
            continue
        output.append(line)
    return "".join(output)


def insert_source_block(text: str, source_id: str, section_name: str, entries):
    lines = text.splitlines(keepends=True)
    start = None
    end = len(lines)
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower() == f"[{section_name.lower()}]":
            start = index
            continue
        if start is not None and index > start and stripped.startswith("[") and stripped.endswith("]"):
            end = index
            break
    if start is None:
        raise ValueError(f"target module section missing: {section_name}")

    block = [
        f"{AUTO_BEGIN} {source_id}\n",
        *[entry.rstrip("\n") + "\n" for entry in entries],
        f"{AUTO_END} {source_id}\n",
    ]
    lines[end:end] = block
    return "".join(lines)


def merge_mitm_hosts(text: str, hosts):
    if not hosts:
        return text, []
    lines = text.splitlines(keepends=True)
    section = ""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped[1:-1].strip().lower()
            continue
        if section != "mitm" or not stripped.lower().startswith("hostname") or "=" not in line:
            continue
        existing = line.split("=", 1)[1]
        additions = [host for host in hosts if host not in existing]
        if additions:
            newline = "\n" if line.endswith("\n") else ""
            lines[index] = line.rstrip("\n").rstrip() + "," + ",".join(additions) + newline
        return "".join(lines), additions
    raise ValueError("target module MITM hostname line missing")


def sync_allowlisted_sources(text: str):
    config = load_json(SOURCES, {"auto_sync_modules": []})
    results = []
    for entry in config.get("auto_sync_modules", []):
        if not isinstance(entry, dict) or entry.get("enabled", True) is False:
            continue
        source_id = str(entry.get("id", "")).strip()
        name = str(entry.get("name", source_id or "Unnamed"))
        if not re.fullmatch(r"[a-z0-9-]+", source_id):
            results.append({"name": name, "state": "BLOCKED", "detail": "invalid source id"})
            continue
        try:
            payload = source_payload(entry)
            updated = remove_source_blocks(text, source_id)
            updated = remove_duplicate_sync_lines(updated, payload["remote_urls"])
            for section, entries in payload["sections"].items():
                updated = insert_source_block(updated, source_id, section, entries)
            updated, added_hosts = merge_mitm_hosts(updated, payload["hosts"])
            text = updated
            results.append({
                "name": name,
                "state": "SYNCED",
                "detail": (
                    f"{sum(len(v) for v in payload['sections'].values())} lines; "
                    f"{len(added_hosts)} new MITM hosts; sha256 {payload['sha256'][:12]}"
                ),
                "url": payload["url"],
            })
        except Exception as exc:
            results.append({
                "name": name,
                "state": "BLOCKED",
                "detail": f"{type(exc).__name__}: {exc}",
                "url": str(entry.get("url", "")),
            })
    return text, results


def watch_interfaces(sync_results):
    old_state = load_json(WATCH_STATE, {})
    new_state = {}
    rows = []
    sources = load_json(SOURCES, {"watched_modules": []})

    for entry in sources.get("watched_modules", []):
        if not isinstance(entry, dict) or entry.get("enabled", True) is False:
            continue
        name = str(entry.get("name", "Unnamed"))
        url = str(entry.get("url", "")).strip()
        if not url:
            continue

        previous = old_state.get(url, {}) if isinstance(old_state.get(url, {}), dict) else {}
        previous_sha = previous.get("sha256")
        state, code, error = probe(url)
        sha = None
        if state == "reachable":
            try:
                sha = hashlib.sha256(fetch_bytes(url)).hexdigest()
            except Exception as exc:
                state = "unknown"
                error = f"{type(exc).__name__}: {exc}"

        if state == "dead":
            change = "WATCH SOURCE DEAD"
        elif state == "unknown":
            change = "UNKNOWN"
            sha = previous_sha
        elif previous_sha is None:
            change = "baseline"
        elif previous_sha != sha:
            change = "CHANGED"
        else:
            change = "unchanged"

        last_commit = github_last_commit(url) if state == "reachable" else None
        new_state[url] = {
            "name": name,
            "sha256": sha,
            "http": code,
            "last_commit": last_commit.isoformat() if last_commit else None,
            "error": error,
        }
        rows.append((name, change, code, fmt_date(last_commit), url, entry.get("note", "")))

    WATCH_STATE.write_text(
        json.dumps(new_state, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )
    lines = [
        "# Interface source maintenance",
        "",
        "> `SYNCED` sources passed repository, section and unlock-risk checks. `BLOCKED` sources do not modify the module.",
        "",
        "## Safe auto-sync",
        "",
        "| App/source | State | Detail | URL |",
        "|---|---|---|---|",
    ]
    if sync_results:
        for item in sync_results:
            lines.append(
                f"| {md(item['name'])} | **{item['state']}** | "
                f"{md(item['detail'])} | {md(item.get('url', '-'))} |"
            )
    else:
        lines.append("| - | - | No automatic sources configured | - |")
    lines += [
        "",
        "## Report-only watch",
        "",
        "> `CHANGED` means a watched source changed. It is never auto-merged.",
        "",
        "| App/source | State | HTTP | Last commit | URL | Note |",
        "|---|---|---:|---|---|---|",
    ]
    if rows:
        for name, change, code, last, url, note in rows:
            lines.append(
                f"| {md(name)} | **{change}** | {code or '-'} | {last} | "
                f"{md(url)} | {md(note)} |"
            )
    else:
        lines.append("| - | - | - | - | - | No watched sources configured |")
    INTERFACE_REPORT.write_text("\n".join(lines) + "\n", "utf-8")


def audit_dependencies(dependencies):
    audit = {}
    items = sorted(dependencies.items())
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, max(1, len(items)))) as pool:
        futures = {
            pool.submit(classify, url, metadata["kinds"]): url
            for url, metadata in items
        }
        completed = 0
        for future in as_completed(futures):
            url = futures[future]
            audit[url] = future.result()
            completed += 1
            print(f"[{completed}/{len(items)}] {audit[url]['status']} {url}")
    return audit


def main():
    if not MODULE.exists():
        raise FileNotFoundError(
            "Module.sgmodule is missing. Restore the bundled file; this independent "
            "maintainer will not fetch a parent fusion module."
        )

    REPORTS.mkdir(parents=True, exist_ok=True)
    text = MODULE.read_text("utf-8")
    text, forbidden_removed = remove_forbidden_module_lines(text)
    text, sync_results = sync_allowlisted_sources(text)
    dependencies = extract_dependencies(text)
    audit = audit_dependencies(dependencies)
    confirmed_dead = {url for url, item in audit.items() if item["status"] == "DEAD"}
    confirmed_risky = {url for url, item in audit.items() if item["status"] == "RISKY"}
    text, dead_removed = remove_dead_lines(text, confirmed_dead)
    text, risky_removed = remove_dead_lines(text, confirmed_risky)
    remaining = extract_dependencies(text)

    counts = defaultdict(int)
    for item in audit.values():
        counts[item["status"]] += 1

    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d")
    description = (
        f"#!desc=个人维护 {today} | remote {len(remaining)}"
        f" | active {counts['ACTIVE']}"
        f" | stale {counts['STALE']}"
        f" | reachable {counts['REACHABLE']}"
        f" | unknown {counts['UNKNOWN']} | risky {counts['RISKY']} | dead-left 0"
    )
    if re.search(r"^#!name\s*=.*$", text, flags=re.M):
        text = re.sub(
            r"^#!name\s*=.*$", "#!name=融合模块·个人维护版", text, count=1, flags=re.M
        )
    else:
        text = "#!name=融合模块·个人维护版\n" + text
    if re.search(r"^#!desc\s*=.*$", text, flags=re.M):
        text = re.sub(r"^#!desc\s*=.*$", description, text, count=1, flags=re.M)
    else:
        lines = text.splitlines(keepends=True)
        text = lines[0] + description + "\n" + "".join(lines[1:])
    MODULE.write_text(text, "utf-8")

    report = [
        "# Fusion Personal health",
        "",
        "- Source of truth: **this repository's bundled `Module.sgmodule`**",
        "- Parent fusion repository dependency: **none**",
        f"- Current remote dependencies audited: **{len(dependencies)}**",
        f"- ACTIVE: **{counts['ACTIVE']}**",
        f"- REACHABLE: **{counts['REACHABLE']}**",
        f"- STALE (> {STALE_DAYS} days): **{counts['STALE']}**",
        f"- UNKNOWN: **{counts['UNKNOWN']}**",
        f"- Confirmed DEAD found this run: **{counts['DEAD']}**",
        f"- Confirmed dead declaration lines removed this run: **{len(dead_removed)}**",
        f"- Remote scripts blocked for unlock risk: **{counts['RISKY']}**",
        f"- Risky remote declaration lines removed this run: **{len(risky_removed)}**",
        f"- Forbidden unlock declarations removed this run: **{len(forbidden_removed)}**",
        f"- Safe auto-sync sources passed: **{sum(1 for item in sync_results if item['state'] == 'SYNCED')}**",
        f"- Safe auto-sync sources blocked: **{sum(1 for item in sync_results if item['state'] == 'BLOCKED')}**",
        "- DEAD dependencies left in Module.sgmodule: **0**",
        "",
        "> Only twice-confirmed HTTP 404/410 is auto-removed. 403/429/timeouts remain UNKNOWN and are kept.",
        "> High-confidence VIP/unlock declarations are removed. An unsafe upstream sync is blocked and the previous managed block is retained.",
        "",
        "## Removed this run",
        "",
    ]
    removed_rows = [f"- DEAD: `{url}`" for url in dead_removed]
    removed_rows += [f"- RISKY: `{url}`" for url in risky_removed]
    report.extend(removed_rows or ["None."])
    report += [
        "", "## Current dependency health", "",
        "| Status | Type | HTTP | Last commit | URL |",
        "|---|---|---:|---|---|",
    ]
    for url, item in sorted(audit.items(), key=lambda pair: (pair[1]["status"], pair[0])):
        report.append(
            f"| {item['status']} | {item['kind']} | {item['http'] or '-'} | "
            f"{fmt_date(item['last_commit'])} | {md(url)} |"
        )
    if forbidden_removed:
        report += ["", "## Forbidden declarations removed", ""]
        report.extend(
            f"- Original line {item['line']}: `{md(item['reason'])}`"
            for item in forbidden_removed
        )
    STATUS.write_text("\n".join(report) + "\n", "utf-8")
    watch_interfaces(sync_results)
    print("Maintenance complete.")
    print(f"  dependencies audited: {len(dependencies)}")
    print(f"  dead removed: {len(dead_removed)}")
    print(f"  risky remote declarations removed: {len(risky_removed)}")
    print(f"  forbidden declarations removed: {len(forbidden_removed)}")
    print(f"  safe sync passed: {sum(1 for item in sync_results if item['state'] == 'SYNCED')}")
    print(f"  safe sync blocked: {sum(1 for item in sync_results if item['state'] == 'BLOCKED')}")


if __name__ == "__main__":
    main()
