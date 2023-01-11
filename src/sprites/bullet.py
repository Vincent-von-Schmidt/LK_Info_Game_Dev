import pygame

import core

class Bullet:
    """A sprite class for bullet movement."""

    def __init__(self, **kwargs):

        self.dir = kwargs["dir"]
        self.speed = kwargs["speed"]

        self.image_right = pygame.image.load("./assets/bullets/arrow_right.png")
        self.image_left = pygame.image.load("./assets/bullets/arrow_left.png")
        self.image_up = pygame.image.load("./assets/bullets/arrow_up.png")
        self.image_down = pygame.image.load("./assets/bullets/arrow_down.png")
    
    def move_up(self, elapsed_time: float = 0) -> float:
        """Move the sprite up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.speed * elapsed_time
        self.y -= dis

        self.dir = core.UP

        return dis
    
    def move_down(self, elapsed_time: float = 0) -> float:
        """Move the sprite down."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.speed * elapsed_time
        self.y += dis
        
        self.dir = core.DOWN

        return dis
    
    def move_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite left."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.speed * elapsed_time
        self.x -= dis

        self.dir = core.LEFT

        return dis
    
    def move_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite right."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.speed * elapsed_time
        self.x += dis

        self.dir = core.RIGHT

        return dis
    
    def move_up_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite up right."""

        dis = self.speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x += dis

        self.dir = core.RIGHT
        
        return 2*dis

    def move_up_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite up left."""

        dis = self.speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x -= dis

        self.dir = core.LEFT
        
        return 2*dis
    
    def move_down_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite down left."""

        dis = self.speed * elapsed_time / 2**0.5

        self.y += dis
        self.x -= dis
    
        self.dir = core.LEFT
        
        return 2*dis
    
    def move_down_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite down right."""

        dis = self.speed * elapsed_time / 2**0.5

        self.y += dis
        self.x += dis

        self.dir = core.RIGHT
        
        return 2*dis
    
    def update_sprite(self, elapsed_time: float) -> None:
        """Updates the players movement."""
        ...
    
    def _render(self) -> pygame.surface.Surface:
        """Render the bullet's image."""

        if self.dir == core.RIGHT:
            return self.image_right
        
        elif self.dir == core.LEFT:
            return self.image_left
        
        elif self.dir == core.UP:
            return self.image_up
        
        elif self.dir == core.DOWN: 
            return self.image_down