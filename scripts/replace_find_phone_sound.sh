#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DECOMPILED_DIR="$ROOT_DIR/work/huawei_health_apktool"
RAW_DIR="$DECOMPILED_DIR/res/raw"
BACKUP_DIR="$ROOT_DIR/backups/find_phone"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <input-audio> [second-audio]"
  echo
  echo "If only one input is provided, it is written to both OGG targets."
  echo "If two inputs are provided, the first replaces zh and the second replaces non-zh."
  exit 1
fi

resolve_target() {
  local numeric_stem="$1"
  local fallback_name="$2"
  local candidate=""

  shopt -s nullglob
  for candidate in     "$RAW_DIR/$numeric_stem"     "$RAW_DIR/$numeric_stem".*     "$RAW_DIR/$fallback_name"     "$RAW_DIR/$fallback_name".*; do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      shopt -u nullglob
      return 0
    fi
  done
  shopt -u nullglob
  return 1
}

TARGET_ZH="$(resolve_target 2131886230 xjm.ogg || true)"
TARGET_INTL="$(resolve_target 2131886231 xjn.ogg || true)"

mkdir -p "$BACKUP_DIR"

if [[ -z "$TARGET_ZH" || -z "$TARGET_INTL" ]]; then
  echo "Find Phone target files are missing. Expected candidates included:" >&2
  echo "  $RAW_DIR/2131886230(.ext) or $RAW_DIR/xjm.ogg" >&2
  echo "  $RAW_DIR/2131886231(.ext) or $RAW_DIR/xjn.ogg" >&2
  echo "Available raw files near expected names:" >&2
  ls -1 "$RAW_DIR" | sort | rg '^(213188623[0-4]|xj[mn]\.ogg|xj[mn])$' >&2 || true
  exit 1
fi

BACKUP_ZH="$BACKUP_DIR/$(basename "$TARGET_ZH").bak"
BACKUP_INTL="$BACKUP_DIR/$(basename "$TARGET_INTL").bak"

cp -f "$TARGET_ZH" "$BACKUP_ZH"
cp -f "$TARGET_INTL" "$BACKUP_INTL"

write_ogg() {
  local input_file="$1"
  local output_file="$2"

  if [[ ! -f "$input_file" ]]; then
    echo "Input file not found: $input_file" >&2
    exit 1
  fi

  case "${input_file##*.}" in
    ogg|OGG)
      cp -f "$input_file" "$output_file"
      ;;
    *)
      if ! command -v ffmpeg >/dev/null 2>&1; then
        echo "ffmpeg is required to convert non-OGG input files." >&2
        exit 1
      fi

      ffmpeg -y -i "$input_file"         -vn         -c:a libvorbis         -q:a 5         "$output_file" >/dev/null 2>&1
      ;;
  esac
}

write_ogg "$1" "$TARGET_ZH"

if [[ $# -eq 2 ]]; then
  write_ogg "$2" "$TARGET_INTL"
else
  write_ogg "$1" "$TARGET_INTL"
fi

echo "Updated:"
echo "  $TARGET_ZH"
echo "  $TARGET_INTL"
echo
echo "Backups:"
echo "  $BACKUP_ZH"
echo "  $BACKUP_INTL"
