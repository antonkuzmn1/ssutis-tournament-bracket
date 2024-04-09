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
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from bot.handlers.callback import callback
from bot.handlers.message import message
from bot.handlers.start import start
from common.logger import log
from config import TELEGRAM_TOKEN


def main() -> None:
    """Start the bot."""
    log(__name__, 'Telegram-bot started')

    _APP = Application.builder().token(TELEGRAM_TOKEN).build()

    _APP.add_handler(CommandHandler("start", start))
    _APP.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    _APP.add_handler(CallbackQueryHandler(callback))

    _APP.run_polling(allowed_updates=Update.ALL_TYPES)
