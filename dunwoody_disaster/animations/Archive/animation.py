# File: animation.py
import pygame
import sys


class Animation:
    def __init__(self, path, frame_count):
        self.frames = self.load_animation(path, frame_count)
        self.current_frame = 0
        self.frame_count = len(self.frames)
        self.frame_duration = 100  # Duration each frame is displayed, in milliseconds
        self.last_frame_time = pygame.time.get_ticks()

    def load_animation(self, path, frame_count):
        frames = []
        for i in range(frame_count):
            frame_path = f"{path}_{str(i + 1).zfill(2)}.png"
            try:
                frames.append(pygame.image.load(frame_path).convert_alpha())
            except pygame.error as e:
                print(f"Error loading {frame_path}: {e}")
                sys.exit(1)
        return frames

    def update(self):
        if pygame.time.get_ticks() - self.last_frame_time > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.last_frame_time = pygame.time.get_ticks()

    def draw(self, screen, x, y):
        screen.blit(self.frames[self.current_frame], (x, y))
