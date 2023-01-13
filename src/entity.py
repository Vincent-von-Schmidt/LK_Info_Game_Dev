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

        self.fac = kwargs["fac"]
        self.active = True
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)
    
    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        self.x, self.y, self.w, self.h = rect.x, rect.y, rect.w, rect.h
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        return [(self._render(), (self.x, self.y))]