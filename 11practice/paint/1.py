import pygame
import math

pygame.init()

# screen setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# colors
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)

# drawing settings
clock = pygame.time.Clock()
THICKNESS = 5

# tool selection
tool = "pen"  # pen, rect, circle, square, rtriangle, etriangle, rhombus, eraser
color = colorRED

# mouse state
LMBpressed = False
start_pos = (0, 0)

# canvas
screen.fill(colorBLACK)


# draw circle using drag distance
def draw_circle(surface, start, end, color, thickness):
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, thickness)


# draw square (equal width & height)
def draw_square(surface, start, end, color, thickness):
    size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    rect = pygame.Rect(start[0], start[1], size, size)
    pygame.draw.rect(surface, color, rect, thickness)


# draw right triangle
def draw_right_triangle(surface, start, end, color, thickness):
    points = [
        start,
        (start[0], end[1]),
        (end[0], end[1])
    ]
    pygame.draw.polygon(surface, color, points, thickness)


# draw equilateral triangle
def draw_equilateral_triangle(surface, start, end, color, thickness):
    side = abs(end[0] - start[0])
    height = int(side * math.sqrt(3) / 2)

    points = [
        (start[0], start[1]),
        (start[0] + side, start[1]),
        (start[0] + side // 2, start[1] - height)
    ]
    pygame.draw.polygon(surface, color, points, thickness)


# draw rhombus (diamond shape)
def draw_rhombus(surface, start, end, color, thickness):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2

    points = [
        (cx, cy - dy),
        (cx + dx, cy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]
    pygame.draw.polygon(surface, color, points, thickness)


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # tool selection
            if event.key == pygame.K_p:
                tool = "pen"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_s:
                tool = "square"
            if event.key == pygame.K_t:
                tool = "rtriangle"
            if event.key == pygame.K_y:
                tool = "etriangle"
            if event.key == pygame.K_u:
                tool = "rhombus"
            if event.key == pygame.K_e:
                tool = "eraser"

            # color selection
            if event.key == pygame.K_1:
                color = colorRED
            if event.key == pygame.K_2:
                color = colorBLUE
            if event.key == pygame.K_3:
                color = colorGREEN
            if event.key == pygame.K_4:
                color = colorWHITE

            # thickness control
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)

            # clear screen
            if event.key == pygame.K_x:
                screen.fill(colorBLACK)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            end_pos = event.pos

            # draw shapes on mouse release
            if tool == "rect":
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    ),
                    THICKNESS
                )

            if tool == "circle":
                draw_circle(screen, start_pos, end_pos, color, THICKNESS)

            if tool == "square":
                draw_square(screen, start_pos, end_pos, color, THICKNESS)

            if tool == "rtriangle":
                draw_right_triangle(screen, start_pos, end_pos, color, THICKNESS)

            if tool == "etriangle":
                draw_equilateral_triangle(screen, start_pos, end_pos, color, THICKNESS)

            if tool == "rhombus":
                draw_rhombus(screen, start_pos, end_pos, color, THICKNESS)

        if event.type == pygame.MOUSEMOTION and LMBpressed:

            pos = event.pos

            # free drawing
            if tool == "pen":
                pygame.draw.circle(screen, color, pos, THICKNESS)

            # eraser
            if tool == "eraser":
                pygame.draw.circle(screen, colorBLACK, pos, THICKNESS * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
