import random
import string
import secrets
import pyperclip  # для копирования в буфер обмена

def generate_secure_password(length=16, use_uppercase=True, use_lowercase=True, 
                           use_digits=True, use_special=False):
    """
    Генерирует безопасный пароль с настройками
    
    Args:
        length: длина пароля
        use_uppercase: использовать заглавные буквы
        use_lowercase: использовать строчные буквы  
        use_digits: использовать цифры
        use_special: использовать специальные символы
    """
    
    # Собираем доступные символы
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Проверяем, что хоть один набор символов выбран
    if not characters:
        raise ValueError("Должен быть выбран хотя бы один тип символов")
    
    # Гарантируем, что пароль содержит хотя бы по одному символу из каждого выбранного типа
    password = []
    
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Заполняем оставшуюся длину случайными символами
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(secrets.choice(characters))
    
    # Перемешиваем пароль
    random.shuffle(password)
    
    return ''.join(password)

def password_strength(password):
    """Оценивает сложность пароля"""
    score = 0
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    if len(password) >= 12:
        score += 1
    
    strength = ["Очень слабый", "Слабый", "Средний", "Хороший", "Отличный", "Отличный"]
    return strength[min(score, 5)]

def main():
    print("=== Генератор паролей ===")
    
    try:
        length = int(input("Длина пароля (рекомендуется 12+): ") or 16)
        use_upper = input("Заглавные буквы? (y/n, по умолчанию y): ").lower() != 'n'
        use_lower = input("Строчные буквы? (y/n, по умолчанию y): ").lower() != 'n'
        use_digits = input("Цифры? (y/n, по умолчанию y): ").lower() != 'n'
        use_special = input("Специальные символы? (y/n, по умолчанию n): ").lower() == 'y'
        
        count = int(input("Сколько паролей сгенерировать? (по умолчанию 1): ") or 1)
        
        print("\n" + "="*50)
        
        for i in range(count):
            password = generate_secure_password(
                length=length,
                use_uppercase=use_upper,
                use_lowercase=use_lower,
                use_digits=use_digits,
                use_special=use_special
            )
            
            strength = password_strength(password)
            print(f"Пароль {i+1}: {password}")
            print(f"Сложность: {strength}")
            print("-" * 30)
        
        # Пытаемся скопировать последний пароль в буфер обмена
        try:
            pyperclip.copy(password)
            print("✓ Последний пароль скопирован в буфер обмена!")
        except:
            print("ℹ Не удалось скопировать в буфер обмена (установите pyperclip: pip install pyperclip)")
            
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
