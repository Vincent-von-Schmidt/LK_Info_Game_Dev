import pygame

import core


class Background:
    """Background class."""

    def __init__(self) -> None:
        """Initialisation of background objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Properties

        self.v = 1000 # Pixel / Second

        self.x = 0
        self.y = 0

        self.image = pygame.image.load("./assets/map/background.png")

    def move_up(self, elapsed_time: float = 0, pixel: float = 0) -> float:
        """Move the background up."""

        ################################################################
        # 1. Change the background position.                           #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.y += dis

        return dis
    
    def move_down(self, elapsed_time: float = 0, pixel: float = 0) -> float:
        """Move the background up."""

        ################################################################
        # 1. Change the background position.                           #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.y -= dis

        return dis
    
    def move_left(self, elapsed_time: float = 0, pixel: float = 0) -> float:
        """Move the background up."""

        ################################################################
        # 1. Change the background position.                           #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.x += dis

        return dis
    
    def move_right(self, elapsed_time: float = 0, pixel: float = 0) -> float:
        """Move the background up."""

        ################################################################
        # 1. Change the background position.                           #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.x -= dis

        return dis
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the background graphic."""
        
        return [(self.image, (self.x, self.y))]
