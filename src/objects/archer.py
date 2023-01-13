import pygame

import core
import entity
import sprites.archer


class Archer(entity.Entity, sprites.archer.Archer):
    """Enemy archer class."""

    def __init__(self, **kwargs):
        
        entity.Entity.__init__(self, **kwargs)
        sprites.archer.Archer.__init__(self, **kwargs)

        self.speed = kwargs["speed"]
        self.dir = kwargs["dir"]

        self.w = self.images_down[0].get_width()
        self.h = self.images_down[0].get_height()
        
        self.goal = core.DOWN
        self.health = 3
    
    def update_health(self, health: float) -> None:
        """Update the archer's health."""

        self.health += health
    
    def check_health(self) -> bool:
        """Check the archer's health."""

        if self.health <= 0:
            return True
        
        return False

    def update(self, elapsed_time: float):
        """Update archer stats."""

        # Health check

        if self.check_health():

            self.active = False
            return

        # Walk

        if self.goal == core.DOWN:
            self.move_down(elapsed_time)

        elif self.goal == core.UP:
            self.move_up(elapsed_time)
        
        # Map check
        
        if self.y >= 150:
            self.goal = core.UP
        
        elif self.y <= 70:
            self.goal = core.DOWN