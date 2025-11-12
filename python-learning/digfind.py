def find_digit_at_position(n):
    if n <= 0:
        raise ValueError("Позиция должна быть положительным числом")
    
    digit_length = 1
    numbers_count = 9
    start_number = 1
    
    while n > digit_length * numbers_count:
        n -= digit_length * numbers_count
        digit_length += 1
        numbers_count *= 10
        start_number *= 10
    
    target_number = start_number + (n - 1) // digit_length
    digit_position = (n - 1) % digit_length
    
    return int(str(target_number)[digit_position])

def find_digit_at_position_simple(n):
    sequence = ""
    i = 1
    
    while len(sequence) < n:
        sequence += str(i)
        i += 1
    
    return int(sequence[n-1])

def test_functions():
    test_cases = [
        (1, 1),
        (5, 5),
        (10, 1),
        (15, 2),
        (100, 5),
    ]
    
    print("Тестирование функций:")
    print("Позиция | Ожидаемая | Алгоритм | Простая")
    print("-" * 40)
    
    for pos, expected in test_cases:
        result1 = find_digit_at_position(pos)
        result2 = find_digit_at_position_simple(pos)
        print(f"{pos:7} | {expected:9} | {result1:8} | {result2:7}")

def interactive_mode():
    print("=== Поиск цифры в последовательности натуральных чисел ===")
    print("Последовательность: 1 2 3 4 5 6 7 8 9 10 11 12 ...")
    
    while True:
        try:
            n = int(input("\nВведите позицию (0 для выхода): "))
            if n == 0:
                break
            
            if n < 1:
                print("Позиция должна быть положительным числом!")
                continue
            
            digit = find_digit_at_position(n)
            
            print(f"\nЦифра на позиции {n}: {digit}")
            
            if n <= 50:
                sequence = ""
                i = 1
                while len(sequence) < min(n + 10, 100):
                    sequence += str(i)
                    i += 1
                
                context_start = max(0, n - 5)
                context_end = min(len(sequence), n + 5)
                context = sequence[context_start:context_end]
                
                pointer = " " * (n - context_start - 1) + "↑"
                print(f"Контекст: ...{context}...")
                print(f"         {pointer}")
        
        except ValueError:
            print("Пожалуйста, введите целое число!")
        except Exception as e:
            print(f"Ошибка: {e}")

import time

def benchmark_functions():
    test_positions = [100, 1000, 10000, 50000]
    
    print("\nСравнение производительности:")
    print("Позиция | Алгоритм (мс) | Простая (мс)")
    print("-" * 35)
    
    for pos in test_positions:
        start = time.time()
        result1 = find_digit_at_position(pos)
        time1 = (time.time() - start) * 1000
        
        if pos <= 10000:
            start = time.time()
            result2 = find_digit_at_position_simple(pos)
            time2 = (time.time() - start) * 1000
        else:
            time2 = "N/A"
        
        print(f"{pos:7} | {time1:12.3f} | {time2}")

if __name__ == "__main__":
    test_functions()
    benchmark_functions()
    interactive_mode()
