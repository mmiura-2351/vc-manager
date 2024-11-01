"""This module provides a function to read environment variables from a .env file."""

import os

from dotenv import load_dotenv


class EnvVariableNotFoundError(KeyError):
    """Exception raised when an environment variable is not found."""

    def __init__(self, key: str) -> None:
        """Initialize with the missing environment variable key."""
        super().__init__(f"Environment variable '{key}' not found.")


def get_env_value(key: str) -> str:
    """Returns the value of the specified environment variable key.

    Raises:
        KeyError: If the environment variable is not found or is None.
    """
    load_dotenv()
    value = os.getenv(key)
    if value is None:
        raise EnvVariableNotFoundError(key)
    return value
