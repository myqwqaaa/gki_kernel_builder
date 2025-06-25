from dataclasses import dataclass, field
from subprocess import CompletedProcess
from src.config.manifest import SOURCES
from src.utils.shell import Shell
from src.utils.log import log
from typing import TypeAlias

Proc: TypeAlias = CompletedProcess[bytes]


@dataclass(slots=True)
class SourceManager:
    shell: Shell = field(default_factory=Shell)
    sources: list[dict[str, str]] = field(default_factory=lambda: SOURCES.copy())

    def clone_repo(
        self, repo: dict[str, str], *, depth: int = 1, args: list[str] | None = None
    ) -> Proc:
        """
        Clone a git repository.

        :param repo: Dictionary with keys 'url', 'branch', and 'to'.
        :param depth: Depth of the clone, default is 1.
        :param args: Additional arguments to pass to git clone.
        :return: Proc
        """
        return self.shell.run(
            [
                "git",
                "clone",
                "--depth",
                str(depth),
                "-b",
                repo["branch"],
                *(args or []),
                repo["url"],
                repo["to"],
            ]
        )

    def clone_sources(self) -> None:
        """
        Clone all sources in SOURCES.

        :return: None
        """
        for source in self.sources:
            log(
                f"Cloning {source['url']} into {source['to']} on branch {source['branch']}"
            )
            self.clone_repo(source, args=["--recurse-submodules"])


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
