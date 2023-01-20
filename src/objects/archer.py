import pygame

import core
import entity
import sprites.archer
import objects.bullet


class Archer(entity.Entity, sprites.archer.Archer):
    """Enemy archer class."""

    def __init__(self, **kwargs):
        
        entity.Entity.__init__(self, **kwargs)
        sprites.archer.Archer.__init__(self, **kwargs)

        self.speed = kwargs["speed"]
        self.dir = kwargs["dir"]

        self.w = self.images_down[0].get_width()
        self.h = self.images_down[0].get_height()
        self.init_rect()
        
        self.attack_block = 1
        self.shooting = True
        self.attack_last = 0 # Time
        self.health = 3

        self.range_x = 150
        self.range_y = 40

    def action(self, player, elapsed_time):

        dis_x = self.rect.center[0] - player.rect.center[0]
        dis_y = self.rect.center[1] - player.rect.center[1]

        if 0 > dis_x > -self.range_x and self.range_y/2 > dis_y > -self.range_y/2:
            
            self.dir = core.RIGHT
            return self.shoot()
        
        if 0 > dis_y > -self.range_x and self.range_y/2 > dis_x > -self.range_y/2:
            
            self.dir = core.DOWN
            return self.shoot()
        
        if 0 < dis_x < self.range_x and self.range_y/2 > dis_y > -self.range_y/2:
            
            self.dir = core.LEFT
            return self.shoot()
        
        if 0 < dis_y < self.range_x and self.range_y/2 > dis_x > -self.range_y/2: 
            
            self.dir = core.UP
            return self.shoot()

        if dis_y > 0: pos_y = core.DOWN # Above
        else: pos_y = core.UP # Under
        
        if dis_x < 0 and pos_y == core.DOWN: pos_x = core.LEFT # Bottom left
        elif dis_x > 0 and pos_y == core.DOWN: pos_x = core.RIGHT # Bottom right
        elif dis_x < 0 and pos_y == core.UP: pos_x = core.LEFT # Top left
        else: pos_x = core.RIGHT # Top right
    
        match player.dir:
            
            case core.UP: 
                
                if pos_x == core.RIGHT:
                    
                    self.dir = core.RIGHT
                    self.move_up_right(elapsed_time)
                    return None
                
                else:
                    
                    self.dir = core.LEFT
                    self.move_up_left(elapsed_time)
                    return None
            
            case core.DOWN: 
                
                if pos_x == core.RIGHT: 
                    
                    self.dir = core.RIGHT
                    self.move_down_right(elapsed_time)
                    return None
                
                else: 
                    
                    self.dir = core.LEFT
                    self.move_down_left(elapsed_time)
                    return None
            
            case core.LEFT:
                
                if pos_y == core.DOWN: 
                    
                    self.dir = core.RIGHT
                    self.move_down_right(elapsed_time)
                    return None
                
                else: 
                    
                    self.dir = core.RIGHT
                    self.move_up_right(elapsed_time)
                    return None
            
            case core.RIGHT:
                
                if pos_y == core.DOWN: 
                    
                    self.dir = core.LEFT
                    self.move_down_left(elapsed_time)
                    return None
                
                else: 
                    
                    self.dir = core.LEFT
                    self.move_up_left(elapsed_time)
                    return None

    def shoot(self):
        """Shoot a bullet."""
        
        if self.shooting:
            
            self.attack_last = 0
            x = self.x + self.w/2
            y = self.y + self.h/2
            
            match self.dir:
                
                case core.UP: x, y = x-2, y-7
                case core.DOWN: x, y = x-2, y
                case core.LEFT: x, y = x-7, y-2
                case core.RIGHT: x, y = x-7, y-2
            
            return objects.bullet.Bullet(
                x = x,
                y = y,
                dir = self.dir,
                speed = 100,
                fac = core.ENEMY
            )
        
        else:
            return None

    def move(self, elapsed_time):
        """Automove the archer."""
        
        match self.dir:
            
            case core.UP: self.move_up(elapsed_time)
            case core.DOWN: self.move_down(elapsed_time)
            case core.LEFT: self.move_left(elapsed_time)
            case core.RIGHT: self.move_right(elapsed_time)
            case core.UP_LEFT: self.move_up_left(elapsed_time)
            case core.DOWN_LEFT: self.move_down_left(elapsed_time)
            case core.UP_RIGHT: self.move_up_right(elapsed_time)
            case core.DOWN_RIGHT: self.move_down_right(elapsed_time)
    
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
            self.shooting = False
            return

        # Attack block

        self.attack_last += elapsed_time

        if self.attack_last >= self.attack_block:
            self.shooting = True
        
        else:
            self.shooting = False