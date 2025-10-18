import logging

from rich.console import Console
from rich.logging import RichHandler

_logging_console = Console(
    stderr=True,
)
CONFIGURED_LOGGER = False


def setup_logger(
    level: int = logging.INFO,
):

    global CONFIGURED_LOGGER

    package_logger = logging.getLogger(
        __package__,
    )

    print(__package__)

    package_logger.setLevel(
        level,
    )

    rich_handler = RichHandler(
        console=_logging_console,
        rich_tracebacks=True,
        show_time=True,
        show_level=True,
        markup=True,
        enable_link_path=True,
        tracebacks_theme="github-dark",
        omit_repeated_times=True,
    )

    rich_handler.setLevel(
        logging.NOTSET,
    )

    package_logger.addHandler(
        rich_handler,
    )

    CONFIGURED_LOGGER = True


def get_logger(
    name: str = __package__,
    level: int = logging.INFO,
):

    if not CONFIGURED_LOGGER:
        setup_logger(
            level=level,
        )

    return logging.getLogger(
        name=name,
    )
