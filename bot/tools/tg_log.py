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

from telegram import Bot

from common.logger import log
from config import TELEGRAM_TOKEN, TELEGRAM_LOG


async def _tg_log(update) -> None:
    """
    make log into logging telegram chat
    :param update:
    """
    _BOT = Bot(token=TELEGRAM_TOKEN)
    _TEXT: str = f'```json\n{json.dumps(update.to_dict(), ensure_ascii=False, indent=4)}```'
    await _BOT.send_message(chat_id=TELEGRAM_LOG, text=_TEXT, parse_mode='markdown')


async def log_start(name, update) -> None:
    """
    log for start handler
    :param name:
    :param update:
    """
    _USERNAME: str = update.effective_user.username
    _ID: str = update.effective_user.id
    log(name, f'started by {_USERNAME}(id={_ID})')
    await _tg_log(update)


async def log_message(name, update) -> None:
    """
    log for message handler
    :param name:
    :param update:
    """
    _USERNAME: str = update.effective_user.username
    _ID: str = update.effective_user.id
    _TEXT: str = update.message._TEXT
    log(name, f'message from {_USERNAME}(id={_ID}): {_TEXT}')
    await _tg_log(update)


async def log_callback(name, update) -> None:
    """
    log for callback handler
    :param name:
    :param update:
    """
    _USERNAME: str = update.effective_user.username
    _ID: str = update.effective_user.id
    _DATA: str = update.callback_query.data
    log(name, f'callback querry from {_USERNAME}(id={_ID}): {_DATA}')
    await _tg_log(update)
