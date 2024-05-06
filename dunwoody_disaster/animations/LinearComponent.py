import pygame
import time
from dunwoody_disaster.animations.AnimationComponent import AnimationComponent
from PySide6.QtCore import SignalInstance


class LinearComponent(AnimationComponent):
    def __init__(self, img: str, finish: SignalInstance, start: tuple[int, int], end: tuple[int, int], duration_ms = 0):
        super().__init__(finish)

        self.img = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (100, 100))
        self.start = start
        self.end = end
        self.duration = duration_ms
        self.start_time = 0

    def time_ms(self) -> int:
        return int(time.time_ns() / 1000000)

    def draw(self, surface: pygame.Surface) -> tuple[int, int]:
        if self.is_finished:
            return (0, 0)

        if self.start_time == 0:
            self.start_time = self.time_ms()
        elapsed = self.time_ms() - self.start_time
        progress = min(elapsed / self.duration, 1)
        pos = (
                int(self.start[0] + (self.end[0] - self.start[0]) * progress),
                int(self.start[1] + (self.end[1] - self.start[1]) * progress)
                )
        surface.blit(self.img, pos)

        if elapsed >= self.duration:
            self.is_finished = True
            self.onFinish.emit()

        return pos
