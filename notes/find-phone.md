# Huawei Health Find Phone Notes

Repository: `git@github.com:Perdonus/huawei.git`

Build/verification policy:
- Use GitHub Actions only for APK patching, alignment, signing, and verification.
- Do not rely on local rebuild or verification loops.

Original APK:
- `input/original/com.huawei.health-16.1.2.310.apk`
- SHA-256: `5b7d162abfd2979108672c2b11b063f0c848f4fe60070f41df2e8e26464e54b8`

Decompiled tree:
- `work/huawei_health_apktool/`

## Find Phone entry point

The phone-finder logic is implemented in:

- `work/huawei_health_apktool/smali/ljo.smali`

This class logs itself as `HwFindPhoneMgr`.

Relevant methods:

- `private c()V`
  - Starts playback (`startPlayRing`)
  - Creates `MediaPlayer`
  - Sets looping to `true`
  - Starts playback
- `private e()V`
  - Handles `startFindPhone`
- `private f()V`
  - Handles `stopFindPhone`
- `public b([B)V`
  - Handles the watch operation report
  - Operation `1` -> start
  - Operation `2` -> stop

## Audio resources used by Find Phone

Inside `ljo.smali`, `MediaPlayer.create(...)` selects one of two OGG files:

- `0x7f120096` -> `work/huawei_health_apktool/res/raw/2131886230.ogg`
- `0x7f120097` -> `work/huawei_health_apktool/res/raw/2131886231.ogg`

Selection logic:

- Locale language `zh` -> `2131886230.ogg`
- Any other language -> `2131886231.ogg`

Current file sizes:

- `2131886230.ogg` -> about `122K`
- `2131886231.ogg` -> about `124K`

## Replacement strategy

The reliable path for this APK is to patch the original archive directly instead of rebuilding with apktool.

Replace both Find Phone resources in the original APK:

- `res/raw/xjm.ogg`
- `res/raw/xjn.ogg`

Fallback names seen in older apktool output:

- `res/raw/2131886230.ogg`
- `res/raw/2131886231.ogg`

Using the same audio for both is the simplest path unless separate Chinese/non-Chinese sounds are needed.

After patching the archive:

- align with `zipalign`
- sign with `apksigner`
- verify on GitHub Actions
