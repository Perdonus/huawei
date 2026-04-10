#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

LJA_TARGET = """.method public e()V
    .locals 5

    const-string v0, "Try to kill health enter"

    filled-new-array {v0}, [Ljava/lang/Object;

    move-result-object v0

    .line 87
    const-string v1, "DEVMGR_KillPhoneServiceManager"

    invoke-static {v1, v0}, Lhealth/compact/a/hwlogsmodel/ReleaseLogUtil;->d(Ljava/lang/String;[Ljava/lang/Object;)V

    .line 88
    invoke-static {}, Ldsk;->a()Ldsk;

    move-result-object v0

    sget-object v2, Lcom/huawei/health/devicemgr/api/constant/HwGetDevicesMode;->ALL_DEVICES:Lcom/huawei/health/devicemgr/api/constant/HwGetDevicesMode;

    const/4 v3, 0x0

    .line 89
    const-string/jumbo v4, "killProcessesWhenNoDevices"

    invoke-virtual {v0, v2, v3, v4}, Ldsk;->getDeviceList(Lcom/huawei/health/devicemgr/api/constant/HwGetDevicesMode;Lcom/huawei/health/devicemgr/business/entity/HwGetDevicesParameter;Ljava/lang/String;)Ljava/util/List;

    move-result-object v0

    if-nez v0, :cond_0

    const-string v0, "allDeviceInfoList is null"

    filled-new-array {v0}, [Ljava/lang/Object;

    move-result-object v0

    .line 93
    invoke-static {v1, v0}, Lhealth/compact/a/hwlogsmodel/ReleaseLogUtil;->e(Ljava/lang/String;[Ljava/lang/Object;)V

    .line 94
    invoke-direct {p0}, Llja;->i()V

    return-void

    .line 98
    :cond_0
    invoke-interface {v0}, Ljava/util/List;->isEmpty()Z

    move-result v0

    if-nez v0, :cond_1

    .line 100
    invoke-direct {p0}, Llja;->j()V

    return-void

    .line 104
    :cond_1
    invoke-direct {p0}, Llja;->d()Z

    move-result v0

    if-nez v0, :cond_2

    invoke-static {}, Lcom/huawei/haf/common/utils/ScreenUtil;->c()Z

    move-result v0

    if-nez v0, :cond_2

    .line 106
    invoke-direct {p0}, Llja;->b()V

    goto :goto_0

    .line 109
    :cond_2
    invoke-direct {p0}, Llja;->i()V

    :goto_0
    return-void
.end method
"""

LJA_REPLACEMENT = """.method public e()V
    .locals 2

    const-string v0, "Skip kill health during pairing"

    filled-new-array {v0}, [Ljava/lang/Object;

    move-result-object v0

    .line 87
    const-string v1, "DEVMGR_KillPhoneServiceManager"

    invoke-static {v1, v0}, Lhealth/compact/a/hwlogsmodel/ReleaseLogUtil;->d(Ljava/lang/String;[Ljava/lang/Object;)V

    return-void
.end method
"""

