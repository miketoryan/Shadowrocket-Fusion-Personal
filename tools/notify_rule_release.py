#!/usr/bin/env python3
"""Publish a GitHub Release only for changed active rules or referenced scripts.

GitHub delivers Release subscription emails; this program needs no SMTP login.
The initial baseline is silent. Metadata-only checks never publish a release.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "miketoryan/Shadowrocket-Fusion-Personal"
BASELINE = "reports/rule-release-baseline.json"
MARKER = re.compile(r"<!-- shadowrocket-rules-sha256:([0-9a-f]{64}) -->")
TAG_PREFIX = "adblock-"


def fingerprint(root, repository=REPOSITORY):
    module = (root / "Module.sgmodule").read_text("utf-8")
    active = [line.strip() for line in module.splitlines()
              if line.strip() and not line.strip().startswith(("#", "//", ";"))]
    scripts = {}
    for url in re.findall(r"script-path=([^,\s]+)", module):
        parsed = urllib.parse.urlsplit(url)
        parts = parsed.path.strip("/").split("/")
        if parsed.netloc != "raw.githubusercontent.com" or len(parts) < 5:
            continue
        if "/".join(parts[:2]) != repository or parts[2] != "main":
            continue
        path = "/".join(parts[3:])
        if not re.fullmatch(r"scripts/[a-zA-Z0-9_.-]+\.js", path):
            raise ValueError("Unrecognized referenced local script path")
        scripts[path] = hashlib.sha256((root / path).read_text("utf-8").rstrip().encode("utf-8")).hexdigest()
    payload = {"module": active, "scripts": scripts}
    digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return digest, scripts


class GitHub:
    def __init__(self, repository, token):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Invalid repository")
        self.base = f"https://api.github.com/repos/{repository}/"
        self.token = token

    def request(self, method, path, body=None):
        data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method, headers={
            "Authorization": "Bearer " + self.token, "Accept": "application/vnd.github+json",
            "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Shadowrocket-RuleRelease/1",
        })
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)


def latest_managed_release(api):
    page = 1
    while True:
        releases = api.request("GET", f"releases?per_page=100&page={page}")
        for release in releases:
            if release.get("draft") or release.get("prerelease"):
                continue
            match = MARKER.search(release.get("body") or "")
            if release.get("tag_name", "").startswith(TAG_PREFIX) and match:
                return release, match[1]
        if len(releases) < 100:
            return None, None
        page += 1


def publish(root, api, repository, head):
    digest, scripts = fingerprint(root, repository)
    baseline = json.loads((root / BASELINE).read_text("utf-8"))
    release, previous_digest = latest_managed_release(api)
    previous_digest = previous_digest or baseline["fingerprint"]
    if digest == previous_digest:
        return {"status": "no_change", "fingerprint": digest}
    if api.request("GET", "git/ref/heads/main")["object"]["sha"] != head:
        return {"status": "superseded", "fingerprint": digest}
    # Concurrent validators see the same previous release and choose the same tag.
    # A real rollback to an older fingerprint still has a new previous-release ID.
    previous_id = str(release["id"]) if release else "baseline"
    tag = TAG_PREFIX + digest[:20] + "-after-" + previous_id
    previous_commit = release.get("target_commitish") if release else baseline["commit"]
    module = (root / "Module.sgmodule").read_text("utf-8")
    stamp = re.search(r"(?m)^#!desc=仓库更新时间：(.*)$", module)
    timestamp = stamp[1] if stamp else "当前已发布版本"
    body = (
        "正式拦截规则或正在使用的仓库内脚本已有实质变化，请在手机上手动更新「广告屏蔽联网版」。\n\n"
        f"- 模块时间标签：**{timestamp}**（北京时间）\n"
        "- 此通知根据有效规则和所引用脚本的内容生成；仅刷新检查报告、时间标签或待审核清单不会通知。\n"
        f"- [查看版本差异](https://github.com/{repository}/compare/{previous_commit}...{head})\n"
        f"- [逐次更新明细](https://github.com/{repository}/blob/main/CHANGELOG.md)\n"
        f"- [原订阅地址](https://raw.githubusercontent.com/{repository}/main/Module.sgmodule)\n\n"
        "手机操作：更新原远程模块，重新连接小火箭，再完全退出并重新打开对应 App。\n\n"
        f"<!-- shadowrocket-rules-sha256:{digest} -->"
    )
    result = {
        "tag_name": tag, "target_commitish": head,
        "name": "小火箭广告规则实质更新｜" + timestamp, "body": body,
        "draft": False, "prerelease": False, "make_latest": "true",
    }
    try:
        created = api.request("POST", "releases", result)
        return {"status": "published", "url": created["html_url"], "fingerprint": digest}
    except urllib.error.HTTPError as error:
        if error.code not in {409, 422}:
            raise
        existing = api.request("GET", "releases/tags/" + urllib.parse.quote(tag, safe=""))
        if MARKER.search(existing.get("body") or "") and MARKER.search(existing["body"])[1] == digest:
            return {"status": "already_published", "fingerprint": digest}
        raise


def main():
    repository = os.environ.get("GITHUB_REPOSITORY", REPOSITORY)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token missing; no email or SMTP credential is required")
    if repository != REPOSITORY:
        raise ValueError("Release publication is limited to the configured repository")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    result = publish(ROOT, GitHub(repository, token), repository, head)
    print(json.dumps(result, ensure_ascii=False))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write("\n## 实质更新邮件通知\n\n" + json.dumps(result, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
