import pygame 
import sprites.player as player
import core 


class Bullets:

    def __init__(self, pos_x, pos_y, dir) -> None:
        
        super().__init__()

        #horizontal bullets
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

        #vertical bullets
        self.image2 = pygame.Surface((10, 50))
        self.image2.fill((0, 255, 0))
        self.rect2 = self.image.get_rect(center =(pos_x, pos_y))

        self.end = False
        self.vel = 1000
        self.dir = dir

    def update(self, elapsed_time):

        v = elapsed_time * self.vel
        
        if self.dir == core.RIGHT:
            self.rect.x += v
        
        elif self.dir == core.LEFT:
            self.rect.x -= 5 
        
        elif self.dir == core.UP:
            self.rect2.y -= 5 

        elif self.dir == core.DOWN:
            self.rect2.y += 5 

    def kill(self): 
        if self.rect.x >= 200:
            self.end = True
        
        elif self.rect.y >= 500: 
            self.end = True 
    
    def render(self): 
        if self.dir == core.RIGHT or self.dir == core.LEFT:
            return [(self.image, (self.rect.centerx, self.rect.centery))] 
        else: 
            return [(self.image2, (self.rect2.centerx, self.rect2.centery))]
        






