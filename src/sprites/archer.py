import pygame

import core

class Archer:
    """Enemy archer spirit class."""

    def __init__(self, **kwargs) -> None:
        ...
    
    def revert(self, rect):
        pass
    
    def update_sprite(self, elapsed_time: float) -> None:
        """Update the archer animation."""
        ...

    def _render(self) -> pygame.surface.Surface:
        return pygame.surface.Surface()