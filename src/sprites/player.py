import pygame

import core
import entity
import sprites.sprite as sprite

class Player(sprite.Sprite):
    """Player class."""

    def __init__(self) -> None:
        """Initialisation of player objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Properties

        super().__init__(
            x = 120,
            y = 96,
            pos = core.DOWN,
            speed = 30, # Pixel / Second
            change = 0.2, # Seconds
            attack_block = 1,
            max_health = 3,
            health = 1.5,
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
