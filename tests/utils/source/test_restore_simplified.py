import pytest
from kernel_builder.utils.source import SourceManager


def test_restore_simplified():
    original = "github.com:foo/bar"
    full = SourceManager.restore_simplified(original)
    assert full == "https://github.com/foo/bar"

    assert SourceManager.restore_simplified(full) == full
