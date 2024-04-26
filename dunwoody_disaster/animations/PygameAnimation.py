import pygame
import sys


def load_animation(path, frame_count):
    frames = []
    for i in range(frame_count):
        # Frame files are named like 'sprite_01.png', 'sprite_02.png', etc.
        frame_path = f"{path}_{str(i+1).zfill(2)}.png"
        frames.append(pygame.image.load(frame_path).convert_alpha())
    return frames


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Define the base path and filename prefix for the animation frames
animation_base_path = r"C:/Users/vuejohw/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/animations/Animation_Assets/idle"

# Load animation frames
animation_frames = load_animation(
    animation_base_path, 8
)  # Adjust the number of frames as needed

# Animation variables
current_frame = 0
frame_count = len(animation_frames)
frame_duration = 100  # Duration each frame is displayed, in milliseconds
last_frame_time = pygame.time.get_ticks()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False

    # Update the frame based on time
    if pygame.time.get_ticks() - last_frame_time > frame_duration:
        current_frame = (current_frame + 1) % frame_count
        last_frame_time = pygame.time.get_ticks()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the current frame
    screen.blit(animation_frames[current_frame], (350, 250))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
