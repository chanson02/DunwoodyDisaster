import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
import dunwoody_disaster as DD
from typing import override
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster import Item
from PySide6.QtCore import Signal


class AttackAnimation(PygameAnimation):
    def __init__(self, background: str, player: str, enemy: str, weapon: str, onFinish: Signal):
        super().__init__()
        self.bkg = pygame.image.load(background).convert_alpha()  # 666x360 image
        self.player = pygame.transform.scale(pygame.image.load(player), (100, 100)).convert_alpha()
        self.enemy = pygame.transform.scale(pygame.image.load(enemy), (100, 100)).convert_alpha()
        self.weapon = pygame.transform.scale(pygame.image.load(weapon), (100, 100)).convert_alpha()
        self.weapon_x = 60
        self.finished = onFinish

    @override
    def run(self):
        if self.running:
            self.surface.blit(self.bkg, (7, 0))
            self.surface.blit(self.player, (100, 200))
            self.surface.blit(self.weapon, (self.weapon_x, 200))

            self.surface.blit(self.enemy, (450, 200))

            self.clock.tick(20)
            self.weapon_x += 10
            if self.weapon_x > 500:
                self.finished.emit()
