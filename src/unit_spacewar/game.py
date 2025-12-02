import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Космический шутер")
clock = pygame.time.Clock()

# Загрузка изображений
def load_images():
    images = {}
    
    # Космолет игрока (простые геометрические формы)
    images['player'] = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.polygon(images['player'], BLUE, [(20, 0), (0, 30), (40, 30)])
    pygame.draw.rect(images['player'], GREEN, (15, 10, 10, 20))
    
    # Вражеский корабль
    images['enemy'] = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.polygon(images['enemy'], RED, [(0, 0), (40, 0), (20, 30)])
    pygame.draw.rect(images['enemy'], YELLOW, (15, 5, 10, 15))
    
    # Пуля игрока
    images['bullet'] = pygame.Surface((4, 15), pygame.SRCALPHA)
    pygame.draw.rect(images['bullet'], GREEN, (0, 0, 4, 15))
    pygame.draw.rect(images['bullet'], YELLOW, (0, 5, 4, 5))
    
    # Вражеская пуля
    images['enemy_bullet'] = pygame.Surface((6, 12), pygame.SRCALPHA)
    pygame.draw.rect(images['enemy_bullet'], RED, (0, 0, 6, 12))
    
    # Фоновые звезды
    images['star_small'] = pygame.Surface((2, 2))
    images['star_small'].fill(WHITE)
    images['star_medium'] = pygame.Surface((3, 3))
    images['star_medium'].fill(YELLOW)
    images['star_large'] = pygame.Surface((4, 4))
    images['star_large'].fill(WHITE)
    
    return images

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.bullets = []
        self.shoot_cooldown = 0
        self.health = 100
        self.score = 0
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.bullets.append(Bullet(self.x + self.width // 2 - 2, self.y))
            self.shoot_cooldown = 10  # Задержка между выстрелами
            
    def update(self):
        # Обновление задержки выстрела
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bbullet)
                
    def draw(self, screen, images):
        screen.blit(images['player'], (self.x, self.y))
        
        # Отображение пуль
        for bullet in self.bullets:
            bullet.draw(screen, images)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Класс пули
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 10
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen, images):
        screen.blit(images['bullet'], (self.x, self.y))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Класс врага
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = random.uniform(1.0, 3.0)
        self.bullets = []
        self.shoot_chance = 0.005  # Вероятность выстрела за кадр
        self.health = 30
        
    def update(self):
        self.y += self.speed
        
        # Случайный выстрел
        if random.random() < self.shoot_chance:
            self.shoot()
            
        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
                
    def shoot(self):
        self.bullets.append(EnemyBullet(self.x + self.width // 2 - 3, self.y + self.height))
        
    def draw(self, screen, images):
        screen.blit(images['enemy'], (self.x, self.y))
        
        # Отображение пуль
        for bullet in self.bullets:
            bullet.draw(screen, images)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Класс вражеской пули
class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 12
        self.speed = 5
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen, images):
        screen.blit(images['enemy_bullet'], (self.x, self.y))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Класс звезды для фона
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2.5)
        self.size = random.choice(['small', 'medium', 'large'])
        
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
            
    def draw(self, screen, images):
        if self.size == 'small':
            screen.blit(images['star_small'], (self.x, self.y))
        elif self.size == 'medium':
            screen.blit(images['star_medium'], (self.x, self.y))
        else:
            screen.blit(images['star_large'], (self.x, self.y))

# Основная функция игры
def main():
    images = load_images()
    player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100)
    enemies = []
    stars = [Star() for _ in range(100)]
    
    enemy_spawn_timer = 0
    game_over = False
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    
    # Главный игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        player.shoot()
                    else:
                        # Рестарт игры
                        player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 100)
                        enemies = []
                        game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        if not game_over:
            # Управление игроком
            keys = pygame.key.get_pressed()
            player.move(keys)
            
            # Автоматическая стрельба при удержании пробела
            if keys[pygame.K_SPACE]:
                player.shoot()
            
            # Обновление игрока
            player.update()
            
            # Спавн врагов
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= 30:  # Каждые 0.5 секунды при 60 FPS
                enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 40), -30))
                enemy_spawn_timer = 0
                
            # Обновление врагов
            for enemy in enemies[:]:
                enemy.update()
                
                # Проверка выхода за границы
                if enemy.y > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    continue
                    
                # Проверка столкновения пуль игрока с врагами
                for bullet in player.bullets[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        enemy.health -= 10
                        if bullet in player.bullets:
                            player.bullets.remove(bullet)
                            
                        if enemy.health <= 0:
                            player.score += 10
                            if enemy in enemies:
                                enemies.remove(enemy)
                
                # Проверка столкновения игрока с врагом
                if player.get_rect().colliderect(enemy.get_rect()):
                    player.health -= 20
                    if enemy in enemies:
                        enemies.remove(enemy)
                        
                # Проверка столкновения пуль врага с игроком
                for bullet in enemy.bullets[:]:
                    if bullet.get_rect().colliderect(player.get_rect()):
                        player.health -= 5
                        if bullet in enemy.bullets:
                            enemy.bullets.remove(bullet)
            
            # Обновление звезд
            for star in stars:
                star.update()
            
            # Проверка здоровья игрока
            if player.health <= 0:
                game_over = True
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Отрисовка звезд
        for star in stars:
            star.draw(screen, images)
        
        # Отрисовка игрока и врагов
        if not game_over:
            player.draw(screen, images)
            for enemy in enemies:
                enemy.draw(screen, images)
        
        # Отрисовка интерфейса
        # Здоровье
        health_text = font.render(f"Здоровье: {player.health}", True, GREEN)
        screen.blit(health_text, (10, 10))
        
        # Очки
        score_text = font.render(f"Очки: {player.score}", True, YELLOW)
        screen.blit(score_text, (10, 50))
        
        # Управление
        controls_text = small_font.render("Управление: Стрелки - движение, Пробел - стрельба, ESC - выход", True, WHITE)
        screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
        # Полоска здоровья
        pygame.draw.rect(screen, RED, (150, 15, 200, 20))
        pygame.draw.rect(screen, GREEN, (150, 15, max(0, player.health * 2), 20))
        pygame.draw.rect(screen, WHITE, (150, 15, 200, 20), 2)  # Рамка
        
        # Сообщение о конце игры
        if game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            restart_text = font.render("Нажмите ПРОБЕЛ для рестарта", True, YELLOW)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            final_score_text = font.render(f"Ваш счет: {player.score}", True, GREEN)
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
