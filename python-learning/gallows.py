import random

def get_words():
    return ["python", "programming", "computer", "algorithm", "variable", "function", "loop"]

def choose_word(words):
    return random.choice(words)

def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def display_hangman(mistakes):
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
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
    while True:
        letter = input("Введите букву: ").lower()
        if len(letter) != 1:
            print("Пожалуйста, введите только одну букву.")
        elif not letter.isalpha():
            print("Пожалуйста, введите букву.")
        elif letter in guessed_letters:
            print("Вы уже вводили эту букву.")
        else:
            return letter

def check_win(word, guessed_letters):
    return all(letter in guessed_letters for letter in word)

def play_game():
    words = get_words()
    word = choose_word(words)
    guessed_letters = set()
    mistakes = 0
    max_mistakes = 6
    
    print("Добро пожаловать в игру 'Виселица'!")
    
    while mistakes < max_mistakes:
        print("\n" + display_hangman(mistakes))
        print("Слово:", display_word(word, guessed_letters))
        print("Ошибки:", mistakes)
        print("Использованные буквы:", ", ".join(sorted(guessed_letters)))
        
        letter = get_letter(guessed_letters)
        guessed_letters.add(letter)
        
        if letter in word:
            print("Правильно! Буква есть в слове.")
        else:
            print("Неправильно! Такой буквы нет в слове.")
            mistakes += 1
        
        if check_win(word, guessed_letters):
            print("\nПоздравляем! Вы выиграли!")
            print("Загаданное слово:", word)
            break
    else:
        print("\n" + display_hangman(mistakes))
        print("Игра окончена! Вы проиграли.")
        print("Загаданное слово было:", word)

if __name__ == "__main__":
    play_game()