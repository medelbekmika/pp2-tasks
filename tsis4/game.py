import json
import os
import random
import pygame

from db import save_result, get_top_scores, get_personal_best

CELL = 20
COLS = 30
ROWS = 20
GRID_WIDTH = COLS * CELL
GRID_HEIGHT = ROWS * CELL
PANEL_HEIGHT = 100
WIDTH = GRID_WIDTH
HEIGHT = GRID_HEIGHT + PANEL_HEIGHT

BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
RED = (220, 60, 60)
DARK_RED = (120, 20, 20)
ORANGE = (255, 165, 0)
YELLOW = (240, 220, 70)
CYAN = (0, 200, 220)
PURPLE = (160, 80, 220)
GRAY = (70, 70, 70)
LIGHT_BG = (230, 230, 230)
BTN = (220, 220, 220)
BTN_HOVER = (190, 190, 190)

BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")


def load_settings():
    default = {
        "snake_color": [50, 180, 90],
        "grid": True,
        "sound": True
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        default.update(data)
        return default
    except Exception:
        save_settings(default)
        return default


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font, mouse_pos):
        color = BTN_HOVER if self.rect.collidepoint(mouse_pos) else BTN
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class SnakeGame:
    def __init__(self):
        pygame.init()

        try:
            pygame.mixer.init()
            self.audio_available = True
        except Exception:
            self.audio_available = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake TSIS4")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 34)

        self.settings = load_settings()

        self.food_sound = None
        self.gameover_sound = None
        self.move_sound = None

        if self.audio_available:
            try:
                self.food_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "food-court-1.wav"))
                self.gameover_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "gameover.wav"))
                self.move_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, ""))

                self.food_sound.set_volume(0.6)
                self.gameover_sound.set_volume(0.7)
                self.move_sound.set_volume(0.25)
            except Exception:
                self.food_sound = None
                self.gameover_sound = None
                self.move_sound = None

        if self.audio_available and self.settings["sound"]:
            self.start_background_music()

        self.state = "menu"
        self.username = ""
        self.cached_personal_best = 0

        self.color_options = [
            [50, 180, 90],
            [220, 60, 60],
            [70, 120, 220],
            [240, 220, 70],
        ]

        self.menu_buttons = [
            Button(210, 150, 180, 42, "Play"),
            Button(210, 205, 180, 42, "Leaderboard"),
            Button(210, 260, 180, 42, "Settings"),
            Button(210, 315, 180, 42, "Quit"),
        ]

        self.back_button = Button(210, 430, 180, 42, "Back")
        self.retry_button = Button(210, 360, 180, 42, "Retry")
        self.menu_button = Button(210, 415, 180, 42, "Main Menu")
        self.save_back_button = Button(180, 430, 240, 42, "Save & Back")

        self.grid_button = Button(220, 150, 160, 40, "")
        self.sound_button = Button(220, 210, 160, 40, "")
        self.color_button = Button(390, 270, 110, 40, "Change")

        self.reset_game()

    def reset_game(self):
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0
        self.level = 1
        self.base_speed = 8
        self.speed = 8

        self.game_over = False
        self.result_saved = False

        self.obstacles = set()

        self.food = self.create_food()
        self.poison_food = self.create_poison_food()

        self.food_lifetime = 5000
        self.food_spawn_time = pygame.time.get_ticks()

        self.powerup = None
        self.powerup_duration_end = 0
        self.active_power = None
        self.shield_ready = False

        self.cached_personal_best = get_personal_best(self.username) if self.username else 0

    def play_food_sound(self):
        if self.settings["sound"] and self.audio_available and self.food_sound:
            self.food_sound.play()

    def play_move_sound(self):
        if self.settings["sound"] and self.audio_available and self.move_sound:
            self.move_sound.play()

    def play_gameover_sound(self):
        if self.settings["sound"] and self.audio_available and self.gameover_sound:
            self.gameover_sound.play()

    def stop_background_music(self):
        if self.audio_available:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def start_background_music(self):
        if self.audio_available and self.settings["sound"]:
            try:
                pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "music_background.mp3"))
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def create_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake and pos not in self.obstacles:
                return {
                    "pos": pos,
                    "weight": random.choice([1, 2, 3])
                }

    def create_poison_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake and pos not in self.obstacles and pos != self.food["pos"]:
                return pos

    def create_powerup(self):
        kinds = ["speed", "slow", "shield"]
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.food["pos"]
                and pos != self.poison_food
            ):
                return {
                    "pos": pos,
                    "type": random.choice(kinds),
                    "expires_at": pygame.time.get_ticks() + 8000
                }

    def generate_obstacles(self):
        self.obstacles.clear()

        if self.level < 3:
            return

        obstacle_count = min(3 + self.level, 10)
        head = self.snake[0]
        attempts = 0
        max_attempts = 200

        while len(self.obstacles) < obstacle_count and attempts < max_attempts:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            attempts += 1

            if pos in self.snake:
                continue
            if pos == self.food["pos"] or pos == self.poison_food:
                continue
            if abs(pos[0] - head[0]) <= 2 and abs(pos[1] - head[1]) <= 2:
                continue

            self.obstacles.add(pos)

        self.food = self.create_food()
        self.poison_food = self.create_poison_food()

    def draw_cell(self, pos, color):
        x, y = pos
        pygame.draw.rect(self.screen, color, (x * CELL, y * CELL, CELL, CELL))

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, GRID_WIDTH, CELL):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, CELL):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (GRID_WIDTH, y))

    def handle_game_logic(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        collision = False

        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            collision = True
        elif new_head in self.snake:
            collision = True
        elif new_head in self.obstacles:
            collision = True

        if collision:
            if self.shield_ready:
                self.shield_ready = False
                self.active_power = None
                return
            self.game_over = True
            self.stop_background_music()
            self.play_gameover_sound()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food["pos"]:
            self.play_food_sound()
            self.score += self.food["weight"]
            self.level = self.score // 4 + 1
            self.base_speed = 8 + (self.level - 1) * 2

            self.food = self.create_food()
            self.poison_food = self.create_poison_food()
            self.food_spawn_time = pygame.time.get_ticks()

            if self.level >= 3:
                self.generate_obstacles()

        elif new_head == self.poison_food:
            self.play_food_sound()

            if len(self.snake) <= 3:
                self.game_over = True
                self.stop_background_music()
                self.play_gameover_sound()
                return

            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            self.poison_food = self.create_poison_food()

        else:
            self.snake.pop()

        if self.powerup and new_head == self.powerup["pos"]:
            if self.powerup["type"] == "speed":
                self.active_power = "speed"
                self.powerup_duration_end = pygame.time.get_ticks() + 5000
            elif self.powerup["type"] == "slow":
                self.active_power = "slow"
                self.powerup_duration_end = pygame.time.get_ticks() + 5000
            else:
                self.active_power = "shield"
                self.shield_ready = True

            self.powerup = None

        if pygame.time.get_ticks() - self.food_spawn_time >= self.food_lifetime:
            self.food = self.create_food()
            self.poison_food = self.create_poison_food()
            self.food_spawn_time = pygame.time.get_ticks()

        if self.powerup is None and random.randint(1, 200) == 1:
            self.powerup = self.create_powerup()

        if self.powerup and pygame.time.get_ticks() > self.powerup["expires_at"]:
            self.powerup = None

        if self.active_power in ["speed", "slow"] and pygame.time.get_ticks() > self.powerup_duration_end:
            self.active_power = None

        self.speed = self.base_speed
        if self.active_power == "speed":
            self.speed = min(20, int(self.base_speed * 1.5))
        elif self.active_power == "slow":
            self.speed = max(4, int(self.base_speed * 0.6))

    def draw_game(self):
        self.screen.fill(BLACK)

        snake_color = tuple(self.settings["snake_color"])
        body_color = (
            max(0, snake_color[0] - 20),
            max(0, snake_color[1] - 20),
            max(0, snake_color[2] - 20),
        )

        for i, segment in enumerate(self.snake):
            self.draw_cell(segment, snake_color if i == 0 else body_color)

        food_colors = {
            1: RED,
            2: ORANGE,
            3: YELLOW,
        }
        self.draw_cell(self.food["pos"], food_colors[self.food["weight"]])
        self.draw_cell(self.poison_food, DARK_RED)

        if self.powerup:
            if self.powerup["type"] == "speed":
                self.draw_cell(self.powerup["pos"], CYAN)
            elif self.powerup["type"] == "slow":
                self.draw_cell(self.powerup["pos"], PURPLE)
            else:
                self.draw_cell(self.powerup["pos"], WHITE)

        for block in self.obstacles:
            self.draw_cell(block, GRAY)

        self.draw_grid()

        pygame.draw.rect(self.screen, (30, 30, 30), (0, GRID_HEIGHT, WIDTH, PANEL_HEIGHT))

        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, GRID_HEIGHT + 10))
        self.screen.blit(self.font.render(f"Level: {self.level}", True, WHITE), (10, GRID_HEIGHT + 40))
        self.screen.blit(self.small_font.render(f"Best: {self.cached_personal_best}", True, WHITE), (180, GRID_HEIGHT + 15))

        if self.active_power == "speed":
            remaining = max(0, (self.powerup_duration_end - pygame.time.get_ticks()) // 1000)
            self.screen.blit(self.small_font.render(f"Speed: {remaining}s", True, CYAN), (420, GRID_HEIGHT + 15))
        elif self.active_power == "slow":
            remaining = max(0, (self.powerup_duration_end - pygame.time.get_ticks()) // 1000)
            self.screen.blit(self.small_font.render(f"Slow: {remaining}s", True, PURPLE), (420, GRID_HEIGHT + 15))
        elif self.shield_ready:
            self.screen.blit(self.small_font.render("Shield: ready", True, WHITE), (420, GRID_HEIGHT + 15))
        else:
            self.screen.blit(self.small_font.render("Power: none", True, WHITE), (420, GRID_HEIGHT + 15))

    def save_result_if_needed(self):
        if self.game_over and not self.result_saved and self.username.strip():
            save_result(self.username, self.score, self.level)
            self.result_saved = True

    def draw_menu(self):
        self.screen.fill(LIGHT_BG)
        title = self.big_font.render("SNAKE MENU", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.draw(self.screen, self.font, mouse_pos)

    def draw_name_input(self):
        self.screen.fill(LIGHT_BG)
        title = self.big_font.render("ENTER USERNAME", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        box = pygame.Rect(150, 210, 300, 50)
        pygame.draw.rect(self.screen, WHITE, box)
        pygame.draw.rect(self.screen, BLACK, box, 2)

        text_surface = self.font.render(self.username, True, BLACK)
        self.screen.blit(text_surface, (box.x + 10, box.y + 10))

        self.screen.blit(self.small_font.render("Press Enter to start", True, BLACK), (220, 290))
        self.screen.blit(self.small_font.render("Press Esc to go back", True, BLACK), (215, 320))

    def draw_leaderboard(self):
        self.screen.fill(LIGHT_BG)
        title = self.big_font.render("LEADERBOARD", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        rows = get_top_scores(10)
        y = 95

        headers = ["#", "Name", "Score", "Level", "Date"]
        xs = [25, 70, 260, 360, 445]

        for i, h in enumerate(headers):
            self.screen.blit(self.small_font.render(h, True, BLACK), (xs[i], 70))

        for idx, row in enumerate(rows, start=1):
            username, score, level_reached, played_at = row
            values = [str(idx), username, str(score), str(level_reached), played_at.strftime("%Y-%m-%d")]
            for i, value in enumerate(values):
                self.screen.blit(self.small_font.render(value, True, BLACK), (xs[i], y))
            y += 28

        self.back_button.draw(self.screen, self.font, pygame.mouse.get_pos())

    def draw_settings(self):
        self.screen.fill(LIGHT_BG)
        title = self.big_font.render("SETTINGS", True, BLACK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        self.grid_button.text = f"Grid: {'ON' if self.settings['grid'] else 'OFF'}"
        self.sound_button.text = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"

        mouse_pos = pygame.mouse.get_pos()

        self.grid_button.draw(self.screen, self.font, mouse_pos)
        self.sound_button.draw(self.screen, self.font, mouse_pos)

        self.screen.blit(self.font.render("Snake color:", True, BLACK), (135, 278))
        color_preview = pygame.Rect(300, 270, 80, 40)
        pygame.draw.rect(self.screen, tuple(self.settings["snake_color"]), color_preview)
        pygame.draw.rect(self.screen, BLACK, color_preview, 2)

        self.color_button.draw(self.screen, self.font, mouse_pos)
        self.save_back_button.draw(self.screen, self.font, mouse_pos)

    def draw_game_over(self):
        self.screen.fill(LIGHT_BG)

        title = self.big_font.render("GAME OVER", True, RED)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        best = max(self.cached_personal_best, self.score)

        self.screen.blit(self.font.render(f"Final score: {self.score}", True, BLACK), (210, 180))
        self.screen.blit(self.font.render(f"Level reached: {self.level}", True, BLACK), (190, 220))
        self.screen.blit(self.font.render(f"Personal best: {best}", True, BLACK), (195, 260))

        mouse_pos = pygame.mouse.get_pos()
        self.retry_button.draw(self.screen, self.font, mouse_pos)
        self.menu_button.draw(self.screen, self.font, mouse_pos)

    def cycle_snake_color(self):
        current = self.settings["snake_color"]
        idx = self.color_options.index(current) if current in self.color_options else 0
        self.settings["snake_color"] = self.color_options[(idx + 1) % len(self.color_options)]

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == "menu":
                    if self.menu_buttons[0].clicked(event):
                        self.state = "name_input"
                        self.username = ""
                    elif self.menu_buttons[1].clicked(event):
                        self.state = "leaderboard"
                    elif self.menu_buttons[2].clicked(event):
                        self.state = "settings"
                    elif self.menu_buttons[3].clicked(event):
                        running = False

                elif self.state == "name_input":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.username.strip():
                            self.cached_personal_best = get_personal_best(self.username)
                            self.reset_game()
                            self.start_background_music()
                            self.state = "game"
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"
                        elif event.unicode.isprintable():
                            self.username += event.unicode

                elif self.state == "leaderboard":
                    if self.back_button.clicked(event):
                        self.state = "menu"

                elif self.state == "settings":
                    if self.grid_button.clicked(event):
                        self.settings["grid"] = not self.settings["grid"]
                    elif self.sound_button.clicked(event):
                        self.settings["sound"] = not self.settings["sound"]
                        if self.settings["sound"]:
                            self.start_background_music()
                        else:
                            self.stop_background_music()
                    elif self.color_button.clicked(event):
                        self.cycle_snake_color()
                    elif self.save_back_button.clicked(event):
                        save_settings(self.settings)
                        self.state = "menu"

                elif self.state == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.next_direction = (0, -1)
                            self.play_move_sound()
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.next_direction = (0, 1)
                            self.play_move_sound()
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.next_direction = (-1, 0)
                            self.play_move_sound()
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.next_direction = (1, 0)
                            self.play_move_sound()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = "menu"

                elif self.state == "game_over":
                    if self.retry_button.clicked(event):
                        self.reset_game()
                        self.start_background_music()
                        self.state = "game"
                    elif self.menu_button.clicked(event):
                        self.state = "menu"

            if self.state == "game":
                self.handle_game_logic()
                if self.game_over:
                    self.save_result_if_needed()
                    self.state = "game_over"
                self.draw_game()

            elif self.state == "menu":
                self.draw_menu()

            elif self.state == "name_input":
                self.draw_name_input()

            elif self.state == "leaderboard":
                self.draw_leaderboard()

            elif self.state == "settings":
                self.draw_settings()

            elif self.state == "game_over":
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(self.speed if self.state == "game" else 60)

        self.stop_background_music()
        pygame.quit()
