#!/usr/bin/env python3
# encoding: utf-8

import os
import sys


def run() -> None:
    KSU: str = input("Choose KernelSU Variant (NONE, NEXT, SUKI, RKSU): ").upper()
    SUSFS: str = str(
        input("Apply SUSFS patch (Required KSU != NONE) (Y/n): ").lower() == "y"
    ).lower()
    LXC: str = str(input("Apply LXC patch (Y/n): ").lower() == "y").lower()

    if KSU == "NONE" and SUSFS == "true":
        from kernel_builder.utils.log import log

        log("SUSFS required KernelSU != NONE", "error")
        sys.exit(-1)

    os.environ["KSU"] = KSU
    os.environ["SUSFS"] = SUSFS
    os.environ["LXC"] = LXC
    os.environ["LOCAL_RUN"] = "true"

    from kernel_builder.main import KernelBuilder

    KernelBuilder().run_build()


if __name__ == "__main__":
    run()
