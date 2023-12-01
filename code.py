import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Размеры экрана
WIDTH, HEIGHT = 600, 400

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Класс для змейки
class Snake:
    def __init__(self):
        self.size = 4  # Изначальная длина змейки
        self.positions = [
            ((WIDTH // 2), (HEIGHT // 2) + i * GRIDSIZE) for i in range(self.size)
        ]
        self.direction = UP  # Изначальное направление вверх
        self.color = RED

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
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRIDSIZE, GRIDSIZE))

# Класс для еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = WHITE
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE)-1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE)-1) * GRIDSIZE)

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

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()

    selected_level = choose_level()

    if selected_level == 0:
        # Уровень 1
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)
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
                or snake.get_head_position()[0] == WIDTH - 20 and  snake.positions[1][0] == 0
                or snake.get_head_position()[1] == 0 and snake.positions[1][1] == HEIGHT - 20
                or snake.get_head_position()[1] == HEIGHT - 20 and snake.positions[1][1] == 0
            ):
                game_over(score)
                return

            screen.fill(BLACK)
            snake.render(screen)
            food.render(screen)

            # Выводим количество очков на экран
            draw_text(screen, f"Очки: {score}", (10, 10), WHITE)

            pygame.display.flip()

            clock.tick(5)

    elif selected_level == 1:
        # Уровень 2
        snake = Snake()
        food = Food()
        score = 0
        while True:
            handle_events(snake)

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

            # Выводим количество очков на экран
            draw_text(screen, f"Очки: {score}", (10, 10), WHITE)

            pygame.display.flip()

            clock.tick(5)

# Функции для обработки событий
def handle_events(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = UP
            elif event.key == pygame.K_DOWN:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT:
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


GRIDSIZE = 20
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

if __name__ == "__main__":
    main()
