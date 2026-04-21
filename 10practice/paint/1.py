import pygame

pygame.init()

# ---------------- SCREEN ----------------
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ---------------- COLORS ----------------
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)

# ---------------- DRAW SETTINGS ----------------
clock = pygame.time.Clock()
THICKNESS = 5

# tool selection
tool = "pen"  # pen, rect, circle, eraser
color = colorRED

# mouse state
LMBpressed = False
start_pos = (0, 0)

# canvas
screen.fill(colorBLACK)


# ---------------- HELPER FUNCTION ----------------
def draw_circle_preview(surface, start, end, color, thickness):
    # calculates radius from drag distance
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, thickness)


# ---------------- MAIN LOOP ----------------
running = True

while running:

    for event in pygame.event.get():

        # exit game
        if event.type == pygame.QUIT:
            running = False

        # ---------------- KEYBOARD CONTROLS ----------------
        if event.type == pygame.KEYDOWN:

            # tool selection
            if event.key == pygame.K_p:
                tool = "pen"        # free drawing
            if event.key == pygame.K_r:
                tool = "rect"       # rectangle tool
            if event.key == pygame.K_c:
                tool = "circle"     # circle tool
            if event.key == pygame.K_e:
                tool = "eraser"     # eraser tool

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
                THICKNESS -= 1

            # clear canvas
            if event.key == pygame.K_x:
                screen.fill(colorBLACK)

        # ---------------- MOUSE DOWN ----------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            start_pos = event.pos

        # ---------------- MOUSE UP ----------------
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False

            end_pos = event.pos

            # FINALIZE SHAPES
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
                draw_circle_preview(screen, start_pos, end_pos, color, THICKNESS)

        # ---------------- DRAWING WHILE MOVING ----------------
        if event.type == pygame.MOUSEMOTION and LMBpressed:

            pos = event.pos

            # PEN TOOL (free drawing)
            if tool == "pen":
                pygame.draw.circle(screen, color, pos, THICKNESS)

            # ERASER (draw black to erase)
            if tool == "eraser":
                pygame.draw.circle(screen, colorBLACK, pos, THICKNESS * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
