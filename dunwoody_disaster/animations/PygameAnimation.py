import pygame


class PygameAnimation:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((800, 600))
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        raise Exception('Unimplemented')

    def to_bytes(self):
        return pygame.image.tobytes(self.surface, 'RGB')
