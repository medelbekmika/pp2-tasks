import pygame
import sys
from datetime import datetime
from tools import (
    draw_circle, draw_square, draw_right_triangle,
    draw_equilateral_triangle, draw_rhombus, flood_fill
)

pygame.init()

# screen settings
WIDTH = 800
HEIGHT = 650
TOOLBAR_HEIGHT = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2")

# colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
GREEN  = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (148, 0, 211)
CYAN   = (0, 255, 255)
PINK   = (255, 105, 180)
GRAY   = (200, 200, 200)

# toolbar background color
TOOLBAR_BG = (50, 50, 50)

# list of colors for the palette
palette_colors = [BLACK, WHITE, RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, CYAN, PINK]

# brush sizes: small, medium, large
BRUSH_SMALL  = 2
BRUSH_MEDIUM = 5
BRUSH_LARGE  = 10

# drawing settings
current_tool  = "pen"
current_color = RED
brush_size    = BRUSH_MEDIUM

# mouse state
mouse_pressed = False
start_x = 0
start_y = 0
prev_x  = 0
prev_y  = 0

# for live preview of shapes
preview_canvas = None

# text tool state
text_mode   = False
text_input  = ""
text_x      = 0
text_y      = 0

# fonts
font       = pygame.font.SysFont("Arial", 14)
font_small = pygame.font.SysFont("Arial", 12)
font_text  = pygame.font.SysFont("Arial", 22)

