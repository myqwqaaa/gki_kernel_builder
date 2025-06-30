import subprocess
import os

from subprocess import CompletedProcess
from typing import TypeAlias
from src.utils.log import log
from pathlib import Path

Proc: TypeAlias = CompletedProcess[bytes]


class Shell:
    """Helper class for interacting with the shell."""

    def run(self, command: list[str]) -> Proc:
        """
        Run cmd with current environment.

        :param command: Command to run as a list of strings.
        :return: CompletedProcess[bytes]
        """
        log(f"Running command {' '.join(command)}")
        return subprocess.run(command, check=True, env=os.environ)

    def patch(self, patch: str | Path) -> Proc:
        with open(patch, "rb") as f:
            return subprocess.run(
                ["patch", "-p1", "--forward", "--fuzz=3"], input=f.read(), check=True
            )


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
