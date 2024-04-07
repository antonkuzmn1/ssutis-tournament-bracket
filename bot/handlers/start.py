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
from telegram.ext import ContextTypes

from config import TELEGRAM_ADMIN
from bot.tools.bridge import get_student
from bot.tools.methods import request_snpg, validation_in_process
from bot.tools.tg_log import log_start


# noinspection PyUnusedLocal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await log_start(__name__, update)
    student = get_student(update)

    if update.message.chat.id == TELEGRAM_ADMIN:
        await update.message.reply_text("not working yet")
        return

    else:
        if student.surname == '':
            await request_snpg(update)
            return
        if student.valid == 0:
            await validation_in_process(update)
            return
