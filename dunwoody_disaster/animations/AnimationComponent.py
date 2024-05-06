import pygame
from PySide6.QtCore import SignalInstance
from typing import Optional


class AnimationComponent:
    is_finished = False

    def __init__(self, finish: Optional[SignalInstance] = None):
        self.onFinish = finish

    def finished(self) -> bool:
        return self.is_finished

    def draw(self, surface: pygame.Surface) -> tuple[int, int]:
        _ = surface
        raise NotImplementedError("draw must be a method on subclasses")
