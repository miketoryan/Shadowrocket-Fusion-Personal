"""Stateful regressions for detection, review retention and failure publication."""
import json
import tempfile
import unittest
from pathlib import Path

import safe_ad_sync as sync

URL = "https://raw.githubusercontent.com/vendor/rules/main/module.conf"
SCRIPT = "https://raw.githubusercontent.com/vendor/rules/main/ad.js"
MODULE = """#!name=test
#!desc=仓库更新时间：2026-11-25 10:00
[Rule]
[URL Rewrite]
[Body Rewrite]
[Script]
[MITM]
hostname = api.example.com
"""
BASE = "[Rule]\nDOMAIN,ads.old.example,REJECT\n"


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "Module.sgmodule").write_text(MODULE)
        (self.root / "README.md").write_text("- **最近更新时间：** 2026-11-25 10:00\n- **最近实质更新：** 2026-11-25 10:00\n")
        (self.root / "CHANGELOG.md").write_text(sync.HISTORY_MARKER + "\n<!-- EFFECTIVE_UPDATES_END -->\n")
        self.config = {
            "controlled_sources": [{
                "id": "domains", "url": URL, "enabled": True,
                "allowed_repository": "vendor/rules", "allowed_path": "module.conf",
                "min_exact_rules": 1, "max_exact_rules": 100, "max_source_lines": 1000,
            }],
            "sync_policy": {"max_additions_per_run": 10},
        }
        self.files = {URL: BASE}

    def run_sync(self, check=lambda *args: None):
        return sync.run(self.root, self.config, lambda url: self.files[url],
                        check, stamp="2026-11-25 11:00")

    def test_no_change_does_not_refresh_effective_time(self):
        self.run_sync()
        before = {name: (self.root / name).read_bytes() for name in ["Module.sgmodule", "README.md", "CHANGELOG.md"]}
        result = self.run_sync()
        self.assertEqual(result["status"], "no_upstream_changes")
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content)
        self.assertTrue((self.root / "reports/status.md").exists())

    def test_pending_interfaces_scripts_and_mitm_survive_unchanged_run(self):
        self.files[URL] += "\n[URL Rewrite]\n^https://api.example.com/ads - reject\n[Script]\nad=type=http-response,script-path=https://example.com/ad.js\n[MITM]\nhostname=api.other.example\n"
        self.run_sync()
        first = self.run_sync()
        second = self.run_sync()
        self.assertEqual(first["status"], "review_required")
        self.assertEqual(first["pending"], second["pending"])
        self.assertEqual({x["category"] for x in second["pending"]}, {"URL Rewrite", "Script", "MITM"})

    def test_unreviewed_suffix_and_protected_hosts_are_not_published(self):
        self.files[URL] += "DOMAIN-SUFFIX,ads.unreviewed.example,REJECT\nDOMAIN,ads.jd.com,REJECT\n"
        result = self.run_sync()
        module = (self.root / "Module.sgmodule").read_text()
        self.assertNotIn("ads.unreviewed.example", module)
        self.assertNotIn("ads.jd.com", module)
        self.assertEqual(len(result["pending"]), 2)

    def test_reviewed_suffix_publishes_but_mitm_does_not(self):
        self.config["sync_policy"]["suffix_allowlist"] = ["ads.reviewed.example"]
        self.files[URL] += "DOMAIN-SUFFIX,ads.reviewed.example,REJECT\n[MITM]\nhostname=*.example.com\n"
        result = self.run_sync()
        self.assertIn("DOMAIN-SUFFIX,ads.reviewed.example,REJECT", (self.root / "Module.sgmodule").read_text())
        self.assertNotIn("hostname=*.example.com", (self.root / "Module.sgmodule").read_text())
        self.assertEqual(len(result["pending"]), 1)

    def test_approved_interface_does_not_approve_future_pattern_expansion(self):
        narrow = r"^https:\/\/api\.example\.com\/ads\/ - reject-dict"
        wide = r"^https:\/\/api\.example\.com\/ - reject-dict"
        self.config["sync_policy"]["reviewed_rewrites"] = [{"source": "domains", "upstream": narrow, "publish": narrow}]
        self.files[URL] += "\n[URL Rewrite]\n" + narrow + "\n"
        self.run_sync()
        self.files[URL] = self.files[URL].replace(narrow, wide)
        result = self.run_sync()
        self.assertTrue(any(x["line"] == wide for x in result["pending"]))
        self.assertNotIn("\n" + wide + "\n", (self.root / "Module.sgmodule").read_text())

    def test_fetch_failure_keeps_last_success_and_pending_items(self):
        self.files[URL] += "\n[MITM]\nhostname=another.example\n"
        self.run_sync()
        state_before = json.loads((self.root / "reports/upstream-state.json").read_text())
        module_before = (self.root / "Module.sgmodule").read_bytes()
        del self.files[URL]
        result = self.run_sync()
        self.assertEqual(result["status"], "sync_failed")
        self.assertEqual(len(result["pending"]), 1)
        self.assertEqual((self.root / "Module.sgmodule").read_bytes(), module_before)
        state_after = json.loads((self.root / "reports/upstream-state.json").read_text())
        self.assertEqual(state_before, state_after)

    def test_validation_failure_does_not_publish_or_refresh_metadata(self):
        before = (self.root / "Module.sgmodule").read_bytes()
        def fail(*args):
            raise ValueError("simulated validation failure")
        result = self.run_sync(check=fail)
        self.assertEqual(result["status"], "sync_failed")
        self.assertFalse(result["applied"])
        self.assertEqual((self.root / "Module.sgmodule").read_bytes(), before)
        self.assertIn("simulated validation failure", (self.root / "reports/status.md").read_text())

    def test_removed_local_rule_remains_reviewable_until_resolved(self):
        self.run_sync()
        self.files[URL] = BASE.replace("ads.old", "ads.new")
        self.run_sync()
        result = self.run_sync()
        retired = [x for x in result["pending"] if "上游已删除" in x["reason"]]
        self.assertEqual(len(retired), 1)
        self.assertIn("ads.old.example", (self.root / "Module.sgmodule").read_text())

    def test_script_body_changes_are_detected_even_when_url_is_unchanged(self):
        self.config["upstream_scripts"] = [{"id": "script", "url": SCRIPT, "reviewed_sha256": sync.sha("v1")}]
        self.files[SCRIPT] = "v1"
        self.run_sync()
        self.files[SCRIPT] = "v2"
        result = self.run_sync()
        self.assertEqual(result["status"], "review_required")
        self.assertEqual(len([x for x in result["pending"] if x["category"] == "Script body"]), 1)
        self.assertEqual(self.run_sync()["status"], "review_required")
        self.config["upstream_scripts"][0]["reviewed_sha256"] = sync.sha("v2")
        self.assertEqual(self.run_sync()["status"], "no_upstream_changes")

    def test_batch_limit_defers_without_losing_remaining_candidates(self):
        self.config["sync_policy"]["max_additions_per_run"] = 1
        self.files[URL] += "DOMAIN,ads.next.example,REJECT\n"
        self.assertEqual(len(self.run_sync()["deferred"]), 1)
        self.assertEqual(len(self.run_sync()["applied"]), 1)
        self.assertFalse(self.run_sync()["deferred"])

    def test_invalid_source_shape_is_not_accepted_as_new_baseline(self):
        self.run_sync()
        before = (self.root / "reports/upstream-state.json").read_bytes()
        self.files[URL] = "<html>Bad gateway</html>"
        result = self.run_sync()
        self.assertEqual(result["status"], "sync_failed")
        self.assertEqual((self.root / "reports/upstream-state.json").read_bytes(), before)

    def test_configured_private_or_non_github_urls_are_rejected(self):
        self.config["upstream_scripts"] = [{"id": "invalid", "url": "https://127.0.0.1/private"}]
        with self.assertRaisesRegex(ValueError, "Unapproved upstream"):
            self.run_sync()

    def test_response_rewrites_remain_separate_from_url_rejects(self):
        result = sync.inventory('[Body Rewrite]\n^https://api.example.com/ response-body-replace-regex a b\n[Map Local]\n^https://api.example.com/ data-type=text data="{}"\n')
        self.assertEqual({item['category'] for item in result}, {'Body Rewrite', 'Map Local'})

    def test_rule_option_changes_are_visible_in_the_diff(self):
        self.run_sync()
        self.files[URL] = BASE.replace('REJECT', 'REJECT,extended-matching')
        result = self.run_sync()
        self.assertTrue(result['changes'][0]['added'])
        self.assertTrue(result['changes'][0]['removed'])


if __name__ == "__main__":
    unittest.main()
