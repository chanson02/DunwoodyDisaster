import pygame
import sys
from Fighter import Fighter

# Initialize
pygame.init()

# Screen Size
Screen_Width = 1000
Screen_Height = 600

# Set up the display
screen = pygame.display.set_mode((Screen_Width, Screen_Height))  # screen is surface
pygame.display.set_caption("Dunwoody Disaster")


# set framerate
clock = pygame.time.Clock()
FPS = 60


# Load background image
bg_image = pygame.image.load("8Bit Animation Work/Images/CourtYard.png").convert_alpha()


# funciton to draw the background image
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (Screen_Width, Screen_Height))
    screen.blit(scaled_bg, (0, 0))


# create two instances of fighters
fighter_1 = Fighter(200, 310)  # x, y coordinates
fighter_2 = Fighter(700, 310)

# Main game loop
running = True
while running:

    clock.tick(FPS)

    # draw background
    draw_bg()

    # move fighters
    fighter_1.move(Screen_Width, Screen_Height, screen, fighter_2)
    fighter_2.move(Screen_Width, Screen_Height, screen, fighter_1)

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
