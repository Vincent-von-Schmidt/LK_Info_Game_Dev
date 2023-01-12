import pygame

import core


class Entity:

    max_id = 0

    def __init__(self, **kwargs) -> None:
        
        Entity.max_id += 1
        self.id = Entity.max_id -1

        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.w = 0
        self.h = 0

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.fac = kwargs["fac"]

        self.active = True
    
    def init_rect(self) -> None:
        
        self.rect[0] = self.x
        self.rect[1] = self.y
        self.rect[2] = self.w
        self.rect[3] = self.h
    
    def update_rect(self) -> None:

        self.rect[0] = self.x
        self.rect[1] = self.y
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        return [(self._render(), (self.x, self.y))]