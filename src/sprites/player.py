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

        self.v = 300 # Pixel / Second

        self.x = 320
        self.y = 240
        self.pos = core.RIGHT

        super().__init__(
            speed = self.v,
            change = 3,
            images_up = (
                pygame.image.load("./assets/player/player_up_0.png"),
                pygame.image.load("./assets/player/player_up_1.png"),
                pygame.image.load("./assets/player/player_up_2.png"),
            ),
            images_down = (
                pygame.image.load("./assets/player/player_down_0.png"),
                pygame.image.load("./assets/player/player_down_1.png"),
                pygame.image.load("./assets/player/player_down_2.png")
            ),
            images_left = (
                pygame.image.load("./assets/player/player_left_0.png"),
                pygame.image.load("./assets/player/player_left_1.png"),
                pygame.image.load("./assets/player/player_left_2.png")
            ),
            images_right = (
                pygame.image.load("./assets/player/player_right_0.png"),
                pygame.image.load("./assets/player/player_right_1.png"),
                pygame.image.load("./assets/player/player_right_2.png")
            )
        )

    



