import pygame


class Room:
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        self.surface: pygame.surface.Surface = pygame.suface.Surface( (240, 176) ) # 14 * 10
        self.surface.fill( (0, 0, 0) )

        # textures
        self.wall_north = pygame.image.load("./assets/wall_north.png")
        self.wall_east = pygame.image.load("./assets/wall_east.png")
        self.wall_south = pygame.imgae.load("./assets/wall_south.png")
        self.wall_west = pygame.image.load("./assets/wall_west.png")
        self.ground = pygame.image.load("./assets/ground.png")

        self.tilemap: list = []
        
        for _ in range( 14 ): self.tilemap.append( self.wall_north )

        for _ in range( 8 ): 
            self.tilemap.append( self.wall_west )
            for _ in range( 8 ): self.tilemap.append( self.ground )
            self.tilemap.append( self.wall_east )

        for _ in range( 14 ): self.tilemap.append( self.wall_south )

    def render( self ) -> None:
        ...
