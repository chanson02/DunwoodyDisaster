import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
import dunwoody_disaster as DD
from typing import override
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster import Item

class AttackAnimation(PygameAnimation):
    def __init__(self):
        super().__init__()
        self.bkg = pygame.image.load(DD.ASSETS["LectureHall"]).convert() # 666x360 image
        self.player = pygame.transform.scale(pygame.image.load(CharacterFactory.Cooper().image_path), (100, 100))
        self.enemy = pygame.transform.scale(pygame.image.load(CharacterFactory.RyanRengo().image_path), (100, 100))

        self.weapon = pygame.transform.scale(pygame.image.load(Item.weapons[0].image), (100, 100))
        self.weapon_x = 60

    @override
    def run(self):
        if self.running:
            self.surface.blit(self.bkg, (0, 0))
            self.surface.blit(self.player, (100, 200))
            self.surface.blit(self.weapon, (self.weapon_x, 200))

            self.surface.blit(self.enemy, (450, 200))

            self.clock.tick(120)
            self.weapon_x += 1
            if self.weapon_x > 500:
                self.weapon_x = 60
