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

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.fac = kwargs["fac"]
        self.active = True
    
    def update_rect(self) -> None:
        
        self.rect.x, self.rect.y = self.x, self.y
        self.rect.w, self.rect.h = self.w, self.h
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        return [(self._render(), (self.x, self.y))]
