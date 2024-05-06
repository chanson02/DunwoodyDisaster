import pygame  # Import the pygame module for graphics and game development.
from typing import Optional  # Import Optional from typing for optional type hinting.


class PygameAnimation:
    """
    An abstract class for managing animations in pygame.
    """

    def __init__(self, size: tuple[int, int] = (800, 600)):
        """
        Initialize the PygameAnimation class with a default or specified size.
        :param size: The size of the surface, in pixels
        """
        pygame.init()  # Initialize all imported pygame modules.
        self.size = size  # Set the window size.
        self.clock = pygame.time.Clock()  # Create a clock object to manage frame rates.
        self.surface = pygame.display.set_mode(
            size, pygame.HIDDEN
        )  # Set up the display surface hidden from view.
        self.running = False  # Set the animation state to not running.

        self.frames: list[pygame.Surface] = (
            []
        )  # Initialize an empty list to hold frames.
        self.frame_index = 0  # Start the frame index at 0.
        self.frame_count = 0  # Initialize frame count.
        self.frame_duration = 0  # Set the duration each frame is shown.
        self.last_frame_time = 0  # Record the time the last frame was shown.

    def start(self):
        """
        Start the animation, setting the running state to True and resetting frame index.
        """
        self.running = True  # Set the animation as running.
        self.frame_index = 0  # Reset frame index to 0.
        self.last_frame_time = (
            pygame.time.get_ticks()
        )  # Update the last frame time to current tick count.

    def current_frame(self) -> pygame.Surface:
        """
        Return the current frame based on the frame index.
        """
        return self.frames[self.frame_index]  # Access and return the current frame.

    def next_frame(self, clear=True) -> pygame.Surface:
        """
        Update to the next frame, optionally clearing the display before drawing.
        :param clear: Whether to clear the display before drawing
        """
        if clear:
            self.surface.fill((0, 0, 0))  # Clear the display to black if clear is True.

        self.frame_index = (
            self.frame_index + 1
        ) % self.frame_count  # Increment and wrap the frame index.
        self.last_frame_time = (
            pygame.time.get_ticks()
        )  # Update the time of the last frame change.
        return self.current_frame()  # Return the new current frame.

    def should_render(self) -> bool:
        """
        Check if the next frame should be rendered based on the frame duration.
        """
        return (
            pygame.time.get_ticks() - self.last_frame_time > self.frame_duration
        )  # Compare current time with last frame time.

    def next_frame_if_ready(self, clear=True) -> Optional[pygame.Surface]:
        """
        Return the next frame only if it's time to update to the next frame based on frame duration.
        """
        if self.should_render():  # Check if it's time to render the next frame.
            return self.next_frame(clear)  # Get and return the next frame.
        return None  # Return None if it's not yet time for the next frame.

    def load_frames(self) -> None:
        """
        Method to be overridden in subclasses to load frames and their properties.
        """
        raise NotImplementedError(
            "load_frames must be implemented in subclass"
        )  # Force subclass implementation.

    def run(self) -> None:
        """
        Abstract method to be implemented by subclasses defining specific animation behavior.
        """
        raise NotImplementedError(
            "run method must be implemented in subclass"
        )  # Force subclass implementation.

    def to_bytes(self) -> bytes:
        """
        Convert the current surface to bytes.
        """
        return pygame.image.tobytes(
            self.surface, "RGB"
        )  # Convert the display surface to bytes in RGB format.
