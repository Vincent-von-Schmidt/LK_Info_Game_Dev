import pygame

import core
import entity
import sprites.archer
import sprites.player # Debug


class Archer(entity.Entity, sprites.player.Player):
    """Enemy archer class."""

    def __init__(self, **kwargs):
        
        entity.Entity.__init__(self, **kwargs)
        # sprites.archer.Archer.__init__(kwargs)
        sprites.player.Player.__init__(self, **kwargs)

        self.speed = kwargs["speed"]
        self.dir = kwargs["dir"]

        self.w = self.images_down[0].get_width()
        self.h = self.images_down[0].get_height()
        self.init_rect()
        
        self.goal = core.DOWN
    
    def update_health(self, health: float) -> None:
        """Update the archer's health."""

        return None
    
    def check_health(self) -> None:
        """Check the archer's health."""

        return None

    def update(self, elapsed_time: float):
        """Update archer stats."""

        # Walk

        if self.goal == core.DOWN:
            self.move_down(elapsed_time)

        elif self.goal == core.UP:
            self.move_up(elapsed_time)
        
        # Check
        
        if self.y >= 150:
            self.goal = core.UP
        
        elif self.y <= 70:
            self.goal = core.DOWN