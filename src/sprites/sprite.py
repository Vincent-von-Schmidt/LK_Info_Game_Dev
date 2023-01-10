import pygame

import core

class Sprite:
    """Sprite class for basic movement, etc."""

    def __init__(self, **kwargs):

        self.step_speed = kwargs["speed"] # pix / s
        self.step_change = kwargs["change"] # s
        self.step_max = len(kwargs["images_up"]) - 1 # num
        self.attack_block = kwargs["attack_block"]

        self.x = 0
        self.y = 0
        self.step_last = 0 # Time
        self.step_idx = 0 # Index
        self.walking = False
        self.shooting = True
        self.attack_last = self.attack_block # Time

        self.images_up = kwargs["images_up"]
        self.images_down = kwargs["images_down"]
        self.images_left = kwargs["images_left"]
        self.images_right = kwargs["images_right"]

    def move_up(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.step_speed * elapsed_time) + pixel
        self.y -= dis

        if not still:
            self.pos = core.UP

        self.walking = True

        return dis
    
    def move_down(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite down."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.step_speed * elapsed_time) + pixel
        self.y += dis

        if not still:
            self.pos = core.DOWN

        self.walking = True

        return dis
    
    def move_left(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite left."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.step_speed * elapsed_time) + pixel
        self.x -= dis

        if not still:
            self.pos = core.LEFT
        
        self.walking = True

        return dis
    
    def move_right(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the sprite right."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.step_speed * elapsed_time) + pixel
        self.x += dis

        if not still:
            self.pos = core.RIGHT
        
        self.walking = True

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
        
        self.walking = True
        
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
        
        self.walking = True
        
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
        
        self.walking = True
        
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

        self.walking = True
        
        return dis
    
    def update(self, elapsed_time: float):
        
        # Movement

        self.step_last += elapsed_time
        self.step_idx += 1

        if self.step_last >= self.step_change:
            self.step_last -= self.step_change
        
        if self.step_idx > self.step_max:
            self.step_idx = 1
        
        if self.walking == False:
            self.step_idx = 0
        
        # Attack

        self.attack_last += elapsed_time

        if self.attack_last >= self.attack_block:
            self.shooting = True
        
        else:
            self.shooting = False


    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the sprite graphic."""

        # Movement

        if self.pos == core.RIGHT:
            return [(self.images_right[self.step_idx], (self.x, self.y))]
        
        elif self.pos == core.LEFT:
            return [(self.images_left[self.step_idx], (self.x, self.y))]
        
        elif self.pos == core.UP:
            return [(self.images_up[self.step_idx], (self.x, self.y))]
        
        elif self.pos == core.DOWN:
            return [(self.images_down[self.step_idx], (self.x, self.y))]
    
