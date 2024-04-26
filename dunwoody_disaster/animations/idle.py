import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
import dunwoody_disaster as DD
# from typing import override


class IdleAnimation(PygameAnimation):
    def __init__(self):
        super().__init__()
        self.load_frames()

    # @override
    def load_frames(self):
        self.frames = []
        self.frame_count = 8
        self.frame_duration = 100
        animation_base_path = f"{DD.ANIMATION_PATH}/Idle"

        for i in range(self.frame_count):
            path = f"{animation_base_path}_{str(i + 1).zfill(2)}.png"
            self.frames.append(pygame.image.load(path).convert_alpha())

    # @override
    def run(self) -> None:
        if self.running and self.should_render():
            self.surface.blit(self.next_frame(), (350, 250))
