from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random
from typing import Dict, Any, Optional

# Константы для состояний игр
GAME_STATES = {
    'GUESS_NUMBER': 'guess_number',
    'RPS': 'rock_paper_scissors',
    'QUIZ': 'quiz'
}

class BaseGame:
    """Базовый класс для всех игр"""
    
    def __init__(self):
        self.user_states = {}
    
    def start(self, user_id: int) -> Dict[str, Any]:
        """Начало игры"""
        raise NotImplementedError
    
    def handle_input(self, user_id: int, user_input: str) -> Dict[str, Any]:
        """Обработка ввода пользователя"""
        raise NotImplementedError
    
    def get_state(self, user_id: int) -> Optional[Dict]:
        """Получение состояния пользователя"""
        return self.user_states.get(user_id)
    
    def set_state(self, user_id: int, state: Dict):
        """Установка состояния пользователя"""
        self.user_states[user_id] = state
    
    def clear_state(self, user_id: int):
        """Очистка состояния пользователя"""
        if user_id in self.user_states:
            del self.user_states[user_id]

class GuessNumberGame(BaseGame):
    """Игра 'Угадай число'"""
    
    def __init__(self):
        super().__init__()
    
    def start(self, user_id: int) -> Dict[str, Any]:
        """Начало игры 'Угадай число'"""
        secret_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 10
        
        self.set_state(user_id, {
            'game_type': GAME_STATES['GUESS_NUMBER'],
            'secret_number': secret_number,
            'attempts': attempts,
            'max_attempts': max_attempts,
            'game_over': False
        })
        
        return {
            'message': (
                f"🎯 Я загадал число от 1 до 100!\n"
                f"У тебя {max_attempts} попыток, чтобы угадать.\n"
                f"Введи число или нажми кнопку 'Сдаться':"
            ),
            'keyboard': self._get_keyboard(),
            'status': 'playing'
        }
    
    def handle_input(self, user_id: int, user_input: str) -> Dict[str, Any]:
        """Обработка ввода в игре 'Угадай число'"""
        state = self.get_state(user_id)
        if not state or state['game_over']:
            return self._get_error_response()
        
        # Проверка на сдачу
        if user_input.lower() in ['сдаться', 'сдаюсь', 'выход']:
            self.clear_state(user_id)
            return {
                'message': f"😔 Жаль! Я загадал число {state['secret_number']}.\nВозвращаюсь в меню...",
                'status': 'finished',
                'won': False
            }
        
        # Проверка ввода числа
        try:
            guess = int(user_input)
        except ValueError:
            return {
                'message': "Пожалуйста, введите целое число!",
                'keyboard': self._get_keyboard(),
                'status': 'playing'
            }
        
        state['attempts'] += 1
        remaining = state['max_attempts'] - state['attempts']
        
        if guess < state['secret_number']:
            response = f"📈 Моё число БОЛЬШЕ! Осталось попыток: {remaining}"
        elif guess > state['secret_number']:
            response = f"📉 Моё число МЕНЬШЕ! Осталось попыток: {remaining}"
        else:
            self.clear_state(user_id)
            return {
                'message': f"🎉 Поздравляю! Ты угадал число {state['secret_number']} за {state['attempts']} попыток!",
                'status': 'finished',
                'won': True
            }
        
        # Проверка на исчерпание попыток
        if state['attempts'] >= state['max_attempts']:
            self.clear_state(user_id)
            return {
                'message': f"💀 Попытки закончились! Я загадал число {state['secret_number']}.",
                'status': 'finished',
                'won': False
            }
        
        self.set_state(user_id, state)
        
        return {
            'message': response,
            'keyboard': self._get_keyboard(),
            'status': 'playing'
        }
    
    def _get_keyboard(self):
        """Клавиатура для игры"""
        keyboard = [
            [InlineKeyboardButton("🚪 Сдаться", callback_data='surrender')]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def _get_error_response(self):
        """Ответ при ошибке состояния"""
        return {
            'message': "Произошла ошибка. Давай начнем новую игру!",
            'status': 'finished',
            'won': False
        }

class RockPaperScissorsGame(BaseGame):
    """Игра 'Камень-ножницы-бумага'"""
    
    CHOICES = {
        'камень': '✊',
        'ножницы': '✌️',
        'бумага': '✋'
    }
    
    WINNING_COMBINATIONS = {
        ('камень', 'ножницы'): True,
        ('ножницы', 'бумага'): True,
        ('бумага', 'камень'): True,
    }
    
    def __init__(self):
        super().__init__()
    
    def start(self, user_id: int) -> Dict[str, Any]:
        """Начало игры 'Камень-ножницы-бумага'"""
        self.set_state(user_id, {
            'game_type': GAME_STATES['RPS'],
            'score_user': 0,
            'score_bot': 0,
            'round': 1,
            'max_rounds': 3
        })
        
        return {
            'message': (
                "🎮 *Камень-ножницы-бумага!*\n\n"
                f"Играем до {3} побед!\n"
                "Выбери свой вариант:"
            ),
            'keyboard': self._get_keyboard(),
            'status': 'playing'
        }
    
    def handle_input(self, user_id: int, user_input: str) -> Dict[str, Any]:
        """Обработка ввода в игре 'Камень-ножницы-бумага'"""
        state = self.get_state(user_id)
        if not state:
            return self._get_error_response()
        
        # Проверка на выход
        if user_input.lower() in ['выход', 'стоп']:
            self.clear_state(user_id)
            return {
                'message': f"Игра завершена. Счет: {state['score_user']}:{state['score_bot']}",
                'status': 'finished',
                'won': state['score_user'] > state['score_bot']
            }
        
        # Проверка выбора пользователя
        user_choice = user_input.lower().strip()
        if user_choice not in self.CHOICES:
            return {
                'message': "Пожалуйста, выбери: камень, ножницы или бумага",
                'keyboard': self._get_keyboard(),
                'status': 'playing'
            }
        
        # Выбор бота
        bot_choice = random.choice(list(self.CHOICES.keys()))
        
        # Определение победителя
        if user_choice == bot_choice:
            result = "🤝 Ничья!"
        elif (user_choice, bot_choice) in self.WINNING_COMBINATIONS:
            result = "🎉 Ты выиграл этот раунд!"
            state['score_user'] += 1
        else:
            result = "🤖 Я выиграл этот раунд!"
            state['score_bot'] += 1
        
        state['round'] += 1
        
        # Формирование сообщения
        message = (
            f"Раунд {state['round'] - 1}:\n"
            f"Ты: {self.CHOICES[user_choice]} {user_choice}\n"
            f"Бот: {self.CHOICES[bot_choice]} {bot_choice}\n\n"
            f"{result}\n"
            f"Счет: {state['score_user']}:{state['score_bot']}"
        )
        
        # Проверка на конец игры
        if state['score_user'] >= 2 or state['score_bot'] >= 2:
            self.clear_state(user_id)
            
            if state['score_user'] > state['score_bot']:
                final_message = f"🏆 Ты выиграл игру! {state['score_user']}:{state['score_bot']}"
                won = True
            else:
                final_message = f"💀 Я выиграл игру! {state['score_user']}:{state['score_bot']}"
                won = False
            
            return {
                'message': final_message,
                'status': 'finished',
                'won': won
            }
        
        self.set_state(user_id, state)
        
        return {
            'message': message + "\n\nСледующий раунд:",
            'keyboard': self._get_keyboard(),
            'status': 'playing'
        }
    
    def _get_keyboard(self):
        """Клавиатура для игры"""
        keyboard = [
            [
                InlineKeyboardButton("✊ Камень", callback_data='камень'),
                InlineKeyboardButton("✌️ Ножницы", callback_data='ножницы'),
                InlineKeyboardButton("✋ Бумага", callback_data='бумага')
            ],
            [InlineKeyboardButton("🚪 Выход", callback_data='выход')]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def _get_error_response(self):
        """Ответ при ошибке состояния"""
        return {
            'message': "Произошла ошибка. Давай начнем новую игру!",
            'status': 'finished',
            'won': False
        }

class QuizGame(BaseGame):
    """Игра 'Викторина'"""
    
    QUIZ_QUESTIONS = [
        {
            'question': 'Какая планета самая большая в Солнечной системе?',
            'options': ['Земля', 'Марс', 'Юпитер', 'Сатурн'],
            'correct': 2  # Индекс правильного ответа (0-based)
        },
        {
            'question': 'Кто написал "Войну и мир"?',
            'options': ['Достоевский', 'Толстой', 'Чехов', 'Тургенев'],
            'correct': 1
        },
        {
            'question': 'Сколько континентов на Земле?',
            'options': ['5', '6', '7', '8'],
            'correct': 2
        },
        {
            'question': 'Какое химическое обозначение у золота?',
            'options': ['Go', 'Gd', 'Au', 'Ag'],
            'correct': 2
        },
        {
            'question': 'В каком году человек впервые полетел в космос?',
            'options': ['1957', '1961', '1969', '1975'],
            'correct': 1
        }
    ]
    
    def __init__(self):
        super().__init__()
    
    def start(self, user_id: int) -> Dict[str, Any]:
        """Начало викторины"""
        questions = self.QUIZ_QUESTIONS.copy()
        random.shuffle(questions)
        
        self.set_state(user_id, {
            'game_type': GAME_STATES['QUIZ'],
            'questions': questions,
            'current_question': 0,
            'score': 0,
            'total_questions': min(3, len(questions))  # Ограничиваем 3 вопросами
        })
        
        return self._get_next_question(user_id)
    
    def handle_input(self, user_id: int, user_input: str) -> Dict[str, Any]:
        """Обработка ответа в викторине"""
        state = self.get_state(user_id)
        if not state:
            return self._get_error_response()
        
        # Проверка на выход
        if user_input.lower() in ['выход', 'стоп']:
            self.clear_state(user_id)
            return {
                'message': f"Викторина завершена. Правильных ответов: {state['score']}/{state['current_question']}",
                'status': 'finished',
                'won': False
            }
        
        # Проверка ответа
        try:
            answer_index = int(user_input) - 1  # Пользователь вводит 1-4
            current_q = state['questions'][state['current_question']]
            
            if answer_index == current_q['correct']:
                state['score'] += 1
                result = "✅ Правильно!"
            else:
                correct_answer = current_q['options'][current_q['correct']]
                result = f"❌ Неправильно! Правильный ответ: {correct_answer}"
            
            state['current_question'] += 1
            
            # Проверка на конец викторины
            if state['current_question'] >= state['total_questions']:
                self.clear_state(user_id)
                percentage = (state['score'] / state['total_questions']) * 100
                
                if percentage >= 70:
                    rating = "Отлично! 🏆"
                    won = True
                elif percentage >= 40:
                    rating = "Хорошо! 👍"
                    won = True
                else:
                    rating = "Можно лучше! 📚"
                    won = False
                
                return {
                    'message': (
                        f"📊 Викторина завершена!\n\n"
                        f"Правильных ответов: {state['score']}/{state['total_questions']}\n"
                        f"Процент: {percentage:.0f}%\n"
                        f"{rating}"
                    ),
                    'status': 'finished',
                    'won': won
                }
            
            self.set_state(user_id, state)
            
            # Получаем следующий вопрос
            next_question_response = self._get_next_question(user_id)
            next_question_response['message'] = f"{result}\n\n{next_question_response['message']}"
            return next_question_response
            
        except (ValueError, IndexError):
            return {
                'message': "Пожалуйста, введите номер ответа (1-4)",
                'keyboard': self._get_keyboard(state['questions'][state['current_question']]),
                'status': 'playing'
            }
    
    def _get_next_question(self, user_id: int) -> Dict[str, Any]:
        """Получение следующего вопроса"""
        state = self.get_state(user_id)
        if not state or state['current_question'] >= len(state['questions']):
            return self._get_error_response()
        
        question_data = state['questions'][state['current_question']]
        
        message = (
            f"Вопрос {state['current_question'] + 1}/{state['total_questions']}:\n"
            f"🎓 {question_data['question']}\n\n"
        )
        
        # Добавляем варианты ответов
        for i, option in enumerate(question_data['options'], 1):
            message += f"{i}. {option}\n"
        
        return {
            'message': message,
            'keyboard': self._get_keyboard(question_data),
            'status': 'playing'
        }
    
    def _get_keyboard(self, question_data: Dict) -> InlineKeyboardMarkup:
        """Клавиатура для викторины"""
        keyboard = []
        for i in range(len(question_data['options'])):
            keyboard.append([InlineKeyboardButton(f"Вариант {i+1}", callback_data=str(i+1))])
        
        keyboard.append([InlineKeyboardButton("🚪 Выход", callback_data='выход')])
        return InlineKeyboardMarkup(keyboard)
    
    def _get_error_response(self):
        """Ответ при ошибке состояния"""
        return {
            'message': "Произошла ошибка. Давай начнем новую игру!",
            'status': 'finished',
            'won': False
        }
