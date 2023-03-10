import pygame

import core

class Archer:
    """Enemy archer spirit class."""

    def __init__(self, **kwargs) -> None:

        self.dir = kwargs["dir"]

        self.step_max = 3 - 1 # Num
        self.step_last = 0 # Time
        self.step_idx = 0 # Index
        self.step_stop = True # Bool

        self.step_speed = kwargs["speed"] # pix / s
        self.step_change = kwargs["change"] # s

        self.images_up = (
            pygame.image.load("./assets/archer/archer_up_0.png"),
            pygame.image.load("./assets/archer/archer_up_1.png"),
            pygame.image.load("./assets/archer/archer_up_2.png")
        )
        self.images_down = (
            pygame.image.load("./assets/archer/archer_down_0.png"),
            pygame.image.load("./assets/archer/archer_down_1.png"),
            pygame.image.load("./assets/archer/archer_down_2.png")
        )
        self.images_left = (
            pygame.image.load("./assets/archer/archer_left_0.png"),
            pygame.image.load("./assets/archer/archer_left_1.png"),
            pygame.image.load("./assets/archer/archer_left_2.png")
        )
        self.images_right = (
            pygame.image.load("./assets/archer/archer_right_0.png"),
            pygame.image.load("./assets/archer/archer_right_1.png"),
            pygame.image.load("./assets/archer/archer_right_2.png")
        )
        self.images_up_right = self.images_right
        self.images_up_left = self.images_left
        self.images_down_left = self.images_left
        self.images_down_right = self.images_right
    
    def move_up(self, elapsed_time: float = 0) -> float:
        """Move the sprite up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.y -= dis

        self.dir = core.UP
        self.step_stop = False

        return dis
    
    def move_down(self, elapsed_time: float = 0) -> float:
        """Move the sprite down."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.y += dis
        
        self.dir = core.DOWN
        self.step_stop = False

        return dis
    
    def move_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite left."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.x -= dis

        self.dir = core.LEFT
        self.step_stop = False

        return dis
    
    def move_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite right."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.x += dis

        self.dir = core.RIGHT
        self.step_stop = False

        return dis
    
    def move_up_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite up right."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x += dis

        self.dir = core.UP_RIGHT
        self.step_stop = False
        
        return 2*dis

    def move_up_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite up left."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x -= dis

        self.dir = core.UP_LEFT
        self.step_stop = False
        
        return 2*dis
    
    def move_down_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite down left."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y += dis
        self.x -= dis
    
        self.dir = core.DOWN_LEFT
        self.step_stop = False
        
        return 2*dis
    
    def move_down_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite down right."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y += dis
        self.x += dis

        self.dir = core.DOWN_RIGHT
        self.step_stop = False
        
        return 2*dis
    
    def update_sprite(self, elapsed_time: float) -> None:
        """Update the archer animation."""

        if not self.step_stop:
            self.step_last += elapsed_time

        while self.step_last >= self.step_change:

            self.step_idx += 1
            self.step_last -= self.step_change
        
        if self.step_idx > self.step_max:
            self.step_idx = 0 # 1
        
        if self.step_stop:
            self.step_idx = 0
        
        self.step_stop = True

    def _render(self) -> pygame.surface.Surface:
        """Render the sprite graphic."""

        # Movement

        if self.dir == core.RIGHT:
            return self.images_right[self.step_idx]
        
        elif self.dir == core.LEFT:
            return self.images_left[self.step_idx]
        
        elif self.dir == core.UP:
            return self.images_up[self.step_idx]
        
        elif self.dir == core.DOWN:
            return self.images_down[self.step_idx]
        
        elif self.dir == core.DOWN_RIGHT:
            return self.images_down_right[self.step_idx]
        
        elif self.dir == core.DOWN_LEFT:
            return self.images_down_left[self.step_idx]
        
        elif self.dir == core.UP_LEFT:
            return self.images_up_left[self.step_idx]
        
        elif self.dir == core.UP_RIGHT:
            return self.images_up_right[self.step_idx]