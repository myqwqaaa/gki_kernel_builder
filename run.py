import os
from src.main import KernelBuilder


def run() -> None:
    KSU: str = input("Choose KernelSU Variant (NONE, NEXT, SUKI): ").upper()
    SUSFS: str = str(
        input("Apply SUSFS patch (Required)(Y/n): ").lower() == "y"
    ).lower()
    LXC: str = str(input("Apply LXC patch (Y/n): ").lower() == "y").lower()

    os.environ["KSU"] = KSU
    os.environ["SUSFS"] = SUSFS
    os.environ["LXC"] = LXC
    os.environ["LOCAL_RUN"] = "true"

    KernelBuilder().run_build()


if __name__ == "__main__":
    run()
