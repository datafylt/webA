import sys
import logging

from loguru import logger as loguru_logger

from app.settings import settings


class Loggin:
    def __init__(self) -> None:
        debug = settings.DEBUG
        if debug:
            self.level = "DEBUG"
        else:
            self.level = "INFO"
            # Désactiver les logs debug de tortoise, aiosqlite, etc.
            logging.getLogger("tortoise").setLevel(logging.WARNING)
            logging.getLogger("aiosqlite").setLevel(logging.WARNING)
            logging.getLogger("tortoise.db_client").setLevel(logging.WARNING)

    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=sys.stdout, level=self.level)

        # logger.add("my_project.log", level=level, rotation="100 MB")  # Output log messages to a file
        return loguru_logger


loggin = Loggin()
logger = loggin.setup_logger()