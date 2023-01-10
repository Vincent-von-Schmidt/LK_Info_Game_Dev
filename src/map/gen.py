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

        self.textures: dict = {
            "wall_north" : pygame.surface.Surface( (16, 24) ),
            "wall_east" : pygame.surface.Surface( (24, 16) ),
            "wall_south" : pygame.surface.Surface( (16, 24) ),
            "wall_west" : pygame.surface.Surface( (24, 16) ),
            "ground" : pygame.surface.Surface( (16, 16) ),
        }

        self.tilemap: list = []
        
        self.tilemap.append( tmp := [] )
        for _ in range ( 14 ): tmp.append( self.textures["wall_north"] )

        for _ in range( 8 ): 
            self.tilemap.append( tmp := [] )
            tmp.append( self.textures["wall_west"] )
            for _ in range( 8 ): tmp.append( self.textures["ground"] )
            tmp.append( self.textures["wall_east"] )

        self.tilemap.append( tmp := [] )
        tmp.append( self.textures["wall_south"] )

        print( f"{self.tilemap = }" )

    def render( self ) -> pygame.surface.Surface:

        for row in range( len( self.tilemap ) ):
            for column in range( len( self.tilemap[row] ) ):
                self.surface.blit( self.tilemap, self.surface )

        return self.surface

if __name__ == "__main__":
    test = Room()

