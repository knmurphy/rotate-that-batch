from rich.logging import RichHandler
import logging
import sys

def setup_logger():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    logger = logging.getLogger("rich")
    return logger

logger = setup_logger()
