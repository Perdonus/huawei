#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PATCH_SCRIPT="$ROOT_DIR/scripts/patch_find_phone_apk.py"

if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo "Usage: $0 <source-apk> <output-apk> <input-audio> [second-audio]"
  echo
  echo "If only one input audio is provided, it is written to both OGG targets."
  echo "If two input audios are provided, the first replaces zh and the second replaces non-zh."
  exit 1
fi

SOURCE_APK="$1"
OUTPUT_APK="$2"
INPUT_ZH="$3"
INPUT_INTL="${4:-$3}"
TMP_DIR="$(mktemp -d)"
TMP_ZH="$TMP_DIR/find_phone_zh.ogg"
TMP_INTL="$TMP_DIR/find_phone_intl.ogg"

trap 'rm -rf "$TMP_DIR"' EXIT

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

if [[ ! -f "$SOURCE_APK" ]]; then
  echo "Source APK not found: $SOURCE_APK" >&2
  exit 1
fi

if [[ ! -f "$PATCH_SCRIPT" ]]; then
  echo "Patch script not found: $PATCH_SCRIPT" >&2
  exit 1
fi

write_ogg "$INPUT_ZH" "$TMP_ZH"
write_ogg "$INPUT_INTL" "$TMP_INTL"

python3 "$PATCH_SCRIPT" \
  --source-apk "$SOURCE_APK" \
  --output-apk "$OUTPUT_APK" \
  --zh-audio "$TMP_ZH" \
  --intl-audio "$TMP_INTL"
