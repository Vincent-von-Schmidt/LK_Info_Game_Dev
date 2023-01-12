import pygame

import core
import entity
import sprites.player

class Player(entity.Entity, sprites.player.Player):
    """Player class."""

    def __init__(self, **kwargs) -> None:
        """Initialisation of player objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Sprite

        entity.Entity.__init__(self, **kwargs)
        sprites.player.Player.__init__(self, **kwargs)

        # Properties

        self.attack_block = 1
        self.shooting = True
        self.attack_last = 0 # Time
        self.max_health = 3
        self.health = 1.5

    def update(self, elapsed_time: float):

        self.attack_last += elapsed_time

        if self.attack_last >= self.attack_block:
            self.shooting = True
        
        else:
            self.shooting = False
    
    def update_health(self, health: float) -> None:
        """Update the player's health."""

        return None
    
    def check_health(self) -> None:
        """Check the player's health."""

        return None