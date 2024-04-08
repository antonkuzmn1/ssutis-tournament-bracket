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

from bot.tools.bridge import get_student
from bot.tools.methods import (request_snpg,
                               request_validation,
                               validation_in_process,
                               main_menu,
                               application_list,
                               application_list_show,
                               application_list_reject,
                               application_list_accept, student_main)
from bot.tools.tg_log import log_callback
from bot.tools.timeout import check
from config import TELEGRAM_ADMIN


# noinspection PyUnusedLocal
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    await log_callback(__name__, update)
    student = get_student(update)
    data = update.callback_query.data

    if update.callback_query.message.chat.id == TELEGRAM_ADMIN:
        if data == 'application_list':
            await application_list(update)
            return
        if data == 'main_menu':
            await main_menu(update)
            return
        if data.split('=')[0] == 'application_list_show':
            await application_list_show(update)
            return
        if data.split('=')[0] == 'application_list_reject':
            await application_list_reject(update)
            return
        if data.split('=')[0] == 'application_list_accept':
            await application_list_accept(update)
            return
        else:
            await main_menu(update)
            return

    else:
        if student.valid == 0:
            if data == 'request_snpg':
                await request_snpg(update)
                return
            if data == 'request_validation':
                await request_validation(update)
                return
            else:
                return
        if student.valid == 1:
            if check(update):
                await validation_in_process(update)
            return
        if student.valid == 2:
            if data == 'student_main':
                await student_main(update)
                return
            else:
                await student_main(update)
                return
        else:
            return
