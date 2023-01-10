import pygame


class Room:
    def __init__(
        self,
        entrance: list = [False, False, False, False],
    ) -> None:

        self.surface: pygame.surface.Surface = pygame.surface.Surface( (240, 176) ) # 14 * 10
        self.surface.fill( (0, 0, 0) )

        self.rendered_map = None

        # textures -> .png, ( x, y )
        self.textures: dict = {
            "wall_north" :  pygame.image.load("./assets/map/wall_north.png"),
            "wall_east" :  pygame.image.load("./assets/map/wall_east.png"),
            "wall_south" :  pygame.image.load("./assets/map/wall_south.png"),
            "wall_west" :  pygame.image.load("./assets/map/wall_west.png"),
            "ground" :  pygame.image.load("./assets/map/ground.png"),
        }

        self.tilemap: list = []
        
        self.tilemap.append( tmp := [] )
        for _ in range ( 15 ): tmp.append( self.textures["wall_north"] )

        for _ in range( 8 ): 
            self.tilemap.append( tmp := [] )
            tmp.append( self.textures["wall_west"] )
            for _ in range( 13 ): tmp.append( self.textures["ground"] )
            tmp.append( self.textures["wall_east"] )

        self.tilemap.append( tmp := [] )
        for _ in range( 15 ): tmp.append( self.textures["wall_south"] )

        print( f"{self.tilemap = }" )

        # render map
        self.__render()

    def __render( self ) -> None: # -> pygame.surface.Surface:

        for row_index, row in enumerate( self.tilemap ):
            for column_index, tile in enumerate( row ):
                self.surface.blit( tile, ( column_index * tile.get_width(), row_index * tile.get_height() ) )

        self.rendered_map = [(pygame.transform.scale(self.surface, (1280, 720)), (0, 65))] 

    def get_map( self ):
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
