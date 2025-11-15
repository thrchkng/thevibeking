import random
import time
import os

class RussianRoulette:
    def __init__(self):
        self.chamber_size = 6
        self.bullet_position = random.randint(1, self.chamber_size)
        self.current_position = 1
        self.score = 0
        self.high_score = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_intro(self):
        print("=" * 50)
        print("       ИГРА: РУССКАЯ РУЛЕТКА")
        print("=" * 50)
        print("Правила:")
        print("- В барабане 6 патронов")
        print("- Один из них настоящий")
        print("- Вращайте барабан и нажимайте на спусковой крючок")
        print("- Если выстрела не произошло, вы получаете очко")
        print("- Игра продолжается до выстрела")
        print("- Ставьте рекорды!")
        print("=" * 50)
        input("Нажмите Enter чтобы начать...")
    
    def spin_chamber(self):
        self.bullet_position = random.randint(1, self.chamber_size)
        self.current_position = random.randint(1, self.chamber_size)
        print("\nБарабан вращается...")
        time.sleep(2)
        print(f"Барабан остановился на позиции {self.current_position}")
    
    def pull_trigger(self):
        print("\nВы подносите пистолет к виску...")
        time.sleep(1)
        print("Палец на спусковом крючке...")
        time.sleep(1)
        
        if self.current_position == self.bullet_position:
            print("💥 БАБАХ! 💥")
            print("К сожалению, этот патрон был настоящим...")
            return True
        else:
            print("💨 *щелк*")
            print("Пустой патрон! Вы выжили!")
            self.score += 1
            self.current_position = (self.current_position % self.chamber_size) + 1
            return False
    
    def display_status(self):
        print(f"\nТекущий счет: {self.score}")
        print(f"Рекорд: {self.high_score}")
        print(f"Текущая позиция барабана: {self.current_position}/{self.chamber_size}")
    
    def play_round(self):
        self.clear_screen()
        self.display_status()
        
        print("\nВыберите действие:")
        print("1 - Вращать барабан и выстрелить")
        print("2 - Выстрелить без вращения")
        print("3 - Выйти из игры")
        
        choice = input("\nВаш выбор (1-3): ")
        
        if choice == '1':
            self.spin_chamber()
            return self.pull_trigger()
        elif choice == '2':
            return self.pull_trigger()
        elif choice == '3':
            return None
        else:
            print("Неверный выбор! Попробуйте снова.")
            time.sleep(1)
            return False
    
    def game_over(self):
        print("\n" + "=" * 50)
        print("         ИГРА ОКОНЧЕНА!")
        print(f"Ваш результат: {self.score} выживших раундов")
        
        if self.score > self.high_score:
            self.high_score = self.score
            print("🎉 НОВЫЙ РЕКОРД! 🎉")
        
        print("=" * 50)
        
        play_again = input("\nХотите сыграть еще раз? (д/н): ").lower()
        return play_again in ['д', 'да', 'y', 'yes']
    
    def run(self):
        self.clear_screen()
        self.display_intro()
        
        while True:
            result = self.play_round()
            
            if result is None:
                break
            elif result:
                if not self.game_over():
                    break
                self.score = 0
                self.bullet_position = random.randint(1, self.chamber_size)
                self.current_position = 1

if __name__ == "__main__":
    print("Загрузка игры...")
    time.sleep(1)
    game = RussianRoulette()
    game.run()
    print("\nСпасибо за игру! Берегите себя!")