import pygame
import math
from dunwoody_disaster.animations.AnimationComponent import AnimationComponent


class IdleComponent(AnimationComponent):
    def __init__(self, img: str, anchor: tuple[int, int], size=(100, 100)):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load(img), size)
        self.anchor = anchor

        self.elapsed = 0
        self.bob_frequency = 0.1
        self.bob_amplitude = 10

    def draw(self, surface: pygame.Surface) -> tuple[int, int]:
        factor = self.elapsed * self.bob_frequency + 0.5
        offset = int(self.bob_amplitude * math.sin(factor))
        pos = (self.anchor[0], self.anchor[1] + offset)
        surface.blit(self.img, pos)
        self.elapsed += 1
        return pos
