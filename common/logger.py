"""

Copyright 2024 Anton Kuzmin (https://github.com/antonkuzmn1)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from logging import Formatter, FileHandler, StreamHandler, getLogger, WARNING

from config import LOGGING_FILE_HANDLER, LOGGING_FORMAT_TEMPLATE

FORMATTER: Formatter = Formatter(LOGGING_FORMAT_TEMPLATE)

FILE_HANDLER: FileHandler = FileHandler(LOGGING_FILE_HANDLER)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER: StreamHandler = StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)


def log(text: str) -> None:
    """
    Configure logging for the application.

    This function sets up the logging mechanism for the application to log messages to both a file and the console.
    It creates a logger with the specified name and logs the given text using the configured handlers.

    Parameters:
        text: str - The text message to be logged.

    Returns:
        None
    """
    LOGGER = getLogger()
    LOGGER.setLevel(WARNING)

    for HANDLER in LOGGER.handlers[:]:
        LOGGER.removeHandler(HANDLER)

    LOGGER.addHandler(FILE_HANDLER)
    LOGGER.addHandler(CONSOLE_HANDLER)

    LOGGER.warning(text)


if __name__ == "__main__":
    """local test"""
    log("Test passed")
