import pygame
import random
import math

import core
import entity
import sprites.bullet


class Bullet(entity.Entity, sprites.bullet.Bullet):
    """A class for the player's bullets."""

    def __init__(self, **kwargs) -> None:

        entity.Entity.__init__(self, **kwargs)
        sprites.bullet.Bullet.__init__(self, **kwargs)

        self.dir = kwargs["dir"]
        self.speed = kwargs["speed"]
        
        if self.dir == core.RIGHT or self.dir == core.LEFT:
            
            self.w = self.image_left.get_width()
            self.h = self.image_left.get_height()
        
        else:
            
            self.w = self.image_up.get_width()
            self.h = self.image_up.get_height()
        
        self.init_rect()

    def update(self, elapsed_time: float) -> None:
        """Update the flight of shooten bullets."""
        
        # Move forward

        if self.dir == core.RIGHT:
            self.move_right(elapsed_time)
        
        elif self.dir == core.LEFT:
            self.move_left(elapsed_time)
        
        elif self.dir == core.UP:
            self.move_up(elapsed_time)

        elif self.dir == core.DOWN:
            self.move_down(elapsed_time)
        
        elif self.dir == core.DOWN_LEFT:
            self.move_down_left(elapsed_time)
        
        elif self.dir == core.DOWN_RIGHT:
            self.move_down_right(elapsed_time)
        
        elif self.dir == core.UP_LEFT:
            self.move_up_left(elapsed_time)
        
        elif self.dir == core.UP_RIGHT:
            self.move_up_right(elapsed_time)
