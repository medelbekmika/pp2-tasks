import pygame
import random
import time

pygame.init()
# SCREEN
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
# IMAGES (SCALED)
image_background = pygame.image.load('practice11/pictures/AnimatedStreet.png')

image_player = pygame.image.load('practice11/pictures/Player.png')
image_player = pygame.transform.scale(image_player, (80, 130))

image_enemy = pygame.image.load('practice11/pictures/Enemy.png')
image_enemy = pygame.transform.scale(image_enemy, (80, 130))

image_coin = pygame.image.load('practice11/pictures/coin.png')
image_coin = pygame.transform.scale(image_coin, (30, 30))
# AUDIO
pygame.mixer.music.load('practice11/songs/background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('practice11/songs/crash.wav')
sound_coin = pygame.mixer.Sound('practice11/songs/coin.wav')
# FONT
font = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 25)

game_over_text = font.render("Game Over", True, "black")
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
# SETTINGS
FPS = 60
clock = pygame.time.Clock()

COINS_TO_SPEEDUP = 5
# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 6

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
# ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 7
        self.reset()

    def reset(self):
        max_x = WIDTH - self.rect.width
        if max_x < 0:
            max_x = 0
        while True:
            self.rect.left = random.randint(0, max_x)
            self.rect.top = random.randint(-200, -100)
            if 'player' in globals():
                if abs(self.rect.centerx - player.rect.centerx) > 100:
                    break
            else:
                break

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.reset()
# COIN
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()

        self.value = random.choice([1, 2, 5])
        self.speed = random.randint(3, 6)

        self.reset()

    def reset(self):
        max_x = WIDTH - self.rect.width
        if max_x < 0:
            max_x = 0

        self.rect.left = random.randint(0, max_x)
        self.rect.top = random.randint(-500, -50)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.reset()
# OBJECTS
player = Player()
enemy = Enemy()

coins = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

enemy_group.add(enemy)
all_sprites.add(player, enemy)
# create coins
for _ in range(5):
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)
# GAME VARIABLES
running = True
score = 0
coin_counter = 0
# GAME LOOP
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # move player
    player.move()
    # draw background
    screen.blit(image_background, (0, 0))
    # move everything
    for obj in all_sprites:
        obj.move()
        screen.blit(obj.image, obj.rect)
    # COIN COLLISION
    collected = pygame.sprite.spritecollide(player, coins, True)
    for coin in collected:
        sound_coin.play()
        score += coin.value
        coin_counter += 1

        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)
        if coin_counter % COINS_TO_SPEEDUP == 0:
            enemy.speed += 1
    # ENEMY COLLISION (SAFE)
    if pygame.sprite.spritecollide(player, enemy_group, False):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        running = False
    # SCORE
    text = font_small.render(f"Score: {score}", True, "black")
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
