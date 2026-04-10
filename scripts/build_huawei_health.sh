#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DECOMPILED_DIR="$ROOT_DIR/work/huawei_health_apktool"
OUTPUT_DIR="$ROOT_DIR/build"
OUTPUT_APK="$OUTPUT_DIR/com.huawei.health-16.1.2.310-rebuilt-unsigned.apk"

mkdir -p "$OUTPUT_DIR"

apktool b "$DECOMPILED_DIR" -o "$OUTPUT_APK"

echo "Built:"
echo "  $OUTPUT_APK"
