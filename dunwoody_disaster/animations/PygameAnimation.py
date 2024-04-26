import pygame


class PygameAnimation:
    """
    An abstract class for manaing animations in pygame.
    """

    def __init__(self, size: tuple[int, int] = (800, 600)):
        """
        :param size: The size of the surface, in pixels
        """
        pygame.init()
        self.size = size
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(size, pygame.HIDDEN)
        self.running = False

        self.frames: list[pygame.Surface] = []
        self.frame_index = 0
        self.frame_count = 0
        self.frame_duration = 0
        self.last_frame_time = pygame.time.get_ticks()

    def current_frame(self) -> pygame.Surface:
        return self.frames[self.frame_index]

    def next_frame(self, clear=True) -> pygame.Surface:
        """
        Sets and returns the next frame of the animation
        :param clear: Whether to clear the display before drawing
        """
        if clear:
            self.surface.fill((0, 0, 0))

        self.frame_index = (self.frame_index + 1) % self.frame_count
        self.last_frame_time = pygame.time.get_ticks()
        return self.current_frame()

    def should_render(self) -> bool:
        """
        Check if the next frame is ready to be rendered based on frame duration
        """
        return pygame.time.get_ticks() - self.last_frame_time > self.frame_duration

    def load_frames(self) -> None:
        """
        This method should be overridden by subclasses to load
        self.frames
        self.frame_count
        self.frame_duration
        """
        raise NotImplementedError("load_frames must be implemented in subclass")

    def run(self) -> None:
        """
        This method should be overridden by subclasses to define behavior
        It's responsible for drawing the frames to the surface and loops
        :example:
            if self.running and self.should_render():
                self.surface.blit(self.next_frame(), (1, 1))
        :example:
            if self.running:
                pygame.draw.circiel(self.surface, (255, 0, 0), (200, 150), 50)
                self.clock.tick(60)
        """
        raise NotImplementedError("run method must be implemented in subclass")

    def to_bytes(self) -> bytes:
        return pygame.image.tobytes(self.surface, "RGB")
