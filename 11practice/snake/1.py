import pygame
import random
from color_palette import *

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 7
clock = pygame.time.Clock()

score = 0
level = 1


# draw grid lines
def draw_grid():
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colorGRAY,
                             (i * CELL, j * CELL, CELL, CELL), 1)


# simple point class for coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [Point(10, 10), Point(10, 11), Point(10, 12)]
        self.dx = 1
        self.dy = 0

    # move snake forward
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    # draw snake (head + body)
    def draw(self):
        pygame.draw.rect(screen, colorRED,
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # check collision with walls
    def check_wall(self):
        head = self.body[0]
        return (
            head.x < 0 or head.x >= WIDTH // CELL or
            head.y < 0 or head.y >= HEIGHT // CELL
        )

    # check collision with itself
    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    # handle eating food
    def eat(self, foods):
        global score, level, FPS

        head = self.body[0]

        for food in foods[:]:
            if head.x == food.pos.x and head.y == food.pos.y:
                score += food.weight  # add points based on weight

                self.body.append(Point(head.x, head.y))  # grow snake

                foods.remove(food)
                foods.append(Food(self.body))  # spawn new food

                # level up system
                if score % 5 == 0:
                    level += 1
                    FPS += 1


class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)

        # random weight (difficulty mechanic)
        self.weight = random.choice([1, 2, 5])

        # lifetime depends on weight
        if self.weight == 1:
            self.lifetime = 5000
        elif self.weight == 2:
            self.lifetime = 7000
        else:
            self.lifetime = 10000

        self.spawn(snake_body)

    # spawn food in a safe random position
    def spawn(self, snake_body):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            if all(segment.x != x or segment.y != y for segment in snake_body):
                self.pos = Point(x, y)
                break

        self.timer = pygame.time.get_ticks()

    # remove food after some time
    def update(self, snake_body):
        current_time = pygame.time.get_ticks()

        if current_time - self.timer > self.lifetime:
            self.__init__(snake_body)

    # draw food with different colors
    def draw(self):
        if self.weight == 1:
            color = colorGREEN
        elif self.weight == 2:
            color = colorYELLOW
        else:
            color = colorRED

        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


snake = Snake()

# multiple food objects
foods = [Food(snake.body) for _ in range(2)]

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # control snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP:
                snake.dx, snake.dy = 0, -1

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()

    # check game over conditions
    if snake.check_wall() or snake.check_self_collision():
        print("Game Over")
        running = False

    snake.eat(foods)

    # update and draw food
    for food in foods:
        food.update(snake.body)
        food.draw()

    snake.draw()

    # display score and level
    font = pygame.font.SysFont("Verdana", 25)
    text = font.render(f"Score: {score}  Level: {level}", True, colorWHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
