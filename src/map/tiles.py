from dataclasses import dataclass
import json
import pygame


@dataclass
class Tile:
    def __init__(

        self, 
        texture: str,
        collision: bool = False,

    ) -> None:
        
        self.surface: pygame.surface.Surface = pygame.image.load( texture )
        self.collision: bool = collision


class TilesMap:
    def __init__( self, heightmap: str = "./assets/map/heightmaps/blank.json" ) -> None:
        self.surface: pygame.surface.Surface = pygame.surface.Surface( (240, 160) )

        self.tiles: dict = {
            "wall_north": Tile( texture = "./assets/map/wall_north.png", collision = True ),
            "wall_east": Tile( texture = "./assets/map/wall_east.png", collision = True ),
            "wall_south": Tile( texture = "./assets/map/wall_south.png", collision = True ),
            "wall_west": Tile( texture = "./assets/map/wall_west.png", collision = True ),
            "ground": Tile( texture = "./assets/map/ground.png" ),
            "edge": Tile( texture = "./assets/map/edge.png" ),
            "block": Tile( texture = "./assets/map/block.png", collision = True ),
        }

        self.load_height_map(heightmap)

    def __map_tiles_to_binary( self, content: list ) -> list:
        output: list = []

        for i in content:

            output.append( tmp := [] )

            for bin in i:
                
                match bin:
                    case 0: tmp.append( self.tiles["ground"] )
                    case 1: tmp.append( self.tiles["block"] )
                    case _: raise FileExistsError( "File not in binary." )

        return output

    def load_height_map( self, heightmap: str ) -> None:
        
        tile_construct: list = []

        # first row
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge"] )
        for _ in range( 13 ): tmp.append( self.tiles["wall_north"] )
        tmp.append( self.tiles["edge"] )

        # between
        with open( heightmap, "r" ) as file:
            # content: list = map( self.__map_tiles_to_binary, json.loads(file.read()) )
            content: list = self.__map_tiles_to_binary( json.loads(file.read()) )

        for i in range( 8 ):
            tile_construct.append( tmp := [] )
            tmp.append( self.tiles["wall_west"] )
            for a in range( 13 ): tmp.append( content[i][a] )
            tmp.append( self.tiles["wall_east"] )
        
        # last row
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge"] )
        for _ in range( 13 ): tmp.append( self.tiles["wall_south"] )
        tmp.append( self.tiles["edge"] )

        self.__render(tile_construct)

    def __render( self, constuct: list ) -> None:
        """Render the map. -> Draws the tiles on the map surface."""

        for row_index, row in enumerate( constuct ):
            for column_index, tile in enumerate( row ):
                self.surface.blit(
                    source = tile.surface,
                    dest = (
                        column_index * tile.surface.get_width(),
                        row_index * tile.surface.get_height() 
                    ) 
                )

    def get_map( self ) -> list:
        # offset: x = 0, y = 32
        return [(self.surface, (0, 32))]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode( (1280, 720) )

    map: TilesMap = TilesMap()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blits( map.get_map() )

        pygame.display.flip()
