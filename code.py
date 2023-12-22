import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
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


# Класс для змейки
class Snake:
    def __init__(self):
        self.size = 4  # Изначальная длина змейки
        self.positions = [
            ((WIDTH // 2), (HEIGHT // 2) + i * GRIDSIZE) for i in range(self.size)
        ]
        self.direction = UP  # Изначальное направление вверх
        self.color = WHITE

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
        self.color = GREEN
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


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


# Функция для выбора уровня
def choose_level():
    levels = ["Уровень 1", "Уровень 2"]
    selected_level = 0

    while True:
        screen.fill(BLACK)
        draw_text(screen, "Выберите уровень:", (50, 50))

        for i, level in enumerate(levels):
            color = WHITE if i == selected_level else RED
            draw_text(screen, level, (50, 100 + i * 50), color)

        draw_text(screen, ">", (30, 100 + selected_level * 50), WHITE)

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
                    return selected_level


def draw_animated_splash_screen():
    screen.fill(BLACK)

    # Начальные координаты для заголовка "SNAKE"
    title_x = -300
    title_y = HEIGHT // 4

    # Анимация выезда заголовка
    while title_x <= (WIDTH - 300):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        title_font_1 = pygame.font.SysFont('comicsansms', 72)
        title_font_2 = pygame.font.SysFont('consolas', 22)        
        title_text_1 = title_font_1.render("SNAKE", True, WHITE)
        title_shadow_1 = title_font_1.render("SNAKE", True, (115, 115, 115))
        screen.blit(title_shadow_1, (title_x + 3, title_y + 3))
        screen.blit(title_text_1, (title_x, title_y))
        title_text_2 = title_font_2.render("Made by Maxim Nenashev & Darina Zelenkova", True, WHITE)
        title_shadow_2 = title_font_2.render("Made by Maxim Nenashev & Darina Zelenkova", True, (115, 115, 115))
        screen.blit(title_shadow_2, (title_x - 240, title_y + 102))
        screen.blit(title_text_2, (title_x - 241, title_y  + 101))        

        pygame.display.flip()
        pygame.time.delay(10)  # Задержка в 10 миллисекунд для создания анимации
        title_x += 2  # Изменение координаты X

    pygame.time.delay(2000)


# Основной игровой цикл
def main():
    global game_flag
    global snake_minus    
    game_flag = 1
    clock = pygame.time.Clock()
    selected_level = choose_level()

    if selected_level == 0:
        # Уровень 1
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)            
            if game_flag == 1:
                snake.update()
    
                if snake.get_head_position() == food.position:
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
    
                screen.fill(BLACK)
                snake.render(screen)
                food.render(screen)
    
                # Выводим количество очков на экран, рисуем кнопку паузы и границы
                pygame.draw.rect(screen, RED, (0, 0, 600, 400), 2)
                pygame.draw.rect(screen, WHITE, (570, 5, 5, 25))
                pygame.draw.rect(screen, WHITE, (583, 5, 5, 25))
                draw_text(screen, f"Очки: {score}", (10, 10), WHITE)
    
                pygame.display.flip()
    
                clock.tick(5)
            else:
                if snake_minus == 1:
                    snake.positions.pop(0)
                    snake.positions.pop(0)
                    snake_minus = 0
    elif selected_level == 1:
        # Уровень 2
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)  
            if game_flag == 1:
                snake.update()
                if snake.get_head_position() == food.position:
                    snake.size += 1
                    food.randomize_position()
                    score += 1
    
                # Проверка столкновения головы змейки с телом
                if snake.get_head_position() in snake.positions[1:]:
                    game_over(score)
                    return
    
                screen.fill(BLACK)
                snake.render(screen)
                food.render(screen)
    
                # Выводим количество очков на экран, рисуем кнопку паузы
                pygame.draw.rect(screen, WHITE, (570, 5, 5, 25))
                pygame.draw.rect(screen, WHITE, (583, 5, 5, 25))
                draw_text(screen, f"Очки: {score}", (10, 10), WHITE)
    
                pygame.display.flip()
    
                clock.tick(5)
            else:
                if snake_minus == 1:
                    snake.positions.pop(0)
                    snake.positions.pop(0)
                    snake_minus = 0

# Функции для обработки событий
def handle_events(snake):
    global game_flag 
    global snake_minus
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 550 <= pygame.mouse.get_pos()[0] <= 600 and 0 <= pygame.mouse.get_pos()[1] <= 50 and game_flag == 1:
                game_flag = 0  
                snake_minus = 1
            elif 550 <= pygame.mouse.get_pos()[0] <= 600 and 0 <= pygame.mouse.get_pos()[1] <= 50 and game_flag == 0:
                game_flag = 1  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_flag == 1:
                game_flag = 0  
                snake_minus = 1
            elif event.key == pygame.K_SPACE and game_flag == 0:
                game_flag = 1      
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
    waiting = True
    while waiting:
        screen.fill(BLACK)
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
                    waiting = False

        pygame.time.delay(100)  # Задержка

    pygame.event.clear()  # Очищаем все события после выхода из цикла
    main()

if __name__ == "__main__":
    draw_animated_splash_screen()
    main()
