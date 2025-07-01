import shutil

from kernel_builder.utils.log import log
from pathlib import Path
from os import chdir


class FileSystem:
    @staticmethod
    def mkdir(path: Path) -> None:
        """
        Create path and parents if missing (same as mkdir -p).

        :param path: Path to create.
        :return: None
        """
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def cd(path: Path) -> None:
        """
        A more verbose wrapper for os.chdir()

        :param path: Path to change to.
        :return: None
        """
        log(f"Changing directory to {path}")
        chdir(path)

    @staticmethod
    def reset_path(path: Path) -> None:
        """
        - If path does not exist -> create it.
        - If path is an empty dir or non-empty -> remove & recreate.
        - If path is a file/symlink -> delete it.

        :param path: Path to reset.
        :return: None
        """
        if path.exists():
            if path.is_dir():
                log(f"Removing existing directory: {path}")
                shutil.rmtree(path)
            else:
                log(f"Removing file/symlink: {path}")
                path.unlink()
        log(f"Creating path: {path}")
        FileSystem.mkdir(path)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
