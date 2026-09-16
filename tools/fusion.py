#!/usr/bin/env python3
"""Validate the connectivity-safe Shadowrocket module.

The module is intentionally local-only. Automated maintenance must never add
scripts, URL rewrites, MITM hosts, remote rule sets, or broad keyword rules.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "Module.sgmodule"
STATUS = ROOT / "reports" / "status.md"

FORBIDDEN_SECTIONS = {"script", "url rewrite", "body rewrite", "mitm", "map local"}
FORBIDDEN_TOKENS = (
    "script-path",
    "rule-set,",
    "domain-keyword,",
    "url-regex,",
    "pangolin-sdk-toutiao",
    "wxs.qq.com",
    "httpdns",
    "googlevideo.com",
    "youtube.com",
    "pan.baidu.com",
)


def active_lines(text: str):
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line and not line.startswith("#"):
            yield number, line


def validate(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    rules: list[str] = []
    section = ""

    for number, line in active_lines(text):
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            if section in FORBIDDEN_SECTIONS:
                errors.append(f"line {number}: forbidden section [{section}]")
            continue

        lowered = line.lower().replace(" ", "")
        hit = next((token for token in FORBIDDEN_TOKENS if token in lowered), None)
        if hit:
            errors.append(f"line {number}: forbidden token {hit}")

        if section == "rule":
            if not line.upper().startswith("DOMAIN,"):
                errors.append(f"line {number}: only exact DOMAIN rules are allowed")
            else:
                rules.append(line)
        else:
            errors.append(f"line {number}: active content outside [Rule]")

    duplicates = [rule for rule, count in Counter(rules).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate rules: {len(duplicates)}")
    if not rules:
        errors.append("no active rules")
    return errors, rules


def main() -> None:
    if not MODULE.exists():
        raise SystemExit("Module.sgmodule is missing")

    text = MODULE.read_text("utf-8")
    errors, rules = validate(text)
    if errors:
        raise SystemExit("Unsafe module:\n- " + "\n- ".join(errors))

    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(
        "\n".join(
            [
                "# Fusion Personal health",
                "",
                "- Mode: **connectivity-safe / local-only**",
                f"- Exact DOMAIN reject rules: **{len(rules)}**",
                "- Remote dependencies: **0**",
                "- Script declarations: **0**",
                "- URL rewrites: **0**",
                "- MITM hosts: **0**",
                "- Broad DOMAIN-KEYWORD rules: **0**",
                "- Validation: **PASS**",
                "",
                "> Automation only validates the module. It does not import upstream rules.",
                "> YouTube, WeChat, and Baidu Netdisk traffic is not decrypted or rewritten.",
                "",
            ]
        ),
        "utf-8",
    )
    print(f"Validation passed: {len(rules)} exact DOMAIN rules")


if __name__ == "__main__":
    main()
