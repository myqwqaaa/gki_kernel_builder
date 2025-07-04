import pytest
import types
import run


@pytest.mark.parametrize(
    "ksu, susfs, expect_exit",
    [
        ("NEXT", True, False),
        ("SUKI", True, False),
        ("RKSU", True, False),
        ("NONE", True, True),
    ],
)
def test_build_guard(mocker, ksu, susfs, expect_exit) -> None:
    fake = mocker.patch("kernel_builder.main.KernelBuilder", autospec=True)
    ns = types.SimpleNamespace(command="build", ksu=ksu, susfs=susfs, lxc=False)

    if expect_exit:
        with pytest.raises(SystemExit):
            run.cmd_build(ns)
    else:
        run.cmd_build(ns)
