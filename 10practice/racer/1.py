import pygame
import random
import time

pygame.init()

# ---------------- SCREEN ----------------
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ---------------- ASSETS ----------------
image_background = pygame.image.load('10prac/images/AnimatedStreet.png')
image_player = pygame.image.load('10prac/images/Player.png')
image_enemy = pygame.image.load('10prac/images/Enemy.png')
image_coin = pygame.image.load('10prac/images/coin.png')  
image_coin = pygame.transform.scale(image_coin , (30 , 30))

sound_crash = pygame.mixer.Sound('10prac/sound/crash.wav')

font = pygame.font.SysFont("Verdana", 30)

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# ---------------- SCORE ----------------
score = 0


# ---------------- PLAYER ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        # keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 8
        self.spawn()

    def spawn(self):
        # SAFE random range (prevents negative randint error)
        max_x = max(0, WIDTH - self.rect.width)
        self.rect.left = random.randint(0, max_x)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.spawn()


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        # SAFE random range (FIX for your error)
        max_x = max(0, WIDTH - self.rect.width)
        self.rect.left = random.randint(0, max_x)

        # spawn above screen
        self.rect.top = random.randint(-600, -40)

    def move(self):
        self.rect.move_ip(0, 5)

        # respawn if off screen
        if self.rect.top > HEIGHT:
            self.spawn()


# ---------------- SETUP ----------------
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemies.add(enemy)
coins.add(coin)

clock = pygame.time.Clock()
FPS = 60

running = True


# ---------------- GAME LOOP ----------------
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # move player
    player.move()

    # draw background
    screen.blit(image_background, (0, 0))

    # draw score
    score_text = font.render(f"Score: {score}", True, "black")
    screen.blit(score_text, (WIDTH - 140, 10))

    # update sprites
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    # ---------------- COIN COLLISION ----------------
    if pygame.sprite.collide_rect(player, coin):
        score += 1
        coin.spawn()

    # ---------------- ENEMY COLLISION ----------------
    if pygame.sprite.spritecollideany(player, enemies):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
