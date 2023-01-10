import pygame 
import sprites.player as player
import core 

pygame.init()


class Bullets(pygame.sprite.Sprite): 
    def __init__(self, pos_x, pos_y, dir) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (pos_y, pos_x))
        self.end = False
        self.vel = 1000

    def update(self, elapsed_time, dir): 

        v = elapsed_time * self.vel
        
        if dir == core.RIGHT:
            self.rect.x += v
        
        elif dir == core.LEFT:
            self.rect.x -= 5 
        
        elif dir == core.UP:
            self.rect.y -= 5 

        elif dir == core.DOWN:
            self.rect.y += 5 

    def kill(self): 
        if self.rect.x >= 200:
            self.end = True
    
    def render(self): 
        return [(self.image, (self.rect.centerx, self.rect.centery))]







