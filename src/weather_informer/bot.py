import logging
from datetime import timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from apscheduler.triggers.interval import IntervalTrigger

from weather import get_weather
from storage import (
    get_user_city,
    set_user_city,
    set_user_interval,
    has_user_city,
)

logger = logging.getLogger(__name__)

# === Функции обратного вызова ===

async def send_weather_update(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    user_id = job.kwargs["user_id"]
    city = job.kwargs["city"]

    weather_msg = get_weather(city)
    try:
        await context.bot.send_message(chat_id=user_id, text=weather_msg)
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

# === Обработчики команд и сообщений ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🌦️ Я бот прогноза погоды.\n"
        "1. Отправь мне название города.\n"
        "2. Затем выбери частоту уведомлений."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    city = update.message.text.strip()

    # Проверяем, существует ли город
    test_msg = get_weather(city)
    if "❌" in test_msg or "⚠️" in test_msg:
        await update.message.reply_text("Город не найден. Попробуйте снова.")
        return

    set_user_city(user_id, city)

    keyboard = [
        [
            InlineKeyboardButton("Каждый час", callback_data="1"),
            InlineKeyboardButton("Каждые 3 часа", callback_data="3"),
        ],
        [
            InlineKeyboardButton("Каждые 5 часов", callback_data="5"),
            InlineKeyboardButton("Каждые 12 часов", callback_data="12"),
        ],
        [InlineKeyboardButton("Отключить уведомления", callback_data="0")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"📍 Город установлен: {city}\nВыберите частоту уведомлений:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    interval_hours = int(query.data)

    city = get_user_city(user_id)
    if not city:
        await query.edit_message_text("Сначала отправьте название города.")
        return

    # Удаляем старые задачи
    jobs = context.job_queue.get_jobs_by_name(str(user_id))
    for job in jobs:
        job.schedule_removal()

    if interval_hours == 0:
        set_user_interval(user_id, 0)
        await query.edit_message_text("Уведомления отключены.")
        return

    # Запускаем новую периодическую задачу
    context.job_queue.run_repeating(
        send_weather_update,
        interval=timedelta(hours=interval_hours),
        first=timedelta(seconds=3),
        name=str(user_id),
        data={"user_id": user_id, "city": city}
    )

    set_user_interval(user_id, interval_hours)
    await query.edit_message_text(
        f"✅ Уведомления настроены!\nГород: {city}\nЧастота: каждые {interval_hours} ч."
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    jobs = context.job_queue.get_jobs_by_name(str(user_id))
    for job in jobs:
        job.schedule_removal()
    set_user_interval(user_id, 0)
    await update.message.reply_text("Уведомления отключены.")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    city = get_user_city(user_id)
    if not city:
        await update.message.reply_text("Сначала отправьте название города.")
        return
    weather_msg = get_weather(city)
    await update.message.reply_text(weather_msg)
