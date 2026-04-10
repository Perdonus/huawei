#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/build"
INPUT_APK="${1:-$ROOT_DIR/input/original/com.huawei.health-16.1.2.310.apk}"
INPUT_ZH_AUDIO="${2:-$ROOT_DIR/assets/custom/find_phone.ogg}"
INPUT_INTL_AUDIO="${3:-$INPUT_ZH_AUDIO}"
OUTPUT_APK="$OUTPUT_DIR/com.huawei.health-16.1.2.310-rebuilt-unsigned.apk"

mkdir -p "$OUTPUT_DIR"

bash "$ROOT_DIR/scripts/replace_find_phone_sound.sh" \
  "$INPUT_APK" \
  "$OUTPUT_APK" \
  "$INPUT_ZH_AUDIO" \
  "$INPUT_INTL_AUDIO"

echo "Built:"
echo "  $OUTPUT_APK"
