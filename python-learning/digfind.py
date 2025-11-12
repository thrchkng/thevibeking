def find_digit_simple_explained(n):
    # Создаем строку-последовательность
    sequence = ""
    current_number = 1
    
    # Продолжаем добавлять числа, пока не достигнем нужной позиции
    while len(sequence) < n:
        sequence += str(current_number)
        current_number += 1
    
    # n-1 потому что индексы в Python начинаются с 0
    digit = sequence[n-1]
    
    print(f"Последовательность до позиции {n}: ...{sequence[max(0, n-10):n+5]}...")
    print(f"Цифра на позиции {n}: {digit} (из числа {current_number-1})")
    
    return int(digit)

# Примеры использования
if __name__ == "__main__":
    # Быстрые примеры
    examples = [1, 5, 10, 15, 20, 100]
    
    for pos in examples:
        digit = find_digit_at_position(pos)
        print(f"Позиция {pos}: цифра {digit}")
