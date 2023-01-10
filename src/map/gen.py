import pygame


class Room:
    """A class to generate the room."""
    
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        self.surface: pygame.surface.Surface = pygame.surface.Surface( (240, 160) ) # 14 * 10
        self.surface.fill( (0, 0, 0) )

        self.rendered_map = None

        # Textures

        self.textures: dict = {
            "wall_north" :  pygame.image.load("./assets/map/wall_north.png"),
            "wall_east" :  pygame.image.load("./assets/map/wall_east.png"),
            "wall_south" :  pygame.image.load("./assets/map/wall_south.png"),
            "wall_west" :  pygame.image.load("./assets/map/wall_west.png"),
            "ground" :  pygame.image.load("./assets/map/ground.png"),
            "edge": pygame.image.load("./assets/map/edge.png"),
            "dor": pygame.surface.Surface((16, 16)), # TODO -> tmp, extra object required
        }

        self.tilemap: list = []
        
        # First row

        self.tilemap.append( tmp := [] )
        tmp.append( self.textures["edge"] )
        for _ in range ( 13 ): tmp.append( self.textures["wall_north"] )
        tmp.append( self.textures["edge"] )

        # Between

        for _ in range( 8 ):

            self.tilemap.append( tmp := [] )
            tmp.append( self.textures["wall_west"] )
            for _ in range( 13 ): tmp.append( self.textures["ground"] )
            tmp.append( self.textures["wall_east"] )

        # Last row

        self.tilemap.append( tmp := [] )
        tmp.append( self.textures["edge"] )
        for _ in range( 13 ): tmp.append( self.textures["wall_south"] )
        tmp.append( self.textures["edge"] )

        print( f"{self.tilemap = }" )

        # Render map

        self.__render()

    def __render( self ) -> None: # -> pygame.surface.Surface:
        for row_index, row in enumerate( self.tilemap ):
            for column_index, tile in enumerate( row ):
                self.surface.blit( tile, ( column_index * tile.get_width(), row_index * tile.get_height() ) )

        self.rendered_map = [(self.surface, (0, 32))] 

    def get_map( self ) -> None:
        """Get the generated map."""

        return self.rendered_map

if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode( (1280, 720) )

    map = Room()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blits( map.get_map() )

        pygame.display.flip()
