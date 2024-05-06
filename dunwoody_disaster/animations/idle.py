# import pygame
# import math
# from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
# import dunwoody_disaster as DD
#
#
# class IdleAnimation(PygameAnimation):
#     def __init__(self, background: str, player: str, enemy: str):
#         super().__init__()
#         self.bkg = pygame.image.load(background).convert_alpha()  # 666x360 image
#         self.player = pygame.transform.scale(pygame.image.load(player), (100, 100))
#         self.enemy = pygame.transform.scale(pygame.image.load(enemy), (100, 100))
#
#         self.bob_amplitude = 10
#         self.bob_frequency = 0.1
#         self.elapsed = 0
#
#     @DD.override
#     def run(self) -> None:
#         if self.running:
#             self.draw()
#             self.clock.tick(20)
#             self.elapsed += 1
#
#     def draw(self):
#         self.surface.blit(self.bkg, (7, 0))
#         factor = self.elapsed * self.bob_frequency + 0.5
#         offset = int(self.bob_amplitude * math.sin(factor))
#         self.surface.blit(self.player, (100, 200 + offset))
#         self.surface.blit(self.enemy, (450, 200 - offset))

import pygame
import math
from dunwoody_disaster.animations.AnimationComponent import AnimationComponent


class IdleComponent(AnimationComponent):
    def __init__(self, img: str, anchor: tuple[int, int]):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load(img), (100, 100))
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
