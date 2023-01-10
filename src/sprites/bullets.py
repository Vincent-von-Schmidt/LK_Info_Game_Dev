import pygame 


class Bullets:

    def __init__(self, pos_x, pos_y) -> None:
        
        super().__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (pos_y, pos_x))
        self.end = False

    def update(self): 
        self.rect.x += 5

    def kill(self): 
        if self.rect.x >= 200:
            self.end = True
    
    def render(self): 
        return [(self.image, (self.rect.centerx, self.rect.centery))]






