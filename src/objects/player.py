import pygame

import core
import entity
import sprites.player
import objects.bullet

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

        # Hitbox

        self.w = self.images_down[0].get_width()
        self.h = self.images_down[0].get_height()
        self.init_rect()

        # Properties

        self.attack_block = 1
        self.shooting = True
        self.attack_last = 0 # Time
        self.max_health = 3
        self.health = 3

    def update(self, elapsed_time: float):

        # Health check

        if self.check_health():

            self.active = False
            self.shooting = False
            return
        
        # Attack block

        self.attack_last += elapsed_time

        if self.attack_last >= self.attack_block:
            self.shooting = True
        
        else:
            self.shooting = False
    
    def update_health(self, health: float) -> None:
        """Update the player's health."""

        self.health += health
    
    def check_health(self) -> bool:
        """Check the player's health."""

        if self.health <= 0:
            return True
        
        return False

    def shoot(self):
        if self.shooting:
            self.attack_last = 0
            x = self.x + self.w/2
            y = self.y + self.h/2
            match self.dir:
                case core.UP: x, y = x-2, y-7
                case core.DOWN: x, y = x-2, y-8
                case core.LEFT: x, y = x-7, y-7
                case core.RIGHT: x, y = x-7, y-7
            return objects.bullet.Bullet(
                                x=x,
                                y=y,
                                dir=self.dir,
                                speed=100,
                                fac=core.FRIEND)
        else: return None