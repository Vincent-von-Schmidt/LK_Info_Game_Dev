import pygame


class Room:
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        self.surface: pygame.surface.Surface = pygame.surface.Surface( (240, 176) ) # 14 * 10
        self.surface.fill( (0, 0, 0) )

        # textures
        # self.textures: dict = {
        #     "wall_north" : pygame.image.load("./assets/wall_north.png"),
        #     "wall_east" : pygame.image.load("./assets/wall_east.png"),
        #     "wall_south" : pygame.imgae.load("./assets/wall_south.png"),
        #     "wall_west" : pygame.image.load("./assets/wall_west.png"),
        #     "ground" : pygame.image.load("./assets/ground.png"),
        # }

        self.wall_north = 0
        self.wall_east = 1
        self.wall_south = 2
        self.wall_west = 3
        self.ground = 4

        self.tilemap: list = []
        
        for _ in range( 14 ): self.tilemap.append( self.wall_north )

        for _ in range( 8 ): 
            self.tilemap.append( self.wall_west )
            for _ in range( 8 ): self.tilemap.append( self.ground )
            self.tilemap.append( self.wall_east )

        for _ in range( 14 ): self.tilemap.append( self.wall_south )

        print( f"{self.tilemap = }" )

    def render( self ) -> None:
        ...

if __name__ == "__main__":
    test = Room()

