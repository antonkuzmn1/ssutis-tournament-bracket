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
import json

from telegram import Update
from telegram.ext import ContextTypes

from bot.tools.tg_log import log
from bot.tools.user_methods import UserMethods
from config import TELEGRAM_ADMIN


# noinspection PyUnusedLocal
async def _admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return


# noinspection PyUnusedLocal
async def _user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return
    # match (await get_student(update)).valid:
    #     case 0:
    #         await confirm_snpg(update)
    #     case 1:
    #         await validation_in_process(update)
    #     case 2:
    #         return
    #     case _:
    #         return


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await log(update=update, context=context)
    # print(json.dumps(update.to_dict(), ensure_ascii=False, indent=4))

    ID: int = update.message.chat.id

    if ID == TELEGRAM_ADMIN:
        await _admin(update, context)
    else:
        await UserMethods(update, context).entry()
