import pygame

class PygameAnimation:
    def __init__(self, size: tuple[int, int] = (800, 600)):
        pygame.init()
        self.size = size
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(size, pygame.HIDDEN)
        self.running = False

        self.frames: list[pygame.Surface] = []
        self.frame_index = -1
        self.frame_count = 0
        self.frame_duration = 0
        self.last_frame_time = pygame.time.get_ticks()

    def current_frame(self) -> pygame.Surface:
        if self.frame_index == -1:
            raise Exception('No frames loaded')

        return self.frames[self.frame_index]

    def next_frame(self, clear=True) -> pygame.Surface:
        if clear:
            self.surface.fill((0, 0, 0))

        self.frame_index = (self.frame_index + 1) % self.frame_count
        self.last_frame_time = pygame.time.get_ticks()
        return self.current_frame()

    def should_render(self) -> bool:
        return pygame.time.get_ticks() - self.last_frame_time > self.frame_duration

    def load_frames(self) -> None:
        raise Exception("Unimplemented")

    def run(self) -> None:
        raise Exception("Unimplemented")

    def to_bytes(self):
        return pygame.image.tobytes(self.surface, "RGB")
