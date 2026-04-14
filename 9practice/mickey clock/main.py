import pygame 
from clock import Clock 

pygame.init()

screen = pygame.display.set_mode((500 , 500))
pygame.display.set_caption("Mickey clock")

clock = pygame.time.Clock()
logic = Clock()

center = (250 , 250)
hand=pygame.image.load("mickeys_clock/images/mickey_hand.png")

sec_hand=pygame.transform.scale(hand , (220 , 12))
right_hand=pygame.transform.scale(hand, (150 , 18))

def blit_rotate(screen , image , center , angle , length):
    rotated = pygame.transform.rotate(image , -angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated,rect)

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
            
    blit_rotate(screen , sec_hand , center , seconds_angles , 80)
    blit_rotate(screen , right_hand , center , minutes_angles , 50)
            
    pygame.draw.circle(screen , (0 , 0 , 0) , center , 5)
            
    pygame.display.flip()

pygame.quit()
