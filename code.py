import pygame
import pygame as pg
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Размеры экрана
WIDTH, HEIGHT = 600, 400

GRIDSIZE = 20
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Шрифт для текста
font = pygame.font.SysFont('monospace', 36)

pause_flag = 0

current_background = 0
background_info_file = "background_info.txt"
background_images = ["background1.jpg", "background2.jpg", "background3.jpg"]
BACKGROUND_COLOR = background_images[current_background]

fon = pygame.image.load("fon.png")
start_fon = pygame.image.load("start_fon.png")

APPLE_IMAGE = [pygame.image.load("apple.png"), pygame.image.load("apple2.png")]

speed_snake = 5

sound1 = pg.mixer.Sound('bell.wav')
sound2 = pg.mixer.Sound('gameover.wav')
sound3 = pg.mixer.Sound('choice.wav')

# Класс для змейки
class Snake:
    def __init__(self):
        self.size = 4  # Изначальная длина змейки
        self.positions = [
            ((WIDTH // 2), (HEIGHT // 2) + i * GRIDSIZE) for i in range(self.size)
        ]
        self.direction = UP  # Изначальное направление вверх
        self.color = WHITE
        self.speed = 5
            
    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)

        self.positions.insert(0, new)
        if len(self.positions) > self.size:
            self.positions.pop()

    def reset(self):
        self.size = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:  # Голова змейки
                head_radius = GRIDSIZE // 2
                head_center = (p[0] + head_radius, p[1] + head_radius)

                # Создание повернутой головы
                pygame.draw.circle(surface, self.color, head_center, head_radius)
                tail_radius = GRIDSIZE // 2
                tail_direction = (
                self.positions[1][0] - self.positions[0][0], self.positions[1][1] - self.positions[0][1])
                tail_offset = (GRIDSIZE // 2)
                if tail_direction == (GRIDSIZE, 0):  # Движется влево
                    pygame.draw.rect(surface, self.color, [
                        (p[0] + tail_radius, p[1]),
                        (tail_radius, GRIDSIZE),
                    ])
                elif tail_direction == (-GRIDSIZE, 0):  # Движется вправо
                    pygame.draw.rect(surface, self.color, [
                        (p[0], p[1]),
                        (tail_radius, GRIDSIZE),
                    ])
                elif tail_direction == (0, GRIDSIZE):  # Движется вверх
                    pygame.draw.rect(surface, self.color, [
                        (p[0], p[1] + tail_radius),
                        (GRIDSIZE, tail_radius),
                    ])
                elif tail_direction == (0, -GRIDSIZE):  # Движется вниз
                    pygame.draw.rect(surface, self.color, [
                        (p[0], p[1]),
                        (GRIDSIZE, tail_radius),
                    ])

            elif i == len(self.positions) - 1:  # Хвост змейки
                tail_radius = GRIDSIZE // 2
                tail_direction = (
                self.positions[-1][0] - self.positions[-2][0], self.positions[-1][1] - self.positions[-2][1])
                tail_offset = (GRIDSIZE // 2)
                if tail_direction == (GRIDSIZE, 0):  # Движется влево
                    pygame.draw.polygon(surface, self.color, [
                        (p[0], p[1]),
                        (p[0], p[1] + GRIDSIZE - 1),
                        (p[0] + tail_radius, p[1] + tail_radius - 1)
                    ])
                elif tail_direction == (-GRIDSIZE, 0):  # Движется вправо
                    pygame.draw.polygon(surface, self.color, [
                        (p[0] + GRIDSIZE, p[1]),
                        (p[0] + GRIDSIZE, p[1] + GRIDSIZE - 1),
                        (p[0] + tail_radius, p[1] + tail_radius - 1)
                    ])
                elif tail_direction == (0, GRIDSIZE):  # Движется вверх
                    pygame.draw.polygon(surface, self.color, [
                        (p[0], p[1]),
                        (p[0] + 2 * tail_radius - 1, p[1]),
                        (p[0] + tail_radius, p[1] + tail_radius)
                    ])
                elif tail_direction == (0, -GRIDSIZE):  # Движется вниз
                    pygame.draw.polygon(surface, self.color, [
                        (p[0], p[1] + GRIDSIZE),
                        (p[0] + 2 * tail_radius - 1, p[1] + GRIDSIZE),
                        (p[0] + tail_radius, p[1] + tail_radius)
                    ])
            else:  # Тело змейки
                pygame.draw.rect(surface, self.color, (p[0], p[1], GRIDSIZE, GRIDSIZE))

    def get_head_angle(self):
        x, y = self.direction
        if x == 1:
            return 0
        elif x == -1:
            return 180
        elif y == 1:
            return 90
        elif y == -1:
            return -90
        return 0

    def get_tail_angle(self):
        dx = self.positions[-1][0] - self.positions[-2][0]
        dy = self.positions[-1][1] - self.positions[-2][1]
        return math.degrees(math.atan2(dy, dx))

    def get_body_angle(self, index):
        dx = self.positions[index + 1][0] - self.positions[index - 1][0]
        dy = self.positions[index + 1][1] - self.positions[index - 1][1]
        return math.degrees(math.atan2(dy, dx))


# Класс для еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.image = random.choice(APPLE_IMAGE)
        self.randomize_position()
        self.glow_counter = 0 # Начальное свечение
        self.max_glow_counter = 3
        self.glow_radius = 15  # Радиус свечения
        self.glow_color = (255, 255, 0, 200)

    def randomize_position(self):
        self.image = random.choice(APPLE_IMAGE)
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def update(self):
        # Обновление счетчика свечения
        self.glow_counter = (self.glow_counter + 1) % (2 * self.max_glow_counter)

    def render(self, surface):
        # Созддание круга для обозначения яблока
        glow_surface = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, self.glow_color, (self.glow_radius, self.glow_radius), self.glow_radius)

        # Эффект мерцания
        alpha = abs(self.glow_counter - self.max_glow_counter) / self.max_glow_counter * 255
        glow_surface.set_alpha(alpha)

        surface.blit(glow_surface, (self.position[0] - self.glow_radius + 10, self.position[1] - self.glow_radius + 10))
        surface.blit(self.image, (self.position[0], self.position[1]))


def choose_background():
    global current_background
    backgrounds_list = ['Камень', 'Трава', 'Грунт']
    while True:
        screen.blit(fon, (0, 0)) 
        draw_text(screen, "Выберите фон:", (50, 50))

        for i, image_path in enumerate(background_images):
            color = WHITE if i == current_background else RED
            draw_text(screen, backgrounds_list[i], (50, 100 + i * 50), color)

        draw_text(screen, ">", (30, 100 + current_background * 50), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_background = (current_background - 1) % len(background_images)
                elif event.key == pygame.K_DOWN:
                    current_background = (current_background + 1) % len(background_images)
                elif event.key == pygame.K_RETURN:
                    sound3.play()
                    save_background_info(current_background)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 100 <= pygame.mouse.get_pos()[1] <= 150:
                    sound3.play()
                    current_background = 0
                elif 150 <= pygame.mouse.get_pos()[1] <= 200:
                    sound3.play()
                    current_background = 1
                elif 200 <= pygame.mouse.get_pos()[1] <= 250:
                    sound3.play()
                    current_background = 2

def save_background_info(background_index):
    with open(background_info_file, "w") as file:
        file.write(str(background_index))

def show_background_menu():
    global current_background
    choose_background()

# Отрисовка текста
def draw_text(surface, text, pos, color=WHITE):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def draw_button(surface, text, position, action=None):
    button_font = pygame.font.SysFont('monospace', 24)
    button_text = button_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=position)

    pygame.draw.rect(surface, RED, (text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10))
    surface.blit(button_text, text_rect.topleft)

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if text_rect.collidepoint(mouse_pos) and mouse_click[0] == 1 and action:
        action()

# Функция для выбора уровня
def choose_level():
    global speed_snake
    levels = ["Уровень 1(с границами)", "Уровень 2(без границ)"]
    selected_level = 0

    while True:
        screen.blit(fon, (0, 0)) 
        draw_text(screen, "Выберите уровень:", (50, 50))

        for i, level in enumerate(levels):
            color = WHITE if i == selected_level else RED
            draw_text(screen, level, (50, 100 + i * 50), color)

        draw_text(screen, ">", (30, 100 + selected_level * 50), WHITE)

        draw_button(screen, "Выбрать фон", (300, 300), choose_background)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    sound3.play()
                    selected_speed = settings_menu()
                    speed_snake = selected_speed 
                    return selected_level


class AnimatedSplashApple:
    def __init__(self):
        self.position = (100, HEIGHT // 2)
        self.color = GREEN
        self.animation_duration = 1  # Длительность анимации
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.animation_duration:
            self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                             random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)
            self.start_time = current_time

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


class AnimatedSplashScreen:
    def __init__(self):
        self.snake = AnimatedSplashSnake()
        self.title_font_1 = pygame.font.SysFont('comicsansms', 72)
        self.title_font_2 = pygame.font.SysFont('consolas', 22)
        self.title_x = -270
        self.title_y = HEIGHT // 4
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if self.title_x <= 340:
            self.title_x += 3  # Изменение координаты X
        self.snake.update()
        
    def render(self, surface):
        screen.blit(start_fon, (0, 0)) 
        
        self.snake.render(surface)
        
        title_text_1 = self.title_font_1.render("SNAKE", True, WHITE)
        title_shadow_1 = self.title_font_1.render("SNAKE", True, (115, 115, 115))
        surface.blit(title_shadow_1, (self.title_x + 3, self.title_y + 3))
        surface.blit(title_text_1, (self.title_x, self.title_y))
        
        title_text_2 = self.title_font_2.render("Created by Maxim Nenashev & Darina Zelenkova", True, WHITE)
        title_shadow_2 = self.title_font_2.render("Created by Maxim Nenashev & Darina Zelenkova", True, (115, 115, 115))
        surface.blit(title_shadow_2, (self.title_x - 280, self.title_y + 102))
        surface.blit(title_text_2, (self.title_x - 281, self.title_y + 101))

# Класс для анимированной змейки на стартовом экране
class AnimatedSplashSnake:
    def __init__(self):
        self.size = 7
        self.positions = [
            (40, HEIGHT // 2 + i * GRIDSIZE) for i in range(self.size)
        ]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = WHITE
        self.change_direction_counter = random.randint(3, 6)

    def update(self):
        self.snake_change_direction()

        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
        self.positions.insert(0, new)
        if len(self.positions) > self.size:
            self.positions.pop()

    def snake_change_direction(self):
        self.change_direction_counter -= 1
        if self.change_direction_counter == 0:
            move = [UP, DOWN, LEFT, RIGHT]   
            # Изменение направления змейки на любое, кроме противоположного
            dict_check = (-self.direction[0], -self.direction[1])
            a = list(filter(lambda x: x != dict_check, move))
            self.direction = random.choice(a)
            self.change_direction_counter = random.randint(2, 4)

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRIDSIZE, GRIDSIZE))

# Функция для анимации змейки на стартовом экране
def draw_animated_splash_screen():
    animated_splash_screen = AnimatedSplashScreen()
    animated_splash_apple = AnimatedSplashApple()
    animated_splash_apple2 = AnimatedSplashApple()
    animated_splash_apple3 = AnimatedSplashApple()
    clock = pygame.time.Clock()
    waiting = True

    while waiting == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        animated_splash_apple.update()
        animated_splash_apple2.update()
        animated_splash_apple3.update()
        animated_splash_screen.update()

        screen.blit(fon, (0, 0)) 
        animated_splash_screen.render(screen)
        animated_splash_apple.render(screen)
        animated_splash_apple2.render(screen)
        animated_splash_apple3.render(screen)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sound3.play()
                    waiting = False


def draw_slider(screen, x, y, value, min_value, max_value, step):
    pygame.draw.rect(screen, WHITE, (x, y, 200, 20), 2)
    slider_pos = int((value - min_value) / (max_value - min_value) * 200)
    pygame.draw.rect(screen, RED, (x + slider_pos - 5, y - 5, 10, 30))

def settings_menu(initial_speed=5):
    selected_speed = initial_speed

    while True:
        screen.blit(fon, (0, 0)) 
        draw_text(screen, "Настройки", (50, 50), RED)

        # Отрисовка скорости (ползунок)
        draw_text(screen, f"Текущая скорость: {selected_speed}", (50, 100), WHITE)  # Вывод скорости
        draw_text(screen, "Выберите скорость:", (50, 150), WHITE)
        draw_slider(screen, 50, 200, selected_speed, 1, 10, 1)

        draw_text(screen, "Enter - начать игру", (50, 350), WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_speed = max(1, selected_speed - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_speed = min(10, selected_speed + 1)
                elif event.key == pygame.K_RETURN:
                    sound3.play()
                    if selected_speed >= 8:
                        pg.mixer.music.load('hard.ogg')
                    else:
                        pg.mixer.music.load('main.ogg')                        
                    return selected_speed

        pygame.time.delay(50)


# Основной игровой цикл
def main():
    global game_flag
    global snake_minus    
    game_flag = 1
    clock = pygame.time.Clock()
    selected_level = choose_level()
    
    background_color = BACKGROUND_COLOR
    try:
        with open(background_info_file, "r") as file:
            current_background = int(file.read())
            background_color = pygame.image.load(background_images[current_background])
    except FileNotFoundError:
        pass      
    
    if selected_level == 0:
        pg.mixer.music.play()
        # Уровень 1
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)            
            if game_flag == 1:
                snake.update()
                food.update()
                food.render(screen)    
                if snake.get_head_position() == food.position:
                    sound1.play()
                    snake.size += 1
                    food.randomize_position()
                    score += 1
    
                # Проверка столкновения головы змейки с телом
                if snake.get_head_position() in snake.positions[1:]:
                    game_over(score)
                    return
    
                # Проверка столкновения с краем экрана
                if (
                        snake.get_head_position()[0] == 0 and snake.positions[1][0] == WIDTH - 20
                        or snake.get_head_position()[0] == WIDTH - 20 and snake.positions[1][0] == 0
                        or snake.get_head_position()[1] == 0 and snake.positions[1][1] == HEIGHT - 20
                        or snake.get_head_position()[1] == HEIGHT - 20 and snake.positions[1][1] == 0
                ):
                    game_over(score)
                    return
    
                screen.blit(background_color, (0, 0))           
                snake.render(screen)
                food.render(screen)
    
                # Выводим количество очков на экран, рисуем кнопку паузы и границы
                pygame.draw.rect(screen, RED, (0, 0, 600, 400), 2)
                pygame.draw.rect(screen, WHITE, (570, 5, 5, 25))
                pygame.draw.rect(screen, WHITE, (583, 5, 5, 25))
                draw_text(screen, f"Очки: {score}", (10, 10), WHITE)
    
                pygame.display.flip()
    
                clock.tick(speed_snake * 4)
            else:
                if snake_minus == 1:
                    snake.positions.pop(0)
                    snake.positions.pop(0)
                    snake_minus = 0
                if not game_flag:
                    food.update()                
    elif selected_level == 1:
        pg.mixer.music.play()
        # Уровень 2
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)  
            if game_flag == 1:
                snake.update()
                food.update()
                food.render(screen)                 
                if snake.get_head_position() == food.position:
                    sound1.play()
                    snake.size += 1
                    food.randomize_position()
                    score += 1
    
                # Проверка столкновения головы змейки с телом
                if snake.get_head_position() in snake.positions[1:]:
                    game_over(score)
                    return
    
                screen.blit(background_color, (0, 0))           
                snake.render(screen)
                food.render(screen)
    
                # Выводим количество очков на экран, рисуем кнопку паузы
                pygame.draw.rect(screen, WHITE, (570, 5, 5, 25))
                pygame.draw.rect(screen, WHITE, (583, 5, 5, 25))
                draw_text(screen, f"Очки: {score}", (10, 10), WHITE)
    
                pygame.display.flip()
    
                clock.tick(speed_snake * 4)
            else:
                if snake_minus == 1:
                    snake.positions.pop(0)
                    snake.positions.pop(0)
                    snake_minus = 0
                if not game_flag:
                    food.update()                 

# Функции для обработки событий
def handle_events(snake):
    global pause_flag
    global game_flag 
    global snake_minus
    if not pg.mixer.music.get_busy() and pause_flag == 0: # Проверка что музыка не завершилась
        pg.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 550 <= pygame.mouse.get_pos()[0] <= 600 and 0 <= pygame.mouse.get_pos()[1] <= 50 and game_flag == 1:
                sound3.play()
                pg.mixer.music.pause()
                game_flag = 0  
                snake_minus = 1
                pause_flag = 1
            elif 550 <= pygame.mouse.get_pos()[0] <= 600 and 0 <= pygame.mouse.get_pos()[1] <= 50 and game_flag == 0:
                sound3.play()
                game_flag = 1  
                pause_flag = 0
                pg.mixer.music.unpause()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_flag == 1:
                sound3.play()
                pg.mixer.music.pause()
                game_flag = 0  
                snake_minus = 1
                pause_flag = 1
            elif event.key == pygame.K_SPACE and game_flag == 0:
                sound3.play()
                game_flag = 1 
                pg.mixer.music.unpause()
                pause_flag = 0
            elif game_flag == 1:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT     


# Функция для вывода сообщения об окончании игры и возврата в главное меню
def game_over(score):
    pg.mixer.music.stop()
    sound2.play()
    waiting = True
    while waiting:
        screen.blit(fon, (0, 0)) 
        draw_text(screen, "Игра окончена!", (50, 50), RED)
        draw_text(screen, f"Очки: {score}", (50, 100), WHITE)
        draw_text(screen, "Нажмите Enter, чтобы вернуться в главное меню", (50, 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sound3.play()
                    waiting = False

        pygame.time.delay(100)  # Задержка

    pygame.event.clear()  # Очищаем все события после выхода из цикла
    main()

if __name__ == "__main__":
    draw_animated_splash_screen()
    main()
