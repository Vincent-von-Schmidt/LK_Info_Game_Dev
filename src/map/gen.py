import pygame


class Room:
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        self.surface: pygame.surface.Surface = pygame.surface.Surface( (240, 176) ) # 14 * 10
        self.surface.fill( (0, 0, 0) )

        # textures -> .png, ( x, y )
        self.textures: dict = {
            "wall_north" : ( pygame.image.load("./assets/wall_north.png"), (16, 24) ),
            "wall_east" : ( pygame.image.load("./assets/wall_east.png"), (24, 16) ),
            "wall_south" : ( pygame.image.load("./assets/wall_south.png"), (16, 24) ),
            "wall_west" : ( pygame.image.load("./assets/wall_west.png"), (24, 26) ),
            "ground" : ( pygame.image.load("./assets/ground.png"), (16, 16) ),
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

        for row_index, row in enumerate( self.tilemap ):
            for column_index, column in enumerate( row ):
                self.surface.blit( column[0], ( column_index * column[1][0], row_index * column[1][1] ) )

        return self.surface

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode( (240, 176) )

    map = Room()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blit( map.render(), (0, 0) )

        pygame.display.flip()
