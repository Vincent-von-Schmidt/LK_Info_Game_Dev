import pygame

import core


class Sprite:
    """Sprite class for basic movement, etc."""

    def __init__(self, **kwargs):

        self.x = 0
        self.y = 0

        self.speed = kwargs["speed"] # pix / s

        self.image_up = kwargs["image_up"]
        self.image_down = kwargs["image_down"]
        self.image_left = kwargs["image_left"]
        self.image_right = kwargs["image_right"]

    def move_up(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.y -= dis

        if not still:
            self.pos = core.UP

        return dis
    
    def move_down(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite down."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.y += dis

        if not still:
            self.pos = core.DOWN

        return dis
    
    def move_left(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite left."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.x -= dis

        if not still:
            self.pos = core.LEFT

        return dis
    
    def move_right(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite right."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.x += dis

        if not still:
            self.pos = core.RIGHT

        return dis
    
    def move_up_right(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ):
        """Move the sprite up right."""

        dis = 0
        dis += self.move_up(elapsed_time/2, still=True)
        dis += self.move_right(elapsed_time/2, still=True)

        if not still:
            self.pos = core.RIGHT
        
        return dis

    def move_up_left(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ):
        """Move the sprite up left."""

        dis = 0
        dis += self.move_up(elapsed_time/2, still=True)
        dis += self.move_left(elapsed_time/2, still=True)

        if not still:
            self.pos = core.LEFT
        
        return dis
    
    def move_down_left(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ):
        """Move the sprite down left."""

        dis = 0
        dis += self.move_down(elapsed_time/2, still=True)
        dis += self.move_left(elapsed_time/2, still=True)

        if not still:
            self.pos = core.LEFT
        
        return dis
    
    def move_down_right(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ):
        """Move the sprite down right."""

        dis = 0
        dis += self.move_down(elapsed_time/2, still=True)
        dis += self.move_right(elapsed_time/2, still=True)

        if not still:
            self.pos = core.RIGHT
        
        return dis

    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the sprite graphic."""

        if self.pos == core.RIGHT:
            return [(self.image_right, (self.x, self.y))]
        
        elif self.pos == core.LEFT:
            return [(self.image_left, (self.x, self.y))]
        
        elif self.pos == core.UP:
            return [(self.image_up, (self.x, self.y))]
        
        elif self.pos == core.DOWN:
            return [(self.image_down, (self.x, self.y))]
    
