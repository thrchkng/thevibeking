import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from games import (
    GuessNumberGame,
    RockPaperScissorsGame,
    QuizGame,
    GAME_STATES
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
MAIN_MENU, PLAYING_GAME = range(2)

class MiniGamesBot:
    def __init__(self, token: str):
        self.token = token
        self.games = {
            'guess_number': GuessNumberGame(),
            'rps': RockPaperScissorsGame(),
            'quiz': QuizGame()
        }
        self.current_game = None
        self.user_scores = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            "Добро пожаловать в мир мини-игр!\n"
            "Выбери игру из меню ниже:",
            reply_markup=self.get_main_menu_keyboard()
        )
        return MAIN_MENU

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = (
            "🎮 *Доступные команды:*\n\n"
            "*/start* - Главное меню\n"
            "*/help* - Справка\n"
            "*/stats* - Статистика\n"
            "*/cancel* - Отменить текущую игру\n\n"
            "*Игры:*\n"
            "1. 🔢 *Угадай число* - бот загадывает число от 1 до 100\n"
            "2. ✂️ *Камень-ножницы-бумага* - классическая игра\n"
            "3. 📚 *Викторина* - вопросы на общие знания\n\n"
            "Для выбора игры используйте кнопки меню."
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показывает статистику пользователя"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_scores:
            await update.message.reply_text("У вас еще нет статистики. Сыграйте в игры!")
            return
        
        stats = self.user_scores[user_id]
        total_games = sum(stats.values())
        
        stats_text = f"📊 *Ваша статистика:*\n\n"
        stats_text += f"Всего игр: {total_games}\n"
        
        for game, score in stats.items():
            game_name = {
                'guess_number': 'Угадай число',
                'rps': 'Камень-ножницы-бумага',
                'quiz': 'Викторина'
            }.get(game, game)
            
            stats_text += f"{game_name}: {score} побед\n"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')

    def get_main_menu_keyboard(self):
        """Создает клавиатуру главного меню"""
        keyboard = [
            [
                InlineKeyboardButton("🔢 Угадай число", callback_data='game_guess_number'),
                InlineKeyboardButton("✂️ Камень-ножницы-бумага", callback_data='game_rps')
            ],
            [
                InlineKeyboardButton("📚 Викторина", callback_data='game_quiz'),
                InlineKeyboardButton("📊 Статистика", callback_data='stats')
            ],
            [
                InlineKeyboardButton("❓ Помощь", callback_data='help'),
                InlineKeyboardButton("🚪 Выход", callback_data='cancel')
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        
        # Инициализация статистики пользователя, если нужно
        if user_id not in self.user_scores:
            self.user_scores[user_id] = {'guess_number': 0, 'rps': 0, 'quiz': 0}
        
        if query.data == 'stats':
            await self.stats_command_callback(query)
            return MAIN_MENU
            
        elif query.data == 'help':
            await query.edit_message_text(
                text="Выберите игру из меню:\n\n"
                     "1. 🔢 Угадай число - попробуйте угадать число от 1 до 100\n"
                     "2. ✂️ Камень-ножницы-бумага - классическая игра\n"
                     "3. 📚 Викторина - вопросы на общие знания",
                reply_markup=self.get_main_menu_keyboard()
            )
            return MAIN_MENU
            
        elif query.data == 'cancel':
            await query.edit_message_text(
                text="До свидания! Возвращайтесь скорее! 👋",
                reply_markup=self.get_main_menu_keyboard()
            )
            return MAIN_MENU
        
        # Запуск игры
        elif query.data.startswith('game_'):
            game_type = query.data.replace('game_', '')
            
            if game_type in self.games:
                self.current_game = self.games[game_type]
                game_state = self.current_game.start(user_id)
                
                await query.edit_message_text(
                    text=game_state['message'],
                    reply_markup=game_state.get('keyboard')
                )
                return PLAYING_GAME
        
        return MAIN_MENU

    async def stats_command_callback(self, query):
        """Показывает статистику в callback"""
        user_id = query.from_user.id
        
        if user_id not in self.user_scores:
            await query.edit_message_text(
                text="У вас еще нет статистики. Сыграйте в игры!",
                reply_markup=self.get_main_menu_keyboard()
            )
            return
        
        stats = self.user_scores[user_id]
        total_games = sum(stats.values())
        
        stats_text = f"📊 *Ваша статистика:*\n\n"
        stats_text += f"Всего игр: {total_games}\n\n"
        
        stats_text += "🔢 *Угадай число:* " + str(stats.get('guess_number', 0)) + " побед\n"
        stats_text += "✂️ *Камень-ножницы-бумага:* " + str(stats.get('rps', 0)) + " побед\n"
        stats_text += "📚 *Викторина:* " + str(stats.get('quiz', 0)) + " правильных ответов\n"
        
        await query.edit_message_text(
            text=stats_text,
            parse_mode='Markdown',
            reply_markup=self.get_main_menu_keyboard()
        )

    async def game_message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик сообщений во время игры"""
        if not self.current_game:
            await update.message.reply_text(
                "Выберите игру из меню:",
                reply_markup=self.get_main_menu_keyboard()
            )
            return MAIN_MENU
        
        user_id = update.effective_user.id
        user_input = update.message.text
        
        # Обработка команды отмены
        if user_input.lower() in ['/cancel', 'отмена', 'выйти']:
            await update.message.reply_text(
                "Игра отменена. Возвращаюсь в главное меню.",
                reply_markup=self.get_main_menu_keyboard()
            )
            self.current_game = None
            return MAIN_MENU
        
        # Обработка ввода в игре
        game_state = self.current_game.handle_input(user_id, user_input)
        
        if game_state['status'] == 'finished':
            # Обновляем статистику при победе
            if game_state.get('won'):
                game_type = self.get_game_type(self.current_game)
                if game_type and user_id in self.user_scores:
                    self.user_scores[user_id][game_type] += 1
            
            await update.message.reply_text(
                game_state['message'],
                reply_markup=self.get_main_menu_keyboard()
            )
            self.current_game = None
            return MAIN_MENU
        
        else:
            await update.message.reply_text(
                game_state['message'],
                reply_markup=game_state.get('keyboard')
            )
            return PLAYING_GAME

    def get_game_type(self, game_instance):
        """Определяет тип игры по экземпляру"""
        for game_type, game in self.games.items():
            if game == game_instance:
                return game_type
        return None

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена игры"""
        await update.message.reply_text(
            "Игра отменена. Возвращаюсь в главное меню.",
            reply_markup=self.get_main_menu_keyboard()
        )
        self.current_game = None
        return ConversationHandler.END

    def run(self):
        """Запуск бота"""
        application = Application.builder().token(self.token).build()
        
        # Conversation handler для управления состояниями
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                MAIN_MENU: [
                    CallbackQueryHandler(self.button_callback),
                    CommandHandler('help', self.help_command),
                    CommandHandler('stats', self.stats_command),
                ],
                PLAYING_GAME: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.game_message_handler),
                    CommandHandler('cancel', self.cancel),
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('help', self.help_command))
        application.add_handler(CommandHandler('stats', self.stats_command))
        
        logger.info("Бот запущен...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Точка входа в приложение"""
    # Для безопасности, токен лучше хранить в переменных окружения
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        print("Ошибка: TELEGRAM_BOT_TOKEN не найден в переменных окружения")
        print("Создайте файл .env и добавьте TELEGRAM_BOT_TOKEN=ваш_токен")
        return
    
    bot = MiniGamesBot(TOKEN)
    bot.run()

if __name__ == '__main__':
    main()
