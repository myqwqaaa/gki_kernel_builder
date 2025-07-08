import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from kernel_builder.utils.env import verbose_enabled
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from kernel_builder.config.config import ROOT


class Shell:
    """Helper class for interacting with the shell."""

    def __init__(self):
        self.fs: FileSystem = FileSystem()

    def run(
        self, command: list[str], verbose: bool | None = None
    ) -> CompletedProcess[bytes]:
        """
        Run cmd with current environment.

        :param command: Command to run as a list of strings.
        :return: CompletedProcess[bytes]
        """
        use_verbose: bool = verbose if verbose is not None else verbose_enabled()
        log(f"Running command {' '.join(command)}")
        if use_verbose:
            return subprocess.run(command, check=True, env=os.environ)
        else:
            return subprocess.run(
                command,
                check=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                env=os.environ,
            )

    def patch(
        self, patch: Path, *, check: bool = True, cwd: Path | None = None
    ) -> CompletedProcess[bytes]:
        log(f"Patching file: {self.fs.relative_to(ROOT, patch)}")
        with open(patch, "rb") as f:
            return subprocess.run(
                ["patch", "-p1", "--forward", "--fuzz=3"],
                input=f.read(),
                check=check,
                cwd=cwd or Path.cwd(),
            )


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
