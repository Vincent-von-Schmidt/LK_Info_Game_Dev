import pygame

import map.tiles as tiles


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
            "wall_north": tiles.Tile( texture = "./assets/map/wall_north.png", collision = True ),
            "wall_east": tiles.Tile( texture = "./assets/map/wall_east.png", collision = True ),
            "wall_south": tiles.Tile( texture = "./assets/map/wall_south.png", collision = True ),
            "wall_west": tiles.Tile( texture = "./assets/map/wall_west.png", collision = True ),
            "ground": tiles.Tile( texture = "./assets/map/ground.png" ),
            "edge": tiles.Tile( texture = "./assets/map/edge.png" ),
            "block": tiles.Tile( texture = "./assets/map/block.png", collision = True ),
        }

        self.tilemap: list = []
        
        # First row
        self.tilemap.append( tmp := [] )
        tmp.append( self.textures["edge"].surface )
        for _ in range ( 13 ): tmp.append( self.textures["wall_north"].surface )
        tmp.append( self.textures["edge"].surface )

        # Between
        for _ in range( 8 ):
            self.tilemap.append( tmp := [] )
            tmp.append( self.textures["wall_west"].surface )
            for _ in range( 13 ): tmp.append( self.textures["ground"].surface )
            tmp.append( self.textures["wall_east"].surface )

        # Last row
        self.tilemap.append( tmp := [] )
        tmp.append( self.textures["edge"].surface )
        for _ in range( 13 ): tmp.append( self.textures["wall_south"].surface )
        tmp.append( self.textures["edge"].surface )

        # TODO -> remove debug
        # print( f"{self.tilemap = }" )

        # Render map

        self.__render()

    def __render( self ) -> None: # -> pygame.surface.Surface:
        """Render the map. -> Draws the tiles on the map surface."""

        for row_index, row in enumerate( self.tilemap ):
            for column_index, tile in enumerate( row ):
                self.surface.blit(
                    source = tile,
                    dest = (
                        column_index * tile.get_width(),
                        row_index * tile.get_height() 
                    ) 
                )

        # save rendered map, set draw offset -> x = 0, y = 32
        self.rendered_map = [(self.surface, (0, 32))] 

    def get_map( self ) -> list[tuple[pygame.surface.Surface, tuple[int, ...]]] | None:
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
