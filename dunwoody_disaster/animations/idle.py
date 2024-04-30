import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
import dunwoody_disaster as DD
from dunwoody_disaster import ASSETS

# from typing import override


class IdleAnimation(PygameAnimation):
    def __init__(
        self,  # animation_path: str, frame_count: int = 8, frame_duration: int = 100#
    ):
        super().__init__()
        """         self.animation_base_path = animation_path
        self.frame_count = frame_count
        self.frame_duration = frame_duration """
        self.load_frames()

    # @override
    def load_frames(self):
        self.frames = []
        self.frame_count = 8
        self.frame_duration = 100
        animation_base_path = f"{DD.ANIMATION_PATH}/Idle"
        self.background_img = pygame.image.load(ASSETS["background"]).convert()

        for i in range(self.frame_count):
            path = f"{animation_base_path}_{str(i + 1).zfill(2)}.png"
            self.frames.append(pygame.image.load(path).convert_alpha())

    # @override
    def run(self) -> None:
        if self.running and self.should_render():
            self.surface.blit(
                pygame.transform.scale(self.background_img, self.surface.get_size()),
                (0, 0),
            )
            self.surface.blit(self.next_frame(False), (350, 250))

    def draw(self, screen, position, dimensions):
        """Draw the current frame of the animation on the provided screen at the specified position."""
        frame = self.current_frame()
        frame = pygame.transform.scale(frame, dimensions)
        screen.blit(frame, position)
