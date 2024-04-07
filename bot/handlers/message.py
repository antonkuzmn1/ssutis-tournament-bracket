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

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.tools.bridge import get_student
from bot.tools.tg_log import log_message
from bot.tools.methods import confirm_snpg, validation_in_process
from config import TELEGRAM_ADMIN


# noinspection PyUnusedLocal
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await log_message(__name__, update)
    student = get_student(update)

    if update.message.chat.id == TELEGRAM_ADMIN:
        await update.message.reply_text("not working yet")
        return

    else:
        if student.surname == '':
            await confirm_snpg(update)
            return
        if student.valid == 0:
            await validation_in_process(update)
            return
