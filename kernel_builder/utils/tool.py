import sh
from pathlib import Path
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from kernel_builder.config.config import ROOT


def patch(
    patch: Path, *, check: bool = True, cwd: Path | None = None
) -> sh.RunningCommand:
    log(f"Patching file: {FileSystem.relative_to(ROOT, patch)}")
    cwd = cwd or Path.cwd()
    data: bytes = patch.read_bytes()
    return sh.patch(
        "-p1",
        "--forward",
        "--fuzz=3",
        _in=data,
        _cwd=str(cwd),
        _ok_code=[0, 1] if not check else [0],
    )


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
