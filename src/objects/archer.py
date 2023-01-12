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

        ...
    
    def update(self, elapsed_time: float):
        """Update archer stats."""

        ...