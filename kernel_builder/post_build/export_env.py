import os
import sh
import re
from sh import Command, head, sed
from datetime import datetime, timezone
from kernel_builder.utils.env import susfs_enabled
from kernel_builder.config.config import OUTPUT, TOOLCHAIN, WORKSPACE
from kernel_builder.utils.build import Builder
from kernel_builder.pre_build.variants import Variants


class GithubExportEnv:
    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.variants: Variants = Variants()

    def _write_env(self, env_map: dict[str, str]) -> None:
        output_path = os.environ.get("GITHUB_OUTPUT")
        if not output_path:
            raise RuntimeError("GITHUB_OUTPUT is not set")

        with open(output_path, "a") as f:
            for k, v in env_map.items():
                k, v = k.strip(), v.strip()
                f.write(f"{k}={v}\n")

    def export_github_env(self) -> None:
        clang: Command = sh.Command(str(TOOLCHAIN / "clang" / "bin" / "clang"))
        raw_toolchain = head("-n", "1", _in=clang("-v", _err_to_out=True))
        toolchain: str = str(
            sed("s/(https..*//; s/ version//", _in=raw_toolchain)
        ).strip()

        susfs_version: str | None = (
            re.search(
                r"v\d+\.\d+\.\d+",
                (WORKSPACE / "include" / "linux" / "susfs.h").read_text(),
            ).group()  # pyright: ignore[reportOptionalMemberAccess]
            if susfs_enabled()
            else None
        )

        now: datetime = datetime.now(timezone.utc)
        current_time: str = now.strftime("%a %b %d %H:%M:%S %Y")

        env_map: dict[str, str] = {
            "output": str(OUTPUT),
            "version": self.builder.get_kernel_version(),
            "variant": self.variants.suffix,
            "susfs_version": susfs_version or "Disabled",
            "toolchain": toolchain,
            "build_time": current_time,
        }
        self._write_env(env_map)
