import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения состояний пользователей
user_states = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "🤖 Я бот для анонимных сообщений\n\n"
        "📝 Используй команды:\n"
        "/send - отправить анонимное сообщение\n"
        "/help - помощь\n"
        "/myid - узнать свой ID"
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **Помощь по использованию бота:**

🔹 **Как отправить сообщение:**
1. Используй команду /send
2. Введи ID пользователя, которому хочешь написать
3. Напиши своё сообщение

🔹 **Как получить свой ID:**
Используй команду /myid

🔹 **Как это работает:**
- Ты отправляешь сообщение через меня
- Получатель видит только текст, твоя личность скрыта
- Получатель может ответить на твоё сообщение

⚠️ **Важно:** 
- Не спамь и не нарушай правила
- Сообщения модерируются
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Команда /myid
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"🆔 Твой ID: `{user_id}`\n\n"
        "Поделись этим ID с друзьями, чтобы они могли отправлять тебе анонимные сообщения!",
        parse_mode='Markdown'
    )

# Команда /send
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_states[update.effective_user.id] = 'waiting_for_id'
    await update.message.reply_text(
        "📨 Введите ID пользователя, которому хотите отправить сообщение:"
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Если пользователь в состоянии ожидания ID
    if user_id in user_states and user_states[user_id] == 'waiting_for_id':
        try:
            target_id = int(text)
            context.user_data['target_id'] = target_id
            user_states[user_id] = 'waiting_for_message'
            await update.message.reply_text(
                "💬 Теперь введите ваше анонимное сообщение:"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Неверный формат ID. ID должен быть числом.\n"
                "Попробуйте снова:"
            )
    
    # Если пользователь в состоянии ожидания сообщения
    elif user_id in user_states and user_states[user_id] == 'waiting_for_message':
        target_id = context.user_data.get('target_id')
        
        if target_id:
            try:
                # Отправляем сообщение целевому пользователю
                keyboard = [
                    [InlineKeyboardButton("📨 Ответить", callback_data=f"reply_{user_id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await context.bot.send_message(
                    chat_id=target_id,
                    text=f"📩 **Анонимное сообщение:**\n\n{text}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
                await update.message.reply_text(
                    "✅ Сообщение успешно отправлено анонимно!"
                )
                
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                await update.message.reply_text(
                    "❌ Не удалось отправить сообщение. Возможно, пользователь с таким ID не найден или заблокировал бота."
                )
        
        # Очищаем состояние
        if user_id in user_states:
            del user_states[user_id]
        if 'target_id' in context.user_data:
            del context.user_data['target_id']
    
    # Обычное сообщение
    else:
        await update.message.reply_text(
            "🤖 Используй команды:\n"
            "/send - отправить сообщение\n"
            "/help - помощь\n"
            "/myid - узнать свой ID"
        )

# Обработка callback кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('reply_'):
        target_id = int(data.split('_')[1])
        context.user_data['reply_target'] = target_id
        user_states[query.from_user.id] = 'waiting_for_reply'
        
        await query.edit_message_text(
            "💌 Введите ваш ответ на это анонимное сообщение:"
        )

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Основная функция
def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    TOKEN = "YOUR_BOT_TOKEN"
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myid", myid))
    application.add_handler(CommandHandler("send", send_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
