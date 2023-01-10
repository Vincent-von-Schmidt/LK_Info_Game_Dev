import pygame 
import sprites.player as player
import core 


class Bullets:

    def __init__(self, pos_x, pos_y, dir) -> None:
        
        super().__init__()

        #horizontal bullets
        #self.image_right = pygame.Surface((50, 10))
        #self.image_right.fill((255, 0, 0))
        self.image_right = pygame.image.load("./assets/arrow_right.png")
        self.rect_right = self.image_right.get_rect(center = (pos_x, pos_y))

        #self.image_left = pygame.Surface((50, 10))
        #self.image_left.fill((255, 0, 0))
        self.image_left = pygame.image.load("./assets/arrow_left.png")
        self.rect_left = self.image_left.get_rect(center = (pos_x, pos_y))

        #vertical bullets
        #self.image_up = pygame.Surface((10, 50))
        #self.image_up.fill((0, 255, 0))
        self.image_up = pygame.image.load("./assets/arrow_up.png")
        self.rect_up = self.image_up.get_rect(center =(pos_x, pos_y))

        #self.image_down = pygame.Surface((10, 50))
        #self.image_down.fill((0, 255, 0))
        self.image_down = pygame.image.load("./assets/arrow_down.png")
        self.rect_down = self.image_down.get_rect(center =(pos_x, pos_y))

        self.end = False
        self.vel = 1000
        self.dir = dir

    def update(self, elapsed_time):

        v = elapsed_time * self.vel
        
        if self.dir == core.RIGHT:
            self.rect_right.x += v
        
        elif self.dir == core.LEFT:
            self.rect_left.x -= 5 
        
        elif self.dir == core.UP:
            self.rect_up.y -= 5 

        elif self.dir == core.DOWN:
            self.rect_down.y += 5 

    def kill(self): 
        if self.rect_right.x >= 200:
            self.end = True
        
        elif self.rect_left.x <= 0: 
            self.end = True 
        
        elif self.rect_up.y <= 0:
            self.end = True 
        
        elif self.rect_down.y >= 500: 
            self.end = True 
    
    def render(self): 
        if self.dir == core.RIGHT:
            return [(self.image_right, (self.rect_right.centerx, self.rect_right.centery))] 
        elif self.dir == core.LEFT: 
            return [(self.image_left, (self.rect_left.centerx, self.rect_left.centery))]
        elif self.dir == core.UP: 
            return [(self.image_up, (self.rect_up.centerx, self.rect_up.centery))]
        elif self.dir == core.DOWN: 
            return [(self.image_down, (self.rect_down.centerx, self.rect_down.centery))]
        






