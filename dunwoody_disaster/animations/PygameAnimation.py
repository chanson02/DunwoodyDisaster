import pygame
from typing import Optional


class PygameAnimation:
    """
    An abstract class for managing animations in pygame.
    """

    def __init__(self, size: tuple[int, int] = (680, 360)):
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
        self.last_frame_time = 0

    def start(self):
        """
        Start the animation, at the first frame
        """
        self.running = True
        self.frame_index = 0
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

    def next_frame_if_ready(self, clear=True) -> Optional[pygame.Surface]:
        """
        Return a frame to render only if the previous frames duration is up
        :param clear:Whether to clear the display before drawing
        """
        if self.should_render():
            return self.next_frame(clear)
        return None

    def load_frames(self) -> None:
        """
        This method should be overridden by subclasses to load:
        self.frames
        self.frame_count
        self.frame_duration
        """
        raise NotImplementedError("load_frames must be implemented in subclass")

    def run(self) -> None:
        """
        This method should be overridden by subclasses to define behavior
        It's responsible for drawing the frames to the surface and loops
        :frame example:
            if self.running and self.should_render():
                self.surface.blit(self.next_frame(), (1, 1))
        :draw example:
            if self.running:
                pygame.draw.circiel(self.surface, (255, 0, 0), (200, 150), 50)
                self.clock.tick(60)
        """
        raise NotImplementedError("run method must be implemented in subclass")

    def to_bytes(self) -> bytes:
        return pygame.image.tobytes(self.surface, "RGB")
