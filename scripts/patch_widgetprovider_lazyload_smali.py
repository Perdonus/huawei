#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


TARGET_SNIPPET = """    .line 60
    invoke-direct {p0}, Lhealth/compact/a/HealthApplicationLazyLoadMgr;->c()V

    .line 63
    invoke-static {}, Lhealth/compact/a/KeyManager;->c()V

    .line 66
    new-instance v0, Lhealth/compact/a/LogApiImpl;
"""

REPLACEMENT_SNIPPET = """    .line 60
    invoke-direct {p0}, Lhealth/compact/a/HealthApplicationLazyLoadMgr;->c()V

    const-string v0, "com.huawei.health:widgetProvider"

    invoke-static {v0}, Lhealth/compact/a/ProcessUtil;->c(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_skip_widgetprovider_keymanager

    .line 63
    invoke-static {}, Lhealth/compact/a/KeyManager;->c()V

    :cond_skip_widgetprovider_keymanager
    .line 66
    new-instance v0, Lhealth/compact/a/LogApiImpl;
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Skip KeyManager lazy-load only inside com.huawei.health:widgetProvider."
    )
    parser.add_argument("smali_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    smali_path = args.smali_path

    if not smali_path.is_file():
        print(f"Smali file not found: {smali_path}", file=sys.stderr)
        return 1

    source_text = smali_path.read_text(encoding="utf-8")

    if REPLACEMENT_SNIPPET in source_text:
        print(f"WidgetProvider KeyManager guard already present in {smali_path}")
        return 0

    occurrences = source_text.count(TARGET_SNIPPET)
    if occurrences != 1:
        print(
            f"Expected exactly one target snippet in {smali_path}, found {occurrences}.",
            file=sys.stderr,
        )
        return 1

    smali_path.write_text(
        source_text.replace(TARGET_SNIPPET, REPLACEMENT_SNIPPET),
        encoding="utf-8",
    )
    print(f"Patched widgetProvider lazy-load guard in {smali_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
