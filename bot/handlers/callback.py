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
                               application_list_accept, student_main, students_list, students_list_show)
from bot.tools.tg_log import log_callback
from bot.tools.timeout import check
from config import TELEGRAM_ADMIN


# noinspection PyUnusedLocal
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    await log_callback(__name__, update)
    _VALID: int = get_student(update).valid
    _DATA: str = update.callback_query.data
    _SPLIT: str = _DATA.split('=')[0]

    if update.callback_query.message.chat.id == TELEGRAM_ADMIN:
        if _DATA == 'application_list':
            await application_list(update)
            return
        if _DATA == 'main_menu':
            await main_menu(update)
            return
        if _DATA == 'students_list':
            await students_list(update)
            return
        if _SPLIT == 'application_list_show':
            await application_list_show(update)
            return
        if _SPLIT == 'application_list_reject':
            await application_list_reject(update)
            return
        if _SPLIT == 'application_list_accept':
            await application_list_accept(update)
            return
        if _SPLIT == 'students_list_show':
            await students_list_show(update)
            return
        await main_menu(update)

    else:
        if _VALID == 0:
            if _DATA == 'request_snpg':
                await request_snpg(update)
                return
            if _DATA == 'request_validation':
                await request_validation(update)
                return

        if _VALID == 1:
            if check(update):
                await validation_in_process(update)

        if _VALID == 2:
            if _DATA == 'student_main':
                await student_main(update)
                return
            if _DATA == 'students_list':
                await students_list(update)
                return
            if _SPLIT == 'students_list_show':
                await students_list_show(update)
                return
            await student_main(update)

    return