CFY_PATCHES = (
    (
        """.field private i:Lxym;

.field private j:[B

.field private l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

.field private n:Z
""",
        """.field private i:Lxym;

.field private j:[B

.field private k:Z

.field private l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

.field private m:Z

.field private n:Z
""",
        "cfy fields",
    ),
    (
        """    const/4 v0, 0x0

    .line 63
    iput-boolean v0, p0, Lcfy;->n:Z

    .line 117
    iput-object p2, p0, Lcfy;->f:Ljava/lang/String;
""",
        """    const/4 v0, 0x0

    .line 63
    iput-boolean v0, p0, Lcfy;->n:Z

    .line 64
    iput-boolean v0, p0, Lcfy;->k:Z

    .line 65
    iput-boolean v0, p0, Lcfy;->m:Z

    .line 117
    iput-object p2, p0, Lcfy;->f:Ljava/lang/String;
""",
        "cfy constructor retry flags",
    ),
    (
        """    invoke-virtual {v0, v1}, Lcfn;->c(Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;)V

    return-object v0
.end method

.method private m()V
""",
        """    invoke-virtual {v0, v1}, Lcfn;->c(Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;)V

    return-object v0
.end method

.method private k()V
    .locals 1

    const/4 v0, 0x0

    .line 478
    iput-boolean v0, p0, Lcfy;->k:Z

    .line 479
    iput-boolean v0, p0, Lcfy;->m:Z

    return-void
.end method

.method private l()Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;
    .locals 4

    .line 482
    iget-boolean v0, p0, Lcfy;->k:Z

    const/4 v1, 0x0

    if-nez v0, :cond_0

    return-object v1

    :cond_0
    iput-boolean v1, p0, Lcfy;->k:Z

    .line 486
    iget-boolean v0, p0, Lcfy;->m:Z

    if-eqz v0, :cond_1

    const-string v0, "retry after HiChain error already used"

    filled-new-array {v0}, [Ljava/lang/Object;

    move-result-object v0

    .line 487
    const-string v2, "HiChain3Client"

    invoke-static {v2, v0}, Lhealth/compact/a/LogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    return-object v1

    :cond_1
    const/4 v0, 0x1

    .line 491
    iput-boolean v0, p0, Lcfy;->m:Z

    const-string v2, "retry auth after HiChain error 42"

    filled-new-array {v2}, [Ljava/lang/Object;

    move-result-object v2

    .line 492
    const-string v3, "DEVMGR_HiChain3Client"

    invoke-static {v3, v2}, Lhealth/compact/a/ReleaseLogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    .line 493
    invoke-static {}, Lcfw;->c()Lcfw;

    move-result-object v2

    iget-object v3, p0, Lcfy;->c:Ljava/lang/String;

    iget-boolean v0, p0, Lcfy;->n:Z

    invoke-virtual {v2, v3, v0}, Lcfw;->f(Ljava/lang/String;Z)Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    move-result-object v0

    if-nez v0, :cond_2

    const-string v2, "retry auth command is null"

    filled-new-array {v2}, [Ljava/lang/Object;

    move-result-object v2

    .line 494
    const-string v3, "DEVMGR_HiChain3Client"

    invoke-static {v3, v2}, Lhealth/compact/a/ReleaseLogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    :cond_2
    return-object v0
.end method

.method private m()V
""",
        "cfy retry helpers",
    ),
    (
        """    .line 440
    invoke-direct {p0}, Lcfy;->m()V

    .line 441
    iget-object p1, p0, Lcfy;->l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    if-nez p1, :cond_1

    iget-boolean p1, p0, Lcfy;->h:Z

    if-eqz p1, :cond_2

    :cond_1
    const/4 p1, 0x1

    .line 442
    invoke-virtual {v0, p1}, Lcfn;->e(Z)V

    .line 444
    :cond_2
    iget-object p1, p0, Lcfy;->l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    invoke-virtual {v0, p1}, Lcfn;->c(Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;)V
""",
        """    .line 440
    invoke-direct {p0}, Lcfy;->m()V

    .line 441
    invoke-direct {p0}, Lcfy;->l()Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    move-result-object p1

    if-eqz p1, :cond_1

    .line 442
    iput-object p1, p0, Lcfy;->l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    .line 444
    :cond_1
    iget-object p1, p0, Lcfy;->l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    if-nez p1, :cond_2

    iget-boolean p1, p0, Lcfy;->h:Z

    if-eqz p1, :cond_3

    :cond_2
    const/4 p1, 0x1

    .line 445
    invoke-virtual {v0, p1}, Lcfn;->e(Z)V

    .line 447
    :cond_3
    iget-object p1, p0, Lcfy;->l:Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    invoke-virtual {v0, p1}, Lcfn;->c(Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;)V
""",
        "cfy auth retry injection",
    ),
    (
        """.method public c()Lcfn;
    .locals 3

    const/4 v0, 0x1

    .line 408
    invoke-virtual {p0, v0}, Lcfy;->c(Z)V
""",
        """.method public c()Lcfn;
    .locals 3

    const/4 v0, 0x1

    .line 408
    invoke-direct {p0}, Lcfy;->k()V

    .line 409
    invoke-virtual {p0, v0}, Lcfy;->c(Z)V
""",
        "cfy reset retry flags",
    ),
    (
        """    return-object v1
.end method

.method public c(Z)V
""",
        """    return-object v1
.end method

.method public e(Z)V
    .locals 0

    .line 418
    iput-boolean p1, p0, Lcfy;->k:Z

    return-void
.end method

.method public c(Z)V
""",
        "cfy retry flag setter",
    ),
)

