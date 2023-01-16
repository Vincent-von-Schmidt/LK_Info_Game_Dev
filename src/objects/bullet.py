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
        # self.target = kwargs["target"]
        if self.dir == core.RIGHT or self.dir == core.LEFT:
            self.w = self.image_left.get_width()
            self.h = self.image_left.get_height()
        else:
            self.w = self.image_up.get_width()
            self.h = self.image_up.get_height()
        self.init_rect()

        # self.xl, self.yl = self.x, self.y # Last point

        # # Build flight trajectory

        # x1, y1 = self.x, self.y
        # x2, y2 = self.target.x, self.target.y

        # a = (y1-y2) / (x2**2-x1**2)
        # sign = random.choice((-1, +1))
        # yv = random.randint(208 - 176, 208) # Vertex
        # xv = x1 - sign * (
        #     (y1-yv) * (x2**2-x1**2) / (y1-y2)
        # )**0.5

        # self.trajectory = lambda x: (a * (x-xv)**2 + yv) # ypos(xpos)
        # self.derivation = lambda x: (2*a*x - 2*a) # ypos'(xpos)
        # self.distance = lambda x: (
        #     x * ( 1 + 4*a**2*x**2 )**0.5
        #     + math.log(  )
        # ) # ydis(xpos)

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
