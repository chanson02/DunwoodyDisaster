import pygame
import sys

# Initialize Pygame
pygame.init()

# Set initial screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Set default dimensions if needed
# Create a resizable screen with the default dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pokémon Battle Simulator")

# Load images after initializing the screen
background_img = pygame.image.load(
    "DunwoodyDisaster/dunwoody_disaster/assets/background.jpg"
).convert()

# Optionally, adjust the screen size to match the background image dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = background_img.get_width(), background_img.get_height()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Game variables
player_health = 100
enemy_health = 100
clock = pygame.time.Clock()  # Create a clock object
FPS = 60  # Frames per second


def draw_battle(screen, background_img):
    # Redraw background to fit the new window size
    scaled_bg = pygame.transform.scale(
        background_img, (screen.get_width(), screen.get_height())
    )
    screen.blit(scaled_bg, (0, 0))
    pygame.display.flip()  # Update display after drawing


def attack(target):
    return max(target - 20, 0)


def heal(target):
    # Function to heal the target, increasing health by 15 points, up to a maximum of 100.
    return min(target + 15, 100)  # Ensure health does not exceed 100


def main():
    global screen  # Declare global if screen might be reassigned within this function
    running = True
    player_turn = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Attack and switch turns
                    global enemy_health, player_health
                    if player_turn:
                        enemy_health = attack(enemy_health)
                    else:
                        player_health = attack(player_health)
                    player_turn = not player_turn  # Switch turn after action
                elif event.key == pygame.K_h:
                    # Heal the player if it's their turn
                    if player_turn:
                        player_health = heal(player_health)
            elif event.type is pygame.VIDEORESIZE:
                # Update the screen object to new size
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                draw_battle(screen, background_img)

        draw_battle(screen, background_img)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
