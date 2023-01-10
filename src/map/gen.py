import pygame


class Room:
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        # texture
        self.ground = pygame.image.load("./assets/ground.png")
        self.wall_north = pygame.image.load("./assets/wall_north.png")
        self.wall_east = pygame.image.load("./assets/wall_east.png")
        self.wall_south = pygame.image.load("./assets/wall_south.png")
        self.wall_west = pygame.image.load("./assets/wall_west.png")

        self.surface: pygame.surface.Surface = pygame.suface.Surface( (240, 176) )

    def render( self ) -> None:
        ...
