import random

def get_words():
    """
    Возвращает список слов для игры
    """
    return ["python", "programming", "computer", "algorithm", "variable", "function", "loop"]

def choose_word(words):
    """
    Выбирает случайное слово из списка
    """
    return random.choice(words)

def display_word(word, guessed_letters):
    """
    Отображает текущее состояние слова:
    угаданные буквы показываются, неугаданные заменяются на '_'
    """
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def display_hangman(mistakes):
    """
    Возвращает ASCII-графику виселицы в зависимости от количества ошибок
    """
    stages = [
        # 0 ошибок - пустая виселица
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        # 1 ошибка - голова
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        # 2 ошибки - туловище
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        # 3 ошибки - одна рука
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        # 4 ошибки - обе руки
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        # 5 ошибок - одна нога
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        # 6 ошибок - полная фигура (проигрыш)
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """
    ]
    return stages[mistakes]

def get_letter(guessed_letters):
    """
    Получает букву от пользователя с проверкой ввода
    """
    while True:
        letter = input("Введите букву: ").lower()
        
        # Проверка на одну букву
        if len(letter) != 1:
            print("Пожалуйста, введите только одну букву.")
        # Проверка, что введена буква
        elif not letter.isalpha():
            print("Пожалуйста, введите букву.")
        # Проверка, что буква еще не вводилась
        elif letter in guessed_letters:
            print("Вы уже вводили эту букву.")
        else:
            return letter

def check_win(word, guessed_letters):
    """
    Проверяет, угадано ли все слово
    """
    return all(letter in guessed_letters for letter in word)

def play_game():
    """
    Основная функция игры, управляет игровым процессом
    """
    # Инициализация игры
    words = get_words()
    word = choose_word(words)
    guessed_letters = set()  # Множество для хранения угаданных букв
    mistakes = 0
    max_mistakes = 6  # Максимальное количество ошибок
    
    print("Добро пожаловать в игру 'Виселица'!")
    
    # Главный игровой цикл
    while mistakes < max_mistakes:
        # Отображение текущего состояния
        print("\n" + display_hangman(mistakes))
        print("Слово:", display_word(word, guessed_letters))
        print("Ошибки:", mistakes)
        print("Использованные буквы:", ", ".join(sorted(guessed_letters)))
        
        # Получение буквы от игрока
        letter = get_letter(guessed_letters)
        guessed_letters.add(letter)
        
        # Проверка угаданной буквы
        if letter in word:
            print("Правильно! Буква есть в слове.")
        else:
            print("Неправильно! Такой буквы нет в слове.")
            mistakes += 1
        
        # Проверка победы
        if check_win(word, guessed_letters):
            print("\nПоздравляем! Вы выиграли!")
            print("Загаданное слово:", word)
            break
    else:
        # Этот блок выполняется, если цикл завершился не через break
        print("\n" + display_hangman(mistakes))
        print("Игра окончена! Вы проиграли.")
        print("Загаданное слово было:", word)

# Точка входа в программу
if __name__ == "__main__":
    play_game()