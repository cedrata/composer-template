from typing import Optional, Protocol


class ILogger(Protocol):
    """
    Interface where basic logging behaviour is defined.
    """

    def add_logger(logger_name: str, configuration: Optional[str] = None) -> None:
        """
        Create a new logger with the given name.

        Args:
            logger_name (str): logger name.
        """

    def file_config(config_file_path: str) -> None:
        """
        Configure the given logger with a valid configuration file.

        Args:
            config_file_path (str): absolute path of the configuration file.
        """

    def debug(logger_name: str, message: str) -> None:
        """
        Print a debug level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """

    def info(logger_name: str, message: str) -> None:
        """
        Print an info level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """

    def warning(logger_name: str, message: str) -> None:
        """
        Print a warning level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """

    def error(logger_name: str, message: str) -> None:
        """
        Print an error level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """

    def critical(logger_name: str, message: str) -> None:
        """
        Print critical level log statement with the specified logger.

        Args:
            logger_name (str): the logger name to use.
            message (str): the message to log.
        """
