import pygame

import core
import sprites.sprite as sprite
import sprites.bullets as bullets

class Player(sprite.Sprite):

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



        super().__init__(
            speed = self.v,
            image_up = pygame.image.load("./assets/player_up.png"),
            image_down = pygame.image.load("./assets/player_down.png"),
            image_left = pygame.image.load("./assets/player_left.png"),
            image_right = pygame.image.load("./assets/player_right.png")
        )

    
    
    def shoot(self):
        return bullets(player.x, player.y)

#Create Sprites Group to draw them later 
# player = Player()
# player_group = pygame.sprite.Group()
# player_group.add(player)
#
# bullet = bullets()
# bullets_group = pygame.sprite.Group()
# bullets_group.add(bullet)
    

