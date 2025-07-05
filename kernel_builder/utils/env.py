import os


def ksu_variant(default: str = "NONE") -> str:
    return os.getenv("KSU", default).upper()


def susfs_enabled(default: str = "false") -> bool:
    return os.getenv("SUSFS", default).lower() == "true"


def lxc_enabled(default: str = "false") -> bool:
    return os.getenv("LXC", default).lower() == "true"
