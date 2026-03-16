

Requirements:
    pip install pygame


import pygame
import random
import sys

# ── Constants ──────────────────────────────────────────────
WIDTH, HEIGHT = 600, 600
CELL = 20
ROWS = HEIGHT // CELL
COLS = WIDTH // CELL
FPS = 10

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 200, 80)
DGREEN = (0, 140, 50)
RED    = (220, 50, 50)
GRAY   = (30, 30, 30)
YELLOW = (255, 220, 0)

# Directions
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(COLS // 2, ROWS // 2)]
        self.direction = RIGHT
        self.grow = False

    def change_direction(self, new_dir):
        # Prevent reversing
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def check_collision(self) -> bool:
        head = self.body[0]
        # Wall collision
        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

    def eat(self, food_pos) -> bool:
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else DGREEN
            rect = pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)
            pygame.draw.rect(surface, color, rect, border_radius=4)


class Food:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(surface, RED, rect, border_radius=5)


def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))


def draw_score(surface, font, score, high_score):
    score_text = font.render(f"Score: {score}   Best: {high_score}", True, WHITE)
    surface.blit(score_text, (10, 5))


def game_over_screen(surface, font, big_font, score, high_score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, RED)
    score_txt = font.render(f"Score: {score}   Best: {high_score}", True, WHITE)
    restart_txt = font.render("Press R to Restart   Q to Quit", True, YELLOW)

    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
    surface.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT // 2))
    surface.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 60))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 52, bold=True)

    high_score = 0

    while True:
        snake = Snake()
        food = Food(snake.body)
        score = 0
        running = True

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)

            snake.move()

            if snake.check_collision():
                high_score = max(high_score, score)
                game_over_screen(screen, font, big_font, score, high_score)
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                waiting = False
                                running = False
                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()
                break

            if snake.eat(food.position):
                score += 10
                food = Food(snake.body)

            # Draw
            screen.fill(BLACK)
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_score(screen, font, score, high_score)
            pygame.display.flip()


if __name__ == "__main__":
    main()
