#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Maintain this repository's independent Shadowrocket fusion module.

The bundled Module.sgmodule is the only source of truth. This maintainer never
downloads or replaces it from a parent fusion repository.
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
UA = "Shadowrocket-Fusion-Personal/FINAL-v2"

SCRIPT_PATH_RE = re.compile(r"script-path\s*=\s*(https?://[^,\s]+)", re.I)
RULESET_RE = re.compile(r"RULE-SET\s*,\s*(https?://[^,\s]+)", re.I)
LITERAL_URL_RE = re.compile(r"(?<!\\)https?://[^\s,`\"']+", re.I)
REMOTE_RESOURCE_SUFFIXES = {
    ".conf", ".js", ".json", ".list", ".module", ".sgmodule", ".txt"
}


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
    }
    if state == "dead":
        item["status"] = "DEAD"
        return item
    if state == "unknown":
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


def watch_interfaces():
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
        "# Interface source watch",
        "",
        "> `CHANGED` means a watched app module changed. Review it manually; changes are never auto-merged.",
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
    dependencies = extract_dependencies(text)
    audit = audit_dependencies(dependencies)
    confirmed_dead = {url for url, item in audit.items() if item["status"] == "DEAD"}
    text, dead_removed = remove_dead_lines(text, confirmed_dead)
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
        f" | unknown {counts['UNKNOWN']} | dead-left 0"
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
        "- DEAD dependencies left in Module.sgmodule: **0**",
        "",
        "> Only twice-confirmed HTTP 404/410 is auto-removed. 403/429/timeouts remain UNKNOWN and are kept.",
        "",
        "## Removed this run",
        "",
    ]
    report.extend([f"- `{url}`" for url in dead_removed] or ["None."])
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
    STATUS.write_text("\n".join(report) + "\n", "utf-8")
    watch_interfaces()
    print("Maintenance complete.")
    print(f"  dependencies audited: {len(dependencies)}")
    print(f"  dead removed: {len(dead_removed)}")


if __name__ == "__main__":
    main()
