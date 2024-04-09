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

import logging

from config import LOGGING_FILE_HANDLER, LOGGING_FORMAT_TEMPLATE

formatter = logging.Formatter(LOGGING_FORMAT_TEMPLATE)

FILE_HANDLER = logging.FileHandler(LOGGING_FILE_HANDLER)
FILE_HANDLER.setFormatter(formatter)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(formatter)


def log(name: str, text: str) -> None:
    """
    Configure logging for the application.

    This function sets up the logging mechanism for the application to log messages to both a file and the console.
    It creates a logger with the specified name and logs the given text using the configured handlers.

    Parameters:
        name: str - The name of the logger.
        text: str - The text message to be logged.

    Returns:
        None
    """
    _LOGGER = logging.getLogger(name)
    _LOGGER.setLevel(logging.INFO)

    for _HADLER in _LOGGER.handlers[:]:
        _LOGGER.removeHandler(_HADLER)

    _LOGGER.addHandler(FILE_HANDLER)
    _LOGGER.addHandler(CONSOLE_HANDLER)

    _LOGGER.info(text)
