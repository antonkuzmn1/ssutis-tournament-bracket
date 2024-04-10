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

    _DATA: str = update.callback_query.data.split('=')[0]

    if update.callback_query.message.chat.id == TELEGRAM_ADMIN:
        match _DATA:
            case 'application_list':
                await application_list(update)
            case 'main_menu':
                await main_menu(update)
            case 'students_list':
                await students_list(update)
            case 'application_list_show':
                await application_list_show(update)
            case 'application_list_reject':
                await application_list_reject(update)
            case 'application_list_accept':
                await application_list_accept(update)
            case 'students_list_show':
                await students_list_show(update)
            case _:
                await main_menu(update)

    else:
        match get_student(update).valid:
            case 0:
                match _DATA:
                    case 'request_snpg':
                        await request_snpg(update)
                    case 'request_validation':
                        await request_validation(update)

            case 1:
                if check(update):
                    await validation_in_process(update)

            case 2:
                match _DATA:
                    case 'student_main':
                        await student_main(update)
                    case 'students_list':
                        await students_list(update)
                    case 'students_list_show':
                        await students_list_show(update)
                    case _:
                        await student_main(update)
