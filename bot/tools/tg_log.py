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

from telegram import Bot, Update
from telegram.ext import ContextTypes

from common.logger import log as logger
from config import TELEGRAM_TOKEN, TELEGRAM_LOG


async def _tg_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    
    make log into logging telegram chat
    :param update:
    :param context:
    
    """
    TEXT: str = f'```json\n{json.dumps(update.to_dict(), ensure_ascii=False, indent=4)}```'
    if len(TEXT) < 4096:
        await context.bot.send_message(chat_id=TELEGRAM_LOG, text=TEXT, parse_mode='markdown')


async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    
    log for all handlers
    :param update:
    :param context:
    
    """
    USERNAME: str = update.effective_user.username
    ID: int = update.effective_user.id
    DATA: str = update.callback_query.data if update.callback_query is not None else update.message.text
    logger(f'{USERNAME}(id={ID}): {DATA}')
    await _tg_log(update, context)
