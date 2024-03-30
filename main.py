from backend.main import main as backend_app
from telegram_bot.bot import main as telegram_bot

if __name__ == '__main__':
    telegram_bot()
    backend_app()
