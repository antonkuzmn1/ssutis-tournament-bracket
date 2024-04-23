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

from telegram import Update
from typing import Dict


class MessageTimeoutChecker:
    def __init__(self):
        self.last_message_time: Dict[int, float] = {}

    # noinspection PyShadowingNames
    def check_timeout(self, update: Update) -> bool:
        """
        check message timeout
        :param update:
        :return: boolean
        """
        ID = update.message.from_user.id
        CURRENT_TIME = update.message.date.timestamp()

        if ID in self.last_message_time:
            if CURRENT_TIME - self.last_message_time[ID] < 60:
                return False

        self.last_message_time[ID] = CURRENT_TIME
        return True


_CHECKER = MessageTimeoutChecker()


def check(update) -> bool:
    return _CHECKER.check_timeout(update)