CFYE_PATCHES = (
    (
        """    .line 216
    const-string v0, "DEVMGR_HiChain3Client"

    invoke-static {v0, p5}, Lhealth/compact/a/ReleaseLogUtil;->e(Ljava/lang/String;[Ljava/lang/Object;)V

    .line 218
""",
        """    .line 216
    const-string v0, "DEVMGR_HiChain3Client"

    invoke-static {v0, p5}, Lhealth/compact/a/ReleaseLogUtil;->e(Ljava/lang/String;[Ljava/lang/Object;)V

    move v7, p4

    move v8, p3

    .line 218
""",
        "cfy$e preserve error code",
    ),
    (
        """    .line 230
    :cond_1
    iget-object p1, p0, Lcfy$e;->b:Lcfy;

    invoke-static {p1}, Lcfy;->c(Lcfy;)V

    return-void
.end method
""",
        """    .line 230
    :cond_1
    const/16 p1, 0x2a

    if-ne v7, p1, :cond_2

    const/4 p1, 0x2

    if-ne v8, p1, :cond_2

    iget-object p1, p0, Lcfy$e;->b:Lcfy;

    const/4 p2, 0x1

    invoke-virtual {p1, p2}, Lcfy;->e(Z)V

    :cond_2
    iget-object p1, p0, Lcfy$e;->b:Lcfy;

    invoke-static {p1}, Lcfy;->c(Lcfy;)V

    return-void
.end method
""",
        "cfy$e schedule retry",
    ),
)

