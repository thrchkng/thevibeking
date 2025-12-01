import time
import random

class TextQuest:
    def __init__(self):
        self.health = 100
        self.inventory = []
        self.game_over = False
        self.current_room = "начало"
        
    def clear_screen(self):
        print("\n" * 50)
    
    def print_slow(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def show_status(self):
        print(f"\n{'='*50}")
        print(f"❤️  Здоровье: {self.health}/100")
        print(f"🎒 Инвентарь: {', '.join(self.inventory) if self.inventory else 'пусто'}")
        print(f"{'='*50}\n")
    
    def take_damage(self, amount):
        self.health -= amount
        self.print_slow(f"💔 Вы получили {amount} урона!")
        if self.health <= 0:
            self.print_slow("☠️  Вы погибли...")
            self.game_over = True
    
    def heal(self, amount):
        self.health = min(100, self.health + amount)
        self.print_slow(f"💚 Вы восстановили {amount} здоровья!")
    
    def add_item(self, item):
        self.inventory.append(item)
        self.print_slow(f"🎁 Вы получили: {item}")
    
    def has_item(self, item):
        return item in self.inventory
    
    def show_choices(self, choices):
        self.print_slow("\nВаши действия:")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice['text']}")
        
        while True:
            try:
                choice = int(input("\nВаш выбор (1-" + str(len(choices)) + "): "))
                if 1 <= choice <= len(choices):
                    return choices[choice-1]
                else:
                    print("Пожалуйста, выберите существующий вариант.")
            except ValueError:
                print("Пожалуйста, введите число.")
    
    def intro(self):
        self.clear_screen()
        self.print_slow("="*50)
        self.print_slow("          ПРИКЛЮЧЕНИЯ В ЗАБРОШЕННОМ ЗАМКЕ")
        self.print_slow("="*50)
        time.sleep(1)
        
        self.print_slow("\nВы стоите у входа в старый заброшенный замок...")
        self.print_slow("Легенды гласят, что внутри хранятся несметные сокровища.")
        self.print_slow("Но будьте осторожны - замок полон опасностей!")
        time.sleep(2)
        
        input("\nНажмите Enter, чтобы начать приключение...")
        self.room_entrance()
    
    def room_entrance(self):
        self.current_room = "вход"
        self.clear_screen()
        self.print_slow("\nВы стоите перед массивными дубовыми дверями замка.")
        self.print_slow("Двери слегка приоткрыты, изнутри доносится странный шум.")
        self.show_status()
        
        choices = [
            {
                "text": "Войти в замок",
                "action": self.room_main_hall
            },
            {
                "text": "Осмотреть двор",
                "action": self.room_yard
            },
            {
                "text": "Уйти прочь (закончить игру)",
                "action": self.end_game
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def room_yard(self):
        self.clear_screen()
        self.print_slow("\nВы обходите замок и находитесь во внутреннем дворе.")
        self.print_slow("Здесь есть колодец и старая кузница.")
        
        if not self.has_item("факел"):
            self.print_slow("В кузнице вы находите старый факел.")
            self.add_item("факел")
        
        choices = [
            {
                "text": "Заглянуть в колодец",
                "action": self.well_event
            },
            {
                "text": "Вернуться ко входу",
                "action": self.room_entrance
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def well_event(self):
        self.print_slow("\nВы заглядываете в колодец...")
        time.sleep(1)
        
        if random.random() < 0.3:
            self.print_slow("Из колодца вылетает стая летучих мышей!")
            self.take_damage(15)
        elif random.random() < 0.5:
            self.print_slow("В колодце вы находите монету!")
            self.add_item("золотая монета")
        else:
            self.print_slow("Колодец пуст и лишь эхо отвечает вам.")
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_yard()
    
    def room_main_hall(self):
        self.current_room = "главный зал"
        self.clear_screen()
        self.print_slow("\nВы входите в огромный главный зал замка.")
        self.print_slow("Пыльные гобелены висят на стенах, а в конце зала вы видите три двери.")
        
        if not self.has_item("карта"):
            self.print_slow("На полу лежит старая карта!")
            self.add_item("карта")
        
        self.show_status()
        
        choices = [
            {
                "text": "Пойти в левую дверь",
                "action": self.room_library
            },
            {
                "text": "Пойти в правую дверь",
                "action": self.room_kitchen
            },
            {
                "text": "Пойти в центральную дверь",
                "action": self.room_dungeon
            },
            {
                "text": "Вернуться к входу",
                "action": self.room_entrance
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def room_library(self):
        self.clear_screen()
        self.print_slow("\nВы попадаете в огромную библиотеку.")
        self.print_slow("Тысячи старых книг покрыты толстым слоем пыли.")
        
        if random.random() < 0.4:
            self.print_slow("На полке вы находите книгу заклинаний!")
            self.add_item("книга заклинаний")
        elif random.random() < 0.3:
            self.print_slow("Падающая книга чуть не попадает вам по голове!")
            self.take_damage(5)
        
        choices = [
            {
                "text": "Искать полезные книги",
                "action": self.search_books
            },
            {
                "text": "Вернуться в главный зал",
                "action": self.room_main_hall
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def search_books(self):
        self.print_slow("\nВы тщательно обыскиваете полки...")
        time.sleep(2)
        
        found = random.choice([
            ("Вы находите руководство по выживанию!", "Восстанавливаете 20 здоровья.", lambda: self.heal(20)),
            ("Вы находите дневник предыдущего исследователя!", "Узнаете секреты замка.", None),
            ("Книжная полка обваливается!", "Получаете 10 урона.", lambda: self.take_damage(10)),
            ("Ничего интересного не найдено.", "", None)
        ])
        
        self.print_slow(found[0])
        if found[1]:
            self.print_slow(found[1])
        if found[2]:
            found[2]()
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_library()
    
    def room_kitchen(self):
        self.clear_screen()
        self.print_slow("\nВы в старой кухне замка.")
        self.print_slow("Здесь стоит запах гнили и плесени.")
        
        if not self.has_item("нож"):
            self.print_slow("На столе вы находите острый нож.")
            self.add_item("нож")
        
        self.print_slow("Из кладовой доносятся странные звуки...")
        
        choices = [
            {
                "text": "Исследовать кладовую",
                "action": self.pantry_event
            },
            {
                "text": "Взять припасы со стола",
                "action": self.take_supplies
            },
            {
                "text": "Вернуться в главный зал",
                "action": self.room_main_hall
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def take_supplies(self):
        self.print_slow("\nВы находите немного старой еды...")
        
        if random.random() < 0.5:
            self.print_slow("Еда оказалась испорченной! Вы отравлены.")
            self.take_damage(25)
        else:
            self.print_slow("Вы нашли съедобные припасы!")
            self.heal(15)
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_kitchen()
    
    def pantry_event(self):
        self.print_slow("\nВы осторожно открываете дверь в кладовую...")
        time.sleep(1)
        
        if self.has_item("нож"):
            self.print_slow("Там сидит гигантская крыса! Но у вас есть нож...")
            self.print_slow("Вы побеждаете крысу и находите сокровище!")
            self.add_item("драгоценный камень")
        else:
            self.print_slow("Гигантская крыса нападает на вас!")
            self.take_damage(30)
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_kitchen()
    
    def room_dungeon(self):
        self.clear_screen()
        self.print_slow("\nВы спускаетесь в темное подземелье...")
        
        if not self.has_item("факел"):
            self.print_slow("Без факела вы ничего не видите!")
            self.print_slow("Вы спотыкаетесь и падаете.")
            self.take_damage(20)
            input("\nНажмите Enter, чтобы вернуться...")
            self.room_main_hall()
            return
        
        self.print_slow("При свете факела вы видите сундук в углу.")
        
        choices = [
            {
                "text": "Открыть сундук",
                "action": self.open_chest
            },
            {
                "text": "Осмотреть подземелье",
                "action": self.explore_dungeon
            },
            {
                "text": "Вернуться наверх",
                "action": self.room_main_hall
            }
        ]
        
        choice = self.show_choices(choices)
        choice["action"]()
    
    def open_chest(self):
        self.print_slow("\nВы открываете старый сундук...")
        time.sleep(2)
        
        if random.random() < 0.7:
            self.print_slow("В сундуке вы находите сокровище!")
            self.add_item("сундук с золотом")
            self.print_slow("🎉 ПОЗДРАВЛЯЕМ! ВЫ НАШЛИ СОКРОВИЩА ЗАМКА!")
            self.game_over = True
            self.end_game()
        else:
            self.print_slow("Сундук оказался ловушкой!")
            self.take_damage(40)
            input("\nНажмите Enter, чтобы продолжить...")
            self.room_dungeon()
    
    def explore_dungeon(self):
        self.print_slow("\nВы исследуете дальние уголки подземелья...")
        time.sleep(2)
        
        event = random.choice([
            ("Вы находите тайный проход!", self.secret_passage),
            ("На вас нападает призрак!", self.ghost_attack),
            ("Вы находите лечебное зелье!", self.find_potion)
        ])
        
        self.print_slow(event[0])
        event[1]()
    
    def secret_passage(self):
        self.print_slow("Проход ведет к сокровищнице!")
        self.add_item("королевская корона")
        self.print_slow("🏆 ВЫ ПОБЕДИЛИ! НАЙДЕНЫ КОРОЛЕВСКИЕ СОКРОВИЩА!")
        self.game_over = True
        self.end_game()
    
    def ghost_attack(self):
        if self.has_item("книга заклинаний"):
            self.print_slow("Вы используете заклинание из книги и прогоняете призрака!")
            self.add_item("призрачная эссенция")
        else:
            self.print_slow("Призрак атакует вас!")
            self.take_damage(35)
        
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_dungeon()
    
    def find_potion(self):
        self.print_slow("Зелье восстанавливает ваше здоровье!")
        self.heal(40)
        input("\nНажмите Enter, чтобы продолжить...")
        self.room_dungeon()
    
    def end_game(self):
        self.clear_screen()
        self.print_slow("\n" + "="*50)
        self.print_slow("                ИГРА ОКОНЧЕНА")
        self.print_slow("="*50)
        
        self.print_slow(f"\nВаш финальный статус:")
        self.print_slow(f"Здоровье: {self.health}")
        self.print_slow(f"Собранные предметы: {', '.join(self.inventory)}")
        
        score = self.health + len(self.inventory) * 10
        self.print_slow(f"\n🏅 Ваш счет: {score}")
        
        if score > 100:
            self.print_slow("🎖️  Отличный результат! Вы мастер приключений!")
        elif score > 50:
            self.print_slow("👍 Хорошая попытка!")
        else:
            self.print_slow("💪 В следующий раз получится лучше!")
        
        self.print_slow("\nСпасибо за игру!")
    
    def play(self):
        self.intro()
        while not self.game_over:
            time.sleep(0.1)

# Запуск игры
if __name__ == "__main__":
    game = TextQuest()
    game.play()
