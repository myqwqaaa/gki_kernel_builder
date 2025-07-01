import os
import re

from os import cpu_count
from subprocess import CompletedProcess
from pathlib import Path
from dataclasses import dataclass, field
from src.config.config import WORKSPACE, DEFCONFIG
from src.utils.shell import Shell
from src.utils.log import log
from typing import ClassVar, TypeAlias

Proc: TypeAlias = CompletedProcess[bytes]


@dataclass(slots=True)
class Builder:
    shell: Shell = field(default_factory=Shell)

    workspace: ClassVar[Path] = WORKSPACE
    jobs: int = field(default_factory=lambda: cpu_count() or 1)
    defconfig: ClassVar[str] = DEFCONFIG
    ksu: str = field(default_factory=lambda: os.getenv("KSU", ""))
    susfs: bool = field(
        default_factory=lambda: os.getenv("SUSFS", "false").lower() == "true"
    )

    def _make(
        self, args: list[str] | None = None, *, jobs: int, out: str | Path
    ) -> Proc:
        return self.shell.run(
            [
                "make",
                f"-j{jobs}",
                "CC=ccache clang",
                "CXX=ccache clang++",
                *(args or []),
                f"O={out}",
            ]
        )

    def config(self, conf: str, mode: bool, config_path: Path | None = None) -> Proc:
        _config: Path = self.workspace / "scripts" / "config"
        target: Path = config_path or (self.workspace / "out" / ".config")
        cmd = [
            str(_config),
            "--file",
            str(target),
            "--enable" if mode else "--disable",
            conf,
        ]
        log(f"{'Enabling' if mode else 'Disabling'} config: {conf} (file={target})")
        return self.shell.run(cmd)

    def _ksu_configurator(self) -> None:
        self.config("CONFIG_KSU", mode=True)

        # Enable Manual Hook
        self.config("CONFIG_KSU_MANUAL_HOOK", True)
        self.config("CONFIG_KSU_KPROBES_HOOK", False)

        # Enable KPM support for SukiSU
        if self.ksu == "SUKI":
            self.config("CONFIG_KPM", True)

        # Config SUSFS
        if self.susfs:
            self.config("CONFIG_KSU_SUSFS", True)
            self.config("CONFIG_KSU_SUSFS_SUS_SU", False)
        else:
            self.config("CONFIG_KSU_SUSFS", False)

    def build(
        self,
        jobs: int | None = None,
        *,
        out: str | Path = "out",
    ) -> None:
        log(
            f"Start build: defconfig={self.defconfig}, out={out}, jobs={jobs or self.jobs}"
        )
        self._make([self.defconfig], jobs=(jobs or self.jobs), out=out)

        if self.ksu != "NONE":
            self._ksu_configurator()
            log("Making oldefconfig")
            self.shell.run(["make", "olddefconfig", f"O={out}"])

        log("Defconfig completed. Starting full build.")
        self._make(jobs=(jobs or self.jobs), out=out)
        log("Build completed successfully.")

    def get_kernel_version(self) -> str | None:
        log("Fetching kernel version...")
        makefile: str = (self.workspace / "Makefile").read_text()
        version = re.findall(
            r"^(?:VERSION|PATCHLEVEL|SUBLEVEL)\s*=\s*(\d+)$", makefile, re.MULTILINE
        )
        return ".".join(version[:3]) if version else None


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