CFW_PATCHES = (
    (
        """    invoke-virtual {p1, v0, v1, v2, v3}, Lcfv;->c(Ljava/lang/String;Lxyi;Ljava/util/concurrent/ConcurrentHashMap;Ljava/util/concurrent/ConcurrentHashMap;)Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    move-result-object p1

    return-object p1
.end method

.method public d()V
""",
        """    invoke-virtual {p1, v0, v1, v2, v3}, Lcfv;->c(Ljava/lang/String;Lxyi;Ljava/util/concurrent/ConcurrentHashMap;Ljava/util/concurrent/ConcurrentHashMap;)Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    move-result-object p1

    return-object p1
.end method

.method public f(Ljava/lang/String;Z)Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;
    .locals 6

    const/4 v0, 0x0

    .line 601
    invoke-static {p1}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v1

    if-eqz v1, :cond_0

    const-string p1, "retryHiChainAuth valid"

    filled-new-array {p1}, [Ljava/lang/Object;

    move-result-object p1

    const-string p2, "HiChain3GroupManager"

    invoke-static {p2, p1}, Lhealth/compact/a/LogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    return-object v0

    :cond_0
    iget-object v1, p0, Lcfw;->f:Ljava/lang/String;

    .line 606
    invoke-static {v1}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_1

    const-string v1, "retryHiChainAuth mGroupId is empty, use mBackUpGroupId"

    filled-new-array {v1}, [Ljava/lang/Object;

    move-result-object v1

    const-string v2, "DEVMGR_HiChain3GroupManager"

    invoke-static {v2, v1}, Lhealth/compact/a/ReleaseLogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    iget-object v1, p0, Lcfw;->d:Ljava/lang/String;

    :cond_1
    invoke-static {v1}, Landroid/text/TextUtils;->isEmpty(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_2

    const-string p1, "retryHiChainAuth groupId is empty"

    filled-new-array {p1}, [Ljava/lang/Object;

    move-result-object p1

    const-string p2, "HiChain3GroupManager"

    invoke-static {p2, p1}, Lhealth/compact/a/LogUtil;->c(Ljava/lang/String;[Ljava/lang/Object;)V

    return-object v0

    :cond_2
    new-instance v2, Lcfv;

    invoke-direct {v2}, Lcfv;-><init>()V

    .line 617
    invoke-virtual {v2, p1}, Lcfv;->a(Ljava/lang/String;)V

    .line 618
    new-instance v3, Lcfy;

    invoke-direct {v3, p1, v1}, Lcfy;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    .line 619
    invoke-virtual {v3, p2}, Lcfy;->c(Z)V

    .line 620
    invoke-virtual {v2, v3}, Lcfv;->b(Lcfy;)V

    .line 621
    iget-object v3, p0, Lcfw;->e:Ljava/util/concurrent/ConcurrentHashMap;

    invoke-virtual {v3, p1, v2}, Ljava/util/concurrent/ConcurrentHashMap;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v3

    const-string v3, "retryHiChainAuth reset client ,"

    invoke-static {p1}, Lcii;->c(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    filled-new-array {v3, v4}, [Ljava/lang/Object;

    move-result-object v3

    .line 623
    const-string v4, "HiChain3GroupManager"

    invoke-static {v4, v3}, Lhealth/compact/a/LogUtil;->e(Ljava/lang/String;[Ljava/lang/Object;)V

    .line 624
    iget-object v3, p0, Lcfw;->i:Lxyi;

    iget-object v4, p0, Lcfw;->j:Ljava/util/concurrent/ConcurrentHashMap;

    iget-object v5, p0, Lcfw;->e:Ljava/util/concurrent/ConcurrentHashMap;

    invoke-virtual {v2, v1, v3, v4, v5}, Lcfv;->c(Ljava/lang/String;Lxyi;Ljava/util/concurrent/ConcurrentHashMap;Ljava/util/concurrent/ConcurrentHashMap;)Lcom/huawei/devicesdk/connect/handshake/HandshakeCommandBase;

    move-result-object p1

    return-object p1
.end method

.method public d()V
""",
        "cfw retry helper",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Patch Huawei Health pairing smali for HiChain retry and PhoneService stability."
    )
    parser.add_argument("lja_smali", type=Path)
    parser.add_argument("cfw_smali", type=Path)
    parser.add_argument("cfy_smali", type=Path)
    parser.add_argument("cfy_error_smali", type=Path)
    return parser.parse_args()


def ensure_file(path: Path) -> None:
    if not path.is_file():
        print(f"Smali file not found: {path}", file=sys.stderr)
        raise SystemExit(1)


def apply_patch(text: str, target: str, replacement: str, label: str, path: Path) -> str:
    if replacement in text:
        print(f"{label} already present in {path}")
        return text

    occurrences = text.count(target)
    if occurrences != 1:
        print(
            f"Expected exactly one target snippet for {label} in {path}, found {occurrences}.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(f"Patched {label} in {path}")
    return text.replace(target, replacement, 1)


def patch_file(path: Path, patches: tuple[tuple[str, str, str], ...]) -> None:
    ensure_file(path)
    text = path.read_text(encoding="utf-8")
    for target, replacement, label in patches:
        text = apply_patch(text, target, replacement, label, path)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    patch_file(args.lja_smali, ((LJA_TARGET, LJA_REPLACEMENT, "KillPhoneServiceManager no-op"),))
    patch_file(args.cfw_smali, CFW_PATCHES)
    patch_file(args.cfy_smali, CFY_PATCHES)
    patch_file(args.cfy_error_smali, CFYE_PATCHES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
