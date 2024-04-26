import pygame
import sys
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation

from typing import override



class IdleAnimation(PygameAnimation):
    def __init__(self):
        super().__init__()
        self.load_frames()

    @override
    def load_frames(self):
        self.frames = []
        self.frame_count = 8
        self.frame_duration = 100


        BASE_PATH = "C:/Users/vuejohw/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster"
        BASE_PATH = "/home/chanson/Documents/ds_algs/SENG3340"
        animation_base_path = f"{BASE_PATH}/dunwoody_disaster/animations/Animation_Assets/Idle"

        for i in range(self.frame_count):
            path = f"{animation_base_path}_{str(i+1).zfill(2)}.png"
            self.frames.append(pygame.image.load(path).convert_alpha())


    @override
    def run(self) -> None:
        if self.running and self.should_render():
            self.surface.blit
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.next_frame(), (350, 250))
