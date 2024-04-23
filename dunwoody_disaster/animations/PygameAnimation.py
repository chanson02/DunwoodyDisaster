import pygame


class PygameAnimation:
    def __init__(self, size: tuple[int, int] = (800, 600)):
        pygame.init()
        self.size = size
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(size, pygame.HIDDEN)
        self.running = False

    def run(self) -> None:
        raise Exception("Unimplemented")

    def to_bytes(self):
        return pygame.image.tobytes(self.surface, "RGB")
