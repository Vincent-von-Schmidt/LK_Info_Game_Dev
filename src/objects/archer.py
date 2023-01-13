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
        ...
    
    def update_health(self, health: float) -> None:
        """Update the archer's health."""

        return None
    
    def check_health(self) -> None:
        """Check the archer's health."""

        return None
    
    def movement_lane_down(self, elapsed_time):
        self.move_down()
        dis = self.speed * elapsed_time
        self.y += dis
        if self.y >= 170: 
            self.dir = core.UP
            return
            

    def movement_lane_up(self, elapsed_time):
        self.move_up()
        dis = self.speed * elapsed_time
        self.y -= dis
        if self.y <= 50:
            self.dir = core.DOWN
            return
        ...


    def update(self, elapsed_time: float):
        """Update archer stats."""
        if self.dir == core.DOWN:
            self.movement_lane_down(elapsed_time)

        elif self.dir == core.UP: 
            self.movement_lane_up(elapsed_time)
        ...