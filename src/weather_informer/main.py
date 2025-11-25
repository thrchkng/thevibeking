import logging
import os
from telegram.ext import Application
from dotenv import load_dotenv

from bot import start, handle_message, button_handler, stop, now

# Загрузка .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Проверьте файл .env")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(start)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("now", now))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger = logging.getLogger(__name__)
    logger.info("Бот запущен и ожидает сообщений...")

    application.run_polling()

if __name__ == "__main__":
    main()
