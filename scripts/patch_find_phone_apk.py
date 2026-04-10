#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZipInfo


ENTRY_CANDIDATES = {
    "zh": ("res/raw/xjm.ogg", "res/raw/2131886230.ogg"),
    "intl": ("res/raw/xjn.ogg", "res/raw/2131886231.ogg"),
}

SIGNATURE_SUFFIXES = (".RSA", ".DSA", ".EC", ".SF")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Patch Huawei Health Find Phone sounds directly inside an APK archive."
    )
    parser.add_argument("--source-apk", required=True, type=Path)
    parser.add_argument("--output-apk", required=True, type=Path)
    parser.add_argument("--zh-audio", required=True, type=Path)
    parser.add_argument("--intl-audio", required=True, type=Path)
    return parser.parse_args()


def is_signature_entry(entry_name: str) -> bool:
    upper_name = entry_name.upper()
    if not upper_name.startswith("META-INF/"):
        return False

    base_name = upper_name.rsplit("/", 1)[-1]
    return base_name == "MANIFEST.MF" or base_name.endswith(SIGNATURE_SUFFIXES)


def build_output_info(source_info: ZipInfo) -> ZipInfo:
    info = ZipInfo(filename=source_info.filename, date_time=source_info.date_time)
    info.compress_type = source_info.compress_type
    info.comment = source_info.comment
    info.extra = source_info.extra
    info.create_system = source_info.create_system
    info.internal_attr = source_info.internal_attr
    info.external_attr = source_info.external_attr
    return info


def resolve_targets(entry_names: set[str]) -> dict[str, str]:
    resolved: dict[str, str] = {}
    missing_targets: list[str] = []

    for locale_key, candidates in ENTRY_CANDIDATES.items():
        for candidate in candidates:
            if candidate in entry_names:
                resolved[candidate] = locale_key
                break
        else:
            missing_targets.append(f"{locale_key}: {', '.join(candidates)}")

    if missing_targets:
        print("Missing Find Phone audio targets in APK:", file=sys.stderr)
        for item in missing_targets:
            print(f"  {item}", file=sys.stderr)

        nearby = sorted(
            name
            for name in entry_names
            if name.startswith("res/raw/")
            and (
                "xjm" in name
                or "xjn" in name
                or "2131886230" in name
                or "2131886231" in name
            )
        )
        if nearby:
            print("Nearby matching entries:", file=sys.stderr)
            for item in nearby:
                print(f"  {item}", file=sys.stderr)

        raise SystemExit(1)

    return resolved


def main() -> int:
    args = parse_args()

    if not args.source_apk.is_file():
        print(f"Source APK not found: {args.source_apk}", file=sys.stderr)
        return 1

    if not args.zh_audio.is_file():
        print(f"Chinese replacement audio not found: {args.zh_audio}", file=sys.stderr)
        return 1

    if not args.intl_audio.is_file():
        print(f"International replacement audio not found: {args.intl_audio}", file=sys.stderr)
        return 1

    zh_bytes = args.zh_audio.read_bytes()
    intl_bytes = args.intl_audio.read_bytes()

    args.output_apk.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(args.source_apk, "r") as source_zip:
        entry_names = set(source_zip.namelist())
        replacements = resolve_targets(entry_names)
        replaced_entries: list[str] = []
        stripped_entries: list[str] = []

        with tempfile.NamedTemporaryFile(
            prefix=f"{args.output_apk.name}.",
            suffix=".tmp",
            dir=args.output_apk.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            with ZipFile(temp_path, "w") as output_zip:
                for source_info in source_zip.infolist():
                    if is_signature_entry(source_info.filename):
                        stripped_entries.append(source_info.filename)
                        continue

                    if source_info.filename in replacements:
                        locale_key = replacements[source_info.filename]
                        payload = zh_bytes if locale_key == "zh" else intl_bytes
                        replaced_entries.append(source_info.filename)
                    else:
                        payload = source_zip.read(source_info.filename)

                    output_zip.writestr(build_output_info(source_info), payload)

            temp_path.replace(args.output_apk)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

    print("Patched APK:")
    print(f"  source: {args.source_apk}")
    print(f"  output: {args.output_apk}")
    print()
    print("Updated entries:")
    for entry in replaced_entries:
        print(f"  {entry}")
    print()
    print("Stripped old signature entries:")
    if stripped_entries:
        for entry in stripped_entries:
            print(f"  {entry}")
    else:
        print("  none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
