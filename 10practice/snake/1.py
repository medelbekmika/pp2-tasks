import pygame
from color_palette import *
import random

pygame.init()

# ---------------- SCREEN SETTINGS ----------------
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

CELL = 30  

# ---------------- GAME SPEED ----------------
FPS = 5
clock = pygame.time.Clock()

# ---------------- SCORE + LEVEL ----------------
score = 0
level = 1

# ---------------- DRAW GRID ----------------
def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


# ---------------- POINT CLASS ----------------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# ---------------- SNAKE CLASS ----------------
class Snake:
    def __init__(self):
        self.body = [
            Point(10, 11),
            Point(10, 12),
            Point(10, 13)
        ]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED,
                         (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # ---------------- WALL COLLISION (GAME OVER) ----------------
    def check_wall_collision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL:
            return True
        if head.y < 0 or head.y >= HEIGHT // CELL:
            return True

        return False

    # ---------------- FOOD COLLISION ----------------
    def check_collision(self, food):
        global score, FPS, level

        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            score += 1 
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos(self.body)

            # ---------------- LEVEL SYSTEM ----------------
            if score % 3 == 0:
                level += 1
                FPS += 1 


# ---------------- FOOD CLASS ----------------
class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    # ---------------- SAFE RANDOM FOOD SPAWN ----------------
    def generate_random_pos(self, snake_body):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            # check food does NOT spawn on snake
            if all(segment.x != x or segment.y != y for segment in snake_body):
                self.pos.x = x
                self.pos.y = y
                break


# ---------------- GAME OBJECTS ----------------
snake = Snake()
food = Food()

running = True

# ---------------- MAIN LOOP ----------------
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------------- CONTROL SNAKE ----------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    # ---------------- DRAW BACKGROUND ----------------
    screen.fill(colorBLUE)
    draw_grid()

    # ---------------- GAME LOGIC ----------------
    snake.move()

    # wall collision check
    if snake.check_wall_collision():
        print("Game Over!")
        running = False

    # food collision check
    snake.check_collision(food)

    # ---------------- DRAW GAME OBJECTS ----------------
    snake.draw()
    food.draw()

    # ---------------- HUD (SCORE + LEVEL) ----------------
    font = pygame.font.SysFont("Verdana", 25)
    text = font.render(f"Score: {score}  Level: {level}", True, colorWHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
