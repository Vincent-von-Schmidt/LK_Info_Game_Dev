import pygame 

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

        self.end = False

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
        
        # End flight
        
        if self.x >= 200:
            self.end = True
        
        elif self.x <= 0: 
            self.end = True 
        
        elif self.y <= 0:
            self.end = True 
        
        elif self.y >= 500: 
            self.end = True
