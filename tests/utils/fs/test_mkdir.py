from pathlib import Path
from kernel_builder.utils.fs import FileSystem


def test_mkdir(tmp_path: Path):
    p: Path = tmp_path / "deep" / "nest" / "out"

    fs = FileSystem()
    fs.mkdir(p)
    fs.mkdir(p)

    assert p.is_dir()
    assert not any(p.iterdir())
