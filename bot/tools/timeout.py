from telegram import Update
from typing import Dict


class MessageTimeoutChecker:
    def __init__(self):
        self.last_message_time: Dict[int, float] = {}

    # noinspection PyShadowingNames
    def check_timeout(self, update: Update) -> bool:
        user_id = update.message.from_user.id
        current_time = update.message.date.timestamp()

        if user_id in self.last_message_time:
            if current_time - self.last_message_time[user_id] < 60:
                return False

        self.last_message_time[user_id] = current_time
        return True


checker = MessageTimeoutChecker()


def check(update) -> bool:
    return checker.check_timeout(update)
