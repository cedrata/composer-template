from genericpath import exists
from logging import getLogger
from logging.config import dictConfig
from os.path import exists as os_path_exists, isfile as os_path_isfile
from typing import List, Optional
from yaml import safe_load
from zope.interface import implementer as z_implementer

from app.services.logger.enums.level import LogLevel
from app.services.logger.interfaces.i_logger import ILogger


@z_implementer(ILogger)
class CdrtLogger():
    """
    Implementation of the ILogger interface using
    the already existing logging facility.
    """

    # Private attributes
    _avaiable_loggers: List[str]

    def __init__(self, config_file_path: Optional[str] = None) -> None:
        """
        Create a new CdrtLogger with an empty list of avaiable loggers.
        If no configurations is passed, the default configuration is applied.

        Args:
            config_file_path (Optional[str], optional): _description_. Defaults to None.
        """
        
        self._avaiable_loggers = []
        if config_file_path is not None:
            self.file_config(config_file_path)

    def add_logger(self, logger_name: str) -> None:
        """
        Create a new logger with the given name.

        Args:
            logger_name (str): logger name.
        """

        new_logger = getLogger(logger_name)
        if new_logger.name not in self._avaiable_loggers: self._avaiable_loggers.append(new_logger.name)

    def file_config(self, config_file_path: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            config_file_path (str): absolute path of the configuration file.
        """

        if not os_path_exists(config_file_path) or not os_path_isfile(config_file_path):
            raise FileNotFoundError

        with open(config_file_path, 'r') as config_file_sream:
            dictConfig(safe_load(config_file_path))

    def print_log(self, logger_name: str, logger_level: LogLevel, message: str) -> None:
        """
        Print a log statement with the specified logger with the given level.

        Args:
            logger_name (str): the logger name to use.
            logger_level (str): the log level to print.
            message (str): the message to log.
        """