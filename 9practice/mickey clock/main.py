import pygame 
from clock import Clock 
import math

pygame.init()

screen = pygame.display.set_mode((500 , 500))
pygame.display.set_caption("Mickey clock")

clock = pygame.time.Clock()
logic = Clock()

center = (250 , 250)

hand = pygame.image.load("mickeys_clock/images/mickey_hand.png")
sec_hand = pygame.transform.scale(hand , (220 , 12))
right_hand = pygame.transform.scale(hand, (150 , 18))

def blit_rotate(screen , image , center , angle):
    rotated = pygame.transform.rotate(image , -angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated, rect)

running = True
while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    minutes_angles , seconds_angles = logic.currently_time()

    screen.fill((255 , 255 , 255))

    pygame.draw.circle(screen, (0, 0, 0), center, 205, 6)
    pygame.draw.circle(screen, (0, 0, 0), center, 195, 2)

    for i in range(60):
        angle = math.radians(i * 6 - 90)

        x1 = center[0] + 190 * math.cos(angle)
        y1 = center[1] + 190 * math.sin(angle)

        if i % 5 == 0:
            length = 20
        else:
            length = 10

        x2 = center[0] + (190 - length) * math.cos(angle)
        y2 = center[1] + (190 - length) * math.sin(angle)

        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

    font = pygame.font.SysFont(None, 30)

    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)

        x = center[0] + 150 * math.cos(angle)
        y = center[1] + 150 * math.sin(angle)

        text = font.render(str(i), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))

        screen.blit(text, text_rect)

    blit_rotate(screen , sec_hand , center , seconds_angles)
    blit_rotate(screen , right_hand , center , minutes_angles)

    pygame.draw.circle(screen , (0 , 0 , 0) , center , 5)

    pygame.display.flip()

pygame.quit()
