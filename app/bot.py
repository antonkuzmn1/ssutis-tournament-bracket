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
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from app.database import request
from config import TELEGRAM_TOKEN

# noinspection SpellCheckingInspection
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def info(update) -> None:
    """
    Logs information to the console.

    This function logs the current date, time, Telegram user ID, username, and text of the message
    from the update provided. It formats the information and prints it to the console.

    Parameters:
        update: Update
            The update object from the Telegram API containing user and message information.

    Returns:
        None

    Authors:
        Anton Kuzmin (https://github.com/antonkuzmn1)
    """
    date = datetime.now().strftime("%Y-%d-%m")
    time = datetime.now().strftime("%H:%M:%S")
    tg_id = update.effective_user.id
    username = update.effective_user.username
    text = update.effective_message.text
    print(f'[date={date}][time={time}][id={tg_id}][username={username}] {text}')


# noinspection PyUnusedLocal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown('```python\nprint(\'hello world!\')```')


# noinspection PyUnusedLocal
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    info(update)
    await update.message.reply_text("Help!")


# noinspection PyUnusedLocal
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    info(update)

    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
        [InlineKeyboardButton("TEST", callback_data="TEST")],
    ]

    await update.message.reply_markdown(update.effective_message.text,
                                        reply_markup=InlineKeyboardMarkup(keyboard))


# noinspection PyUnusedLocal
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    if update.callback_query.data == 'TEST':
        rows = request('''SELECT * FROM users''')
        await update.callback_query.edit_message_text(f'```json\n{json.dumps(rows)}```')

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # await query.answer()

    # await query.edit_message_text(text=f"Selected option: {query.data}")


def start_bot() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main() -> None:
    start_bot()


if __name__ == "__main__":
    main()
