import pytest
from kernel_builder.utils.env import ksu_variant, susfs_enabled, lxc_enabled, local_run
from pytest import MonkeyPatch


@pytest.mark.parametrize(
    "var,value,func,expected",
    [
        ("KSU", "next", ksu_variant, "NEXT"),
        ("SUSFS", "TrUe", susfs_enabled, True),
        ("LXC", "false", lxc_enabled, False),
        ("LOCAL_RUN", "FaLsE", local_run, False),
    ],
)
def test_env_flag_present(monkeypatch: MonkeyPatch, var, value, func, expected) -> None:
    monkeypatch.setenv(var, value)
    assert func() == expected


def test_env_flag_defaults() -> None:
    assert ksu_variant() == "NONE"
    assert susfs_enabled() is False
    assert lxc_enabled() is False
    assert local_run() is False

    assert ksu_variant("NEXT") == "NEXT"
    assert susfs_enabled("TrUe") is True
    assert lxc_enabled("TrUe") is True
    assert local_run("FaLSe") is False
