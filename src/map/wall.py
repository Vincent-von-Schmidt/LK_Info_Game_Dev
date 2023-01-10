import pygame


class Wall:
    """A class to generate walls of a room."""

    def __init__( self ) -> None:
        self.surface = pygame.surface.Surface( (24, 16) )
