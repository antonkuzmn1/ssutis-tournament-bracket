import json

from telegram import Bot

from common.logger import log
from config import TELEGRAM_TOKEN, TELEGRAM_LOG


async def tg_log(update) -> None:
    """
    make log into logging telegram chat
    :param update:
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    text = f'```json\n{json.dumps(update.to_dict(), ensure_ascii=False, indent=4)}```'
    await bot.send_message(chat_id=TELEGRAM_LOG, text=text, parse_mode='markdown')


async def log_start(name, update) -> None:
    log(name, f'started by {update.effective_user.username}(id={update.effective_user.id})')
    await tg_log(update)


async def log_message(name, update) -> None:
    log(name, f'message from {update.effective_user.username}(id={update.effective_user.id}): {update.message.text}')
    await tg_log(update)


async def log_callback(name, update) -> None:
    log(name, f'callback querry from {update.effective_user.username}(id={update.effective_user.id}): {update.callback_query.data}')
    await tg_log(update)
