import pygame
import math
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
import dunwoody_disaster as DD
from dunwoody_disaster import ASSETS

#from typing import override

class IdleAnimation(PygameAnimation):
    def __init__(self, background: str, player: str, enemy: str):
        super().__init__()
        self.bkg = pygame.image.load(background).convert_alpha()  # 666x360 image
        self.player = pygame.transform.scale(pygame.image.load(player), (100, 100))
        self.enemy = pygame.transform.scale(pygame.image.load(enemy), (100, 100))

        self.bob_amplitude = 10
        self.bob_frequency = 0.1
        self.elapsed = 0

    #@override
    def run(self) -> None:
        if self.running:
            self.draw()
            self.clock.tick(20)
            self.elapsed += 1

    def draw(self):
        self.surface.blit(self.bkg, (7, 0))
        factor = self.elapsed * self.bob_frequency + 0.5
        offset = int(self.bob_amplitude * math.sin(factor))
        self.surface.blit(self.player, (100, 200 + offset))
        self.surface.blit(self.enemy, (450, 200 - offset))
