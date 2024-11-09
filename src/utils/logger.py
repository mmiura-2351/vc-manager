"""This module provides the Logger class for managing logging."""

import logging

from logzero import setup_logger


class Logger:
    """A logger class to handle logging with a specified name and level."""

    def __init__(
        self,
        logfile: str,
        name: str,
        level: int = logging.INFO,
        *,
        disablestderrlogger: bool = False,
    ) -> None:
        """Initialize the Logger with a specified name and logging level.

        Args:
            logfile (str): The path to the log file.
            name (str): The name of the logger.
            level (int, optional): The logging level. Defaults to logging.INFO.
            disablestderrlogger (bool, optional): Disable the stderr logger.
                Defaults to False.
        """
        self.logger = setup_logger(
            name=name,
            level=level,
            formatter=logging.Formatter(
                "[%(asctime)s - %(levelname)s] %(message)s",
            ),
            logfile=logfile,
            disableStderrLogger=disablestderrlogger,
        )

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)
