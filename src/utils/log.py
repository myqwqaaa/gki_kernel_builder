from logging import Logger
import logging
from rich.logging import RichHandler
from pathlib import Path
from src.config.config import LOGFILE

logger: Logger = logging.getLogger(__name__)


def _configure_log(
    *, level: int = logging.INFO, logfile: str | Path | None = None
) -> None:
    """
    Initialize logging if NOT configured.

    :param level: Logging level, default is INFO.
    :return: None
    """

    if logger.handlers:
        return

    handlers: list[logging.Handler] = [
        RichHandler(
            show_level=True,
            show_path=False,
            rich_tracebacks=True,
        )
    ]

    if logfile:
        handlers.append(logging.FileHandler(logfile))

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=handlers,
    )


def log(
    message: str, level: str = "info", *, logfile: str | Path | None = LOGFILE
) -> None:
    """
    Simple wrapper for logging.

    :param message: Message to log.
    :param level: Log level, default is info.
    :param logfile: Log file path, default is LOGFILE.
    :return: None
    """
    _configure_log(logfile=logfile)

    match level.lower():
        case "debug":
            logger.debug(message)
        case "info":
            logger.info(message)
        case "warn" | "warning":
            logger.warning(message)
        case "error":
            logger.error(message)
        case "critical":
            logger.critical(message)
        case _:
            logger.warning("Unknown log level %s; defaulting to INFO", level)
            logger.info(message)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
