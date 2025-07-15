from kernel_builder.pre_build.ksu import KSUInstaller
from kernel_builder.pre_build.lxc import LXCPatcher
from kernel_builder.pre_build.susfs import SUSFSPatcher
from kernel_builder.utils import env
from kernel_builder.utils.log import log
from dataclasses import dataclass, field


@dataclass(slots=True)
class Variants:
    ksu: KSUInstaller = KSUInstaller()
    susfs: SUSFSPatcher = SUSFSPatcher()
    lxc: LXCPatcher = LXCPatcher()

    ksu_variant: str = field(default_factory=env.ksu_variant)
    use_lxc: bool = field(default_factory=env.lxc_enabled)
    use_susfs: bool = field(default_factory=env.susfs_enabled)

    @property
    def variant_name(self) -> list[str]:
        result: list[str] = []
        k: str = self.ksu_variant.upper()

        if k == "NONE":
            result = ["Non-KSU"]
        elif k == "NEXT":
            result = ["KSUN"]
        elif k == "SUKI":
            result = ["SUKISU"]
        else:
            log(f"Unknown KernelSU variant {self.ksu!r}", "error")
            return ["UNKNOWN"]

        if self.use_susfs:
            result.append("SUSFS")

        if self.use_lxc:
            result.append("LXC")
        return result

    @property
    def suffix(self) -> str:
        return f"-{'-'.join(self.variant_name)}" if self.variant_name else "-UNKNOWN"

    def setup(self) -> None:
        self.ksu.install()
        self.susfs.apply()
        self.lxc.apply()


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
