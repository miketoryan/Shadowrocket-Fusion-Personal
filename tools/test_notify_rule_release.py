import json
import tempfile
import unittest
import urllib.error
from pathlib import Path

import notify_rule_release as notify

REPO = notify.REPOSITORY
HEAD = "a" * 40
MODULE = (
    "#!name=test\n#!desc=仓库更新时间：2026-11-25 22:25\n"
    "[Rule]\nDOMAIN,ads.example.com,REJECT\n[Script]\n"
    "ads=type=http-response,script-path=https://raw.githubusercontent.com/"
    + REPO + "/main/scripts/active.js?v=1\n"
)


class FakeAPI:
    def __init__(self):
        self.releases = []
        self.head = HEAD
        self.posts = []

    def request(self, method, path, body=None):
        if path.startswith("releases?"):
            return self.releases
        if path == "git/ref/heads/main":
            return {"object": {"sha": self.head}}
        if method == "POST":
            self.posts.append(body)
            release = {**body, "id": len(self.posts), "html_url": "https://github.com/release"}
            self.releases.insert(0, release)
            return release
        if path.startswith("releases/tags/"):
            return self.releases[0]
        raise AssertionError(path)


class NotificationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "reports").mkdir()
        (self.root / "Module.sgmodule").write_text(MODULE)
        (self.root / "scripts/active.js").write_text("original")
        self.initial = notify.fingerprint(self.root)[0]
        (self.root / notify.BASELINE).write_text(json.dumps({"fingerprint": self.initial, "commit": "b" * 40}))
        self.api = FakeAPI()

    def run_notify(self):
        return notify.publish(self.root, self.api, REPO, HEAD)

    def test_baseline_is_silent(self):
        self.assertEqual(self.run_notify()["status"], "no_change")
        self.assertFalse(self.api.posts)

    def test_timestamp_comments_and_blank_lines_are_silent(self):
        (self.root / "Module.sgmodule").write_text(MODULE.replace("22:25", "23:59") + "\n# only a report update\n\n")
        self.assertEqual(self.run_notify()["status"], "no_change")

    def test_unused_script_and_reports_are_silent(self):
        (self.root / "scripts/unused.js").write_text("not referenced")
        (self.root / "reports/status.md").write_text("new check, no actual rule update")
        self.assertEqual(self.run_notify()["status"], "no_change")

    def test_trailing_script_whitespace_is_not_a_rule_update(self):
        (self.root / "scripts/active.js").write_text("original\n\n")
        self.assertEqual(self.run_notify()["status"], "no_change")

    def test_active_rule_change_publishes_once(self):
        (self.root / "Module.sgmodule").write_text(MODULE.replace("ads.example", "ads.new.example"))
        self.assertEqual(self.run_notify()["status"], "published")
        self.assertEqual(self.run_notify()["status"], "no_change")
        self.assertEqual(len(self.api.posts), 1)
        self.assertFalse(self.api.posts[0]["draft"])
        self.assertFalse(self.api.posts[0]["prerelease"])
        self.assertIn("原订阅地址", self.api.posts[0]["body"])

    def test_referenced_script_change_is_substantive(self):
        (self.root / "scripts/active.js").write_text("changed")
        self.assertEqual(self.run_notify()["status"], "published")

    def test_superseded_commit_cannot_send_an_old_version_notice(self):
        (self.root / "scripts/active.js").write_text("changed")
        self.api.head = "c" * 40
        self.assertEqual(self.run_notify()["status"], "superseded")
        self.assertFalse(self.api.posts)

    def test_real_rollback_creates_a_new_notification(self):
        (self.root / "scripts/active.js").write_text("changed")
        self.run_notify()
        first_tag = self.api.posts[0]["tag_name"]
        (self.root / "scripts/active.js").write_text("original")
        self.assertEqual(self.run_notify()["status"], "published")
        self.assertNotEqual(self.api.posts[1]["tag_name"], first_tag)

    def test_duplicate_creation_from_concurrent_checks_is_idempotent(self):
        (self.root / "scripts/active.js").write_text("changed")
        original = self.api.request
        def race(method, path, body=None):
            if method == "POST":
                original(method, path, body)
                raise urllib.error.HTTPError("url", 422, "already exists", {}, None)
            return original(method, path, body)
        self.api.request = race
        self.assertEqual(self.run_notify()["status"], "already_published")

    def test_pinned_local_script_is_not_replaced_by_unreferenced_main_content(self):
        module = MODULE.replace("/main/scripts/", "/" + "d" * 40 + "/scripts/")
        (self.root / "Module.sgmodule").write_text(module)
        before = notify.fingerprint(self.root)[0]
        (self.root / "scripts/active.js").write_text("not the pinned revision")
        self.assertEqual(before, notify.fingerprint(self.root)[0])


if __name__ == "__main__":
    unittest.main()
