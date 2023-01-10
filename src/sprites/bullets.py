import pygame 

pygame.init()


class bullets(pygame.sprite.Sprite): 
    def __init__(self, pos_x, pos_y) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 0, 0))
        self.rect = pygame.imgage.get_rect(center = (pos_y, pos_x))

    def b_update(self): 
        self.rect += 5

        if self.rect.x >= 200:
            self.kill()