# canvas (separate surface so we can save it without toolbar)
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()
# draw the toolbar at the top
def draw_toolbar():
    # toolbar background
    pygame.draw.rect(screen, TOOLBAR_BG, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # tool buttons - simple rectangles with labels
    tools_list = ["pen", "line", "rect", "circle", "square", "rtri", "etri", "rhomb", "eraser", "fill", "text"]
    x = 5
    for t in tools_list:
        if t == current_tool or (t == "rtri" and current_tool == "rtriangle") or \
           (t == "etri" and current_tool == "etriangle") or \
           (t == "rhomb" and current_tool == "rhombus"):
            btn_color = (100, 180, 100)
        else:
            btn_color = (80, 80, 80)

        pygame.draw.rect(screen, btn_color, (x, 8, 54, 28))
        pygame.draw.rect(screen, WHITE, (x, 8, 54, 28), 1)
        label = font_small.render(t, True, WHITE)
        screen.blit(label, (x + 4, 16))
        x += 57

    # brush size buttons
    x += 5
    for size_label, size_val in [("S", BRUSH_SMALL), ("M", BRUSH_MEDIUM), ("L", BRUSH_LARGE)]:
        if brush_size == size_val:
            btn_color = (100, 150, 220)
        else:
            btn_color = (80, 80, 80)
        pygame.draw.rect(screen, btn_color, (x, 15, 22, 22))
        pygame.draw.rect(screen, WHITE, (x, 15, 22, 22), 1)
        lbl = font_small.render(size_label, True, WHITE)
        screen.blit(lbl, (x + 5, 18))
        x += 25

    # color palette swatches
    x += 5
    for c in palette_colors:
        pygame.draw.rect(screen, c, (x, 14, 20, 20))
        if c == current_color:
            pygame.draw.rect(screen, WHITE, (x - 1, 13, 22, 22), 2)
        else:
            pygame.draw.rect(screen, GRAY, (x, 14, 20, 20), 1)
        x += 23

    # show current color preview
    pygame.draw.rect(screen, current_color, (x + 5, 10, 30, 30))
    pygame.draw.rect(screen, WHITE, (x + 5, 10, 30, 30), 2)

    # hint text
    if text_mode:
        hint = font_small.render("Text mode: type then press Enter, Esc to cancel", True, YELLOW)
    else:
        hint = font_small.render("Ctrl+S = save  |  X = clear", True, GRAY)
    screen.blit(hint, (5, 46))

# check if a point is inside the toolbar area
def is_toolbar_click(x, y):
    return y < TOOLBAR_HEIGHT

# figure out what was clicked in the toolbar
def handle_toolbar_click(x, y):
    global current_tool, brush_size, current_color

    # check tool buttons
    tools_list = ["pen", "line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus", "eraser", "fill", "text"]
    bx = 5
    for t in tools_list:
        if bx <= x <= bx + 54 and 8 <= y <= 36:
            current_tool = t
            return
        bx += 57

    # check brush size buttons
    bx += 5
    for size_label, size_val in [("S", BRUSH_SMALL), ("M", BRUSH_MEDIUM), ("L", BRUSH_LARGE)]:
        if bx <= x <= bx + 22 and 15 <= y <= 37:
            brush_size = size_val
            return
        bx += 25

    # check color swatches
    bx += 5
    for c in palette_colors:
        if bx <= x <= bx + 20 and 14 <= y <= 34:
            current_color = c
            return
        bx += 23

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # keyboard input
        if event.type == pygame.KEYDOWN:

            # if text mode is active, handle typing
            if text_mode:
                if event.key == pygame.K_RETURN:
                    # commit text to canvas
                    text_surface = font_text.render(text_input, True, current_color)
                    canvas.blit(text_surface, (text_x, text_y))
                    text_mode  = False
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    text_mode  = False
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if event.unicode != "" and event.unicode.isprintable():
                        text_input += event.unicode
                continue  # skip other key handling while typing

            # Ctrl + S to save
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_s:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = "canvas_" + timestamp + ".png"
                    pygame.image.save(canvas, filename)
                    pygame.display.set_caption("Saved: " + filename)

            # clear canvas
            if event.key == pygame.K_x:
                canvas.fill(WHITE)

            # tool shortcuts
            if event.key == pygame.K_p:
                current_tool = "pen"
            if event.key == pygame.K_l:
                current_tool = "line"
            if event.key == pygame.K_r:
                current_tool = "rect"
            if event.key == pygame.K_c:
                current_tool = "circle"
            if event.key == pygame.K_s:
                current_tool = "square"
            if event.key == pygame.K_t:
                current_tool = "rtriangle"
            if event.key == pygame.K_y:
                current_tool = "etriangle"
            if event.key == pygame.K_u:
                current_tool = "rhombus"
            if event.key == pygame.K_e:
                current_tool = "eraser"
            if event.key == pygame.K_f:
                current_tool = "fill"
            if event.key == pygame.K_i:
                current_tool = "text"

            # brush size shortcuts
            if event.key == pygame.K_1:
                brush_size = BRUSH_SMALL
            if event.key == pygame.K_2:
                brush_size = BRUSH_MEDIUM
            if event.key == pygame.K_3:
                brush_size = BRUSH_LARGE

        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx = event.pos[0]
            my = event.pos[1]

            # check if clicked toolbar
            if is_toolbar_click(mx, my):
                handle_toolbar_click(mx, my)
            else:
                # clicking on canvas
                canvas_x = mx
                canvas_y = my - TOOLBAR_HEIGHT

                mouse_pressed = True
                start_x = canvas_x
                start_y = canvas_y
                prev_x  = canvas_x
                prev_y  = canvas_y

                # text tool: set position and enter text mode
                if current_tool == "text":
                    text_mode  = True
                    text_input = ""
                    text_x     = canvas_x
                    text_y     = canvas_y
                    mouse_pressed = False

                # fill tool: run flood fill immediately
                elif current_tool == "fill":
                    flood_fill(canvas, (canvas_x, canvas_y), current_color)
                    mouse_pressed = False

                # save canvas state for live preview
                elif current_tool in ("line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"):
                    preview_canvas = canvas.copy()

        # mouse button up - finalize shapes
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_pressed:
                mouse_pressed = False

                ex = event.pos[0]
                ey = event.pos[1] - TOOLBAR_HEIGHT

                if current_tool == "rect":
                    rect_x = min(start_x, ex)
                    rect_y = min(start_y, ey)
                    rect_w = abs(ex - start_x)
                    rect_h = abs(ey - start_y)
                    pygame.draw.rect(canvas, current_color, (rect_x, rect_y, rect_w, rect_h), brush_size)

                elif current_tool == "circle":
                    draw_circle(canvas, (start_x, start_y), (ex, ey), current_color, brush_size)

                elif current_tool == "square":
                    draw_square(canvas, (start_x, start_y), (ex, ey), current_color, brush_size)

                elif current_tool == "rtriangle":
                    draw_right_triangle(canvas, (start_x, start_y), (ex, ey), current_color, brush_size)

                elif current_tool == "etriangle":
                    draw_equilateral_triangle(canvas, (start_x, start_y), (ex, ey), current_color, brush_size)

                elif current_tool == "rhombus":
                    draw_rhombus(canvas, (start_x, start_y), (ex, ey), current_color, brush_size)

                elif current_tool == "line":
                    pygame.draw.line(canvas, current_color, (start_x, start_y), (ex, ey), brush_size)

                preview_canvas = None

        # mouse motion - drawing while held down
        if event.type == pygame.MOUSEMOTION:
            if mouse_pressed:
                mx = event.pos[0]
                my = event.pos[1]

                # dont draw on toolbar
                if my < TOOLBAR_HEIGHT:
                    continue

                canvas_x = mx
                canvas_y = my - TOOLBAR_HEIGHT

                # pencil: draw line between previous and current position
                if current_tool == "pen":
                    pygame.draw.line(canvas, current_color, (prev_x, prev_y), (canvas_x, canvas_y), brush_size)
                    prev_x = canvas_x
                    prev_y = canvas_y

                # eraser
                elif current_tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, (canvas_x, canvas_y), brush_size * 3)

                # live preview for shapes and line
                elif current_tool in ("line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus"):
                    if preview_canvas is None:
                        continue  # not ready yet, skip to avoid drawing permanently

                    canvas.blit(preview_canvas, (0, 0))

                    if current_tool == "line":
                        pygame.draw.line(canvas, current_color, (start_x, start_y), (canvas_x, canvas_y), brush_size)

                    elif current_tool == "rect":
                        rect_x = min(start_x, canvas_x)
                        rect_y = min(start_y, canvas_y)
                        rect_w = abs(canvas_x - start_x)
                        rect_h = abs(canvas_y - start_y)
                        pygame.draw.rect(canvas, current_color, (rect_x, rect_y, rect_w, rect_h), brush_size)

                    elif current_tool == "circle":
                        draw_circle(canvas, (start_x, start_y), (canvas_x, canvas_y), current_color, brush_size)

                    elif current_tool == "square":
                        draw_square(canvas, (start_x, start_y), (canvas_x, canvas_y), current_color, brush_size)

                    elif current_tool == "rtriangle":
                        draw_right_triangle(canvas, (start_x, start_y), (canvas_x, canvas_y), current_color, brush_size)

                    elif current_tool == "etriangle":
                        draw_equilateral_triangle(canvas, (start_x, start_y), (canvas_x, canvas_y), current_color, brush_size)

                    elif current_tool == "rhombus":
                        draw_rhombus(canvas, (start_x, start_y), (canvas_x, canvas_y), current_color, brush_size)

    # draw everything
    screen.fill(BLACK)

    # draw canvas below toolbar
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # if text mode, show what user is typing
    if text_mode:
        typing_surface = font_text.render(text_input + "|", True, current_color)
        screen.blit(typing_surface, (text_x, text_y + TOOLBAR_HEIGHT))

    # draw toolbar on top
    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
