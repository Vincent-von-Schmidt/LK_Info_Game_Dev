import pygame

import core


class Entity:

    max_id = 0

    def __init__(self, **kwargs) -> None:
        
        Entity.max_id += 1
        self.id = Entity.max_id -1

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.w = kwargs.get("w", 0)
        self.h = kwargs.get("h", 0)

        self.rect = pygame.Rect(0, 0, 0, 0)

        self.fac = kwargs["fac"]
        self.active = True
    
    def init_rect(self):
        self.rect.x, self.rect.y, self.rect.w, self.rect.h = self.x, self.y, self.w, self.h
    
    def update_rect(self):
        self.rect.x, self.rect.y = self.x, self.y
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float, float]]]:
        return [(self._render(), (self.x, self.y))]
    