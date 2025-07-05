from types import SimpleNamespace
from pytest_mock.plugin import MockType
import pytest
import types
import run
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    "ksu, susfs, expect_exit",
    [
        ("NEXT", True, False),
        ("SUKI", True, False),
        ("RKSU", True, False),
        ("NONE", True, True),
    ],
)
def test_build_guard(mocker: MockerFixture, ksu, susfs, expect_exit) -> None:
    fake: MockType = mocker.patch("kernel_builder.main.KernelBuilder", autospec=True)
    ns: SimpleNamespace = types.SimpleNamespace(
        command="build", ksu=ksu, susfs=susfs, lxc=False
    )

    if expect_exit:
        with pytest.raises(SystemExit):
            run.cmd_build(ns)
    else:
        run.cmd_build(ns)
