from pathlib import Path
from kernel_builder.utils.fs import FileSystem


def test_reset_path(tmp_path: Path):
    p: Path = tmp_path / "out"
    p.mkdir()
    (p / "text").write_text("x")
    FileSystem().reset_path(p)
    assert p.exists() and not any(p.iterdir())
