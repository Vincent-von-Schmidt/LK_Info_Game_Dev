import pygame

import core

class Archer:
    """Enemy archer spirit class."""

    def __init__(self, **kwargs) -> None:

        self.dir = kwargs["dir"]

        self.step_max = 3 - 1 # Num
        self.step_last = 0 # Time
        self.step_idx = 0 # Index
        self.step_stop = True # Bool

        self.step_speed = kwargs["speed"] # pix / s
        self.step_change = kwargs["change"] # s

        self.images_up = (
            pygame.image.load("./assets/archer/archer_up_0.png"),
            pygame.image.load("./assets/archer/archer_up_1.png"),
            pygame.image.load("./assets/archer/archer_up_2.png")
        )
        self.images_down = (
            pygame.image.load("./assets/archer/archer_down_0.png"),
            pygame.image.load("./assets/archer/archer_down_1.png"),
            pygame.image.load("./assets/archer/archer_down_2.png")
        )
        self.images_left = (
            pygame.image.load("./assets/archer/archer_left_0.png"),
            pygame.image.load("./assets/archer/archer_left_1.png"),
            pygame.image.load("./assets/archer/archer_left_2.png")
        )
        self.images_right = (
            pygame.image.load("./assets/archer/archer_right_0.png"),
            pygame.image.load("./assets/archer/archer_right_1.png"),
            pygame.image.load("./assets/archer/archer_right_2.png")
        )
        ...
    
    def revert(self, rect):
        pass
    
    def update_sprite(self, elapsed_time: float) -> None:
        """Update the archer animation."""

        if not self.step_stop:
            self.step_last += elapsed_time

        while self.step_last >= self.step_change:

            self.step_idx += 1
            self.step_last -= self.step_change
        
        if self.step_idx > self.step_max:
            self.step_idx = 0 # 1
        
        if self.step_stop:
            self.step_idx = 0
        
        self.step_stop = True
        ...

    def _render(self) -> pygame.surface.Surface:
        if self.dir == core.RIGHT:
            return self.images_right[self.step_idx]
        
        elif self.dir == core.LEFT:
            return self.images_left[self.step_idx]
        
        elif self.dir == core.UP:
            print("oben!!!!")
            return self.images_up[self.step_idx]
        
        elif self.dir == core.DOWN:
            return self.images_down[self.step_idx]
        #return pygame.surface.Surface()