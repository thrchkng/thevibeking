import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.4
JUMP_STRENGTH = 10
PLATFORM_WIDTH = 70
PLATFORM_HEIGHT = 20
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
SCROLL_THRESHOLD = 200
PLATFORM_GAP = 100
PLATFORM_FREQUENCY = 0.8  # Вероятность появления платформы

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()

# Класс игрока
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = HEIGHT - 100
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_y = 0
        self.jumping = False
        
    def update(self, platforms):
        # Применение гравитации
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Проверка столкновения с платформами
        for platform in platforms:
            if (self.vel_y > 0 and 
                self.y + self.height >= platform.y and 
                self.y + self.height <= platform.y + 10 and
                self.x + self.width > platform.x and 
                self.x < platform.x + platform.width):
                self.vel_y = -JUMP_STRENGTH
                self.y = platform.y - self.height
        
        # Ограничение движения по горизонтали (выход за экран)
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
            
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        # Рисуем глаза для визуализации направления
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y + 15), 5)
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + 15), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 15), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 15), 2)
        
    def move(self, direction):
        if direction == "left":
            self.x -= 5
        elif direction == "right":
            self.x += 5

# Класс платформы
class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Функция создания начальных платформ
def create_initial_platforms():
    platforms = []
    # Стартовая платформа
    platforms.append(Platform(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 50))
    
    # Создаем платформы до верха экрана
    y = HEIGHT - 50 - PLATFORM_GAP
    while y > 0:
        if random.random() < PLATFORM_FREQUENCY:
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            platforms.append(Platform(x, y))
        y -= PLATFORM_GAP
    
    return platforms

# Основная функция игры
def main():
    player = Player()
    platforms = create_initial_platforms()
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
            
        # Обновление игрока
        player.update(platforms)
        
        # Прокрутка экрана вниз, когда игрок поднимается
        if player.y < SCROLL_THRESHOLD:
            scroll_amount = SCROLL_THRESHOLD - player.y
            player.y = SCROLL_THRESHOLD
            score += int(scroll_amount)
            
            # Перемещаем платформы вниз
            for platform in platforms:
                platform.y += scroll_amount
                
                # Удаляем платформы, которые ушли за нижнюю границу
                if platform.y > HEIGHT:
                    platforms.remove(platform)
                    
            # Добавляем новые платформы сверху
            while platforms[-1].y > 0:
                if random.random() < PLATFORM_FREQUENCY:
                    x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                    platforms.append(Platform(x, platforms[-1].y - PLATFORM_GAP))
        
        # Проверка проигрыша (падение вниз)
        if player.y > HEIGHT:
            running = False
            
        # Отрисовка
        screen.fill(WHITE)
        
        # Рисуем платформы
        for platform in platforms:
            platform.draw()
            
        # Рисуем игрока
        player.draw()
        
        # Рисуем счет
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # Экран окончания игры
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to restart or Q to quit", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()  # Перезапуск игры
                if event.key == pygame.K_q:
                    waiting = False
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()