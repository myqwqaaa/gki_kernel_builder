import os

from src.utils.log import log
from dataclasses import dataclass, field


@dataclass(slots=True)
class Variants:
    ksu: str = field(default_factory=lambda: os.getenv("KSU", "NONE"))
    use_lxc: bool = field(
        default_factory=lambda: os.getenv("LXC", "false").lower() == "true"
    )

    @property
    def variant_name(self) -> list[str]:
        result: list[str] = []
        k: str = self.ksu.upper()

        if k == "NONE":
            result = ["non-ksu"]
        elif k == "NEXT":
            result = ["ksu-next"]
        elif k == "SUKI":
            result = ["sukisu"]
        else:
            log(f"Unknown KernelSU variant {self.ksu!r}", "error")
            return ["unknown"]

        if self.use_lxc:
            result.append("lxc")
        return result

    @property
    def suffix(self) -> str:
        return f"-{'-'.join(self.variant_name)}" if self.variant_name else "-unknown"
