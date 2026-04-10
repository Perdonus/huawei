#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DECOMPILED_DIR="$ROOT_DIR/work/huawei_health_apktool"
RAW_DIR="$DECOMPILED_DIR/res/raw"
BACKUP_DIR="$ROOT_DIR/backups/find_phone"

TARGET_ZH="$RAW_DIR/2131886230.ogg"
TARGET_INTL="$RAW_DIR/2131886231.ogg"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <input-audio> [second-audio]"
  echo
  echo "If only one input is provided, it is written to both OGG targets."
  echo "If two inputs are provided, the first replaces zh and the second replaces non-zh."
  exit 1
fi

mkdir -p "$BACKUP_DIR"

if [[ ! -f "$TARGET_ZH" || ! -f "$TARGET_INTL" ]]; then
  echo "Find Phone target files are missing. Expected:" >&2
  echo "  $TARGET_ZH" >&2
  echo "  $TARGET_INTL" >&2
  exit 1
fi

cp -f "$TARGET_ZH" "$BACKUP_DIR/2131886230.ogg.bak"
cp -f "$TARGET_INTL" "$BACKUP_DIR/2131886231.ogg.bak"

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

      ffmpeg -y -i "$input_file" \
        -vn \
        -c:a libvorbis \
        -q:a 5 \
        "$output_file" >/dev/null 2>&1
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
echo "  $BACKUP_DIR/2131886230.ogg.bak"
echo "  $BACKUP_DIR/2131886231.ogg.bak"
