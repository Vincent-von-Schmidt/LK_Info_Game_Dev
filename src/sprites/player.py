import pygame

import core

#Create Sprites Group to draw them later 
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()



class Player:
    """Player class."""

    def __init__(self) -> None:
        """Initialisation of player objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Properties

        self.v = 1000 # Pixel / Second

        self.x = 320
        self.y = 240
        self.pos = core.RIGHT

        self.image_up = pygame.image.load("./assets/player_up.png")
        self.image_down = pygame.image.load("./assets/player_down.png")
        self.image_left = pygame.image.load("./assets/player_left.png")
        self.image_right = pygame.image.load("./assets/player_right.png")

    def move_up(
        self, elapsed_time: float = 0, pixel: float = 0, still=False
    ) -> float:
        """Move the player up."""

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
        """Move the player up."""

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
        """Move the player up."""

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
        """Move the player up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = (self.v * elapsed_time) + pixel
        self.x += dis

        if not still:
            self.pos = core.RIGHT

        return dis
    
    def shoot(self):
        ...










    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the player graphic."""

        if self.pos == core.RIGHT:
            return [(self.image_right, (self.x, self.y))]
        
        elif self.pos == core.LEFT:
            return [(self.image_left, (self.x, self.y))]
        
        elif self.pos == core.UP:
            return [(self.image_up, (self.x, self.y))]
        
        elif self.pos == core.DOWN:
            return [(self.image_down, (self.x, self.y))]

