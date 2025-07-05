from pathlib import Path
from types import ModuleType
import importlib
import pytest
import logging


@pytest.fixture
def fresh_log() -> ModuleType:
    return importlib.import_module("kernel_builder.utils.log")


def test_log_info(caplog: pytest.LogCaptureFixture, fresh_log):
    with caplog.at_level(logging.INFO):
        fresh_log.log("hello world")
    assert "hello world" in caplog.text


def test_no_duplicate_handlers(fresh_log):
    fresh_log.log("once")
    count = len(fresh_log.logger.handlers)
    fresh_log.log("twice")
    assert len(fresh_log.logger.handlers) == count
