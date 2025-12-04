import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    # Токен бота
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Настройки игр
    GAME_CONFIG = {
        'guess_number': {
            'min_number': 1,
            'max_number': 100,
            'max_attempts': 10
        },
        'rps': {
            'win_score': 2,
            'max_rounds': 3
        },
        'quiz': {
            'questions_per_game': 3,
            'passing_score': 0.7  # 70%
        }
    }
    
    # Сообщения
    MESSAGES = {
        'welcome': "👋 Добро пожаловать в мир мини-игр!",
        'help': "Выберите игру из меню ниже:",
        'error': "⚠️ Произошла ошибка. Попробуйте еще раз.",
        'goodbye': "👋 До новых встреч!"
    }
