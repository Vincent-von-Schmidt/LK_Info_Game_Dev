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
    def __init__( 

        self,
        heightmap: str = "./assets/map/heightmaps/blank.json",
        door_north: bool = False,
        door_east: bool = False,
        door_south: bool = False,
        door_west: bool = False,

    ) -> None:

        # -> main - radio : 256, 208
        self.surface: pygame.surface.Surface = pygame.surface.Surface( (256, 176) )

        self.tiles: dict = {
            "wall_north": Tile( texture = "./assets/map/wall_north.png", collision = True ),
            "wall_east": Tile( texture = "./assets/map/wall_east.png", collision = True ),
            "wall_south": Tile( texture = "./assets/map/wall_south.png", collision = True ),
            "wall_west": Tile( texture = "./assets/map/wall_west.png", collision = True ),
            "ground": Tile( texture = "./assets/map/ground.png" ),
            "edge_north_east": Tile( texture = "./assets/map/edge_north_east.png" ),
            "edge_north_west": Tile( texture = "./assets/map/edge_north_west.png" ),
            "edge_south_west": Tile( texture = "./assets/map/edge_south_west.png" ),
            "edge_south_east": Tile( texture = "./assets/map/edge_south_east.png" ),
            "block": Tile( texture = "./assets/map/block.png", collision = True ),
            # "door_north": Tile( texture = "./assets/map/door_north.png" ),
            # "door_south": Tile( texture = "./assets/map/door_south.png" ),
            "door_closed_north": Tile( texture = "./assets/map/door_north_closed.png" ),
            "door_closed_east": Tile( texture = "./assets/map/door_east_closed.png" ),
            "door_closed_south": Tile( texture = "./assets/map/door_south_closed.png" ),
            "door_closed_west": Tile( texture = "./assets/map/door_west_closed.png" ),
            "door_open_north": Tile( texture = "./assets/map/door_north_open.png" ),
            "door_open_east": Tile( texture = "./assets/map/door_east_open.png" ),
            "door_open_south": Tile( texture = "./assets/map/door_south_open.png" ),
            "door_open_west": Tile( texture = "./assets/map/door_west_open.png" ),
        }

        self.door_north: bool = door_north
        self.door_east: bool = door_east
        self.door_south: bool = door_south
        self.door_west: bool = door_west

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
        tmp.append( self.tiles["edge_north_west"] )

        if not self.door_north:
            for _ in range( 13 ): tmp.append( self.tiles["wall_north"] )
        else: 
            for _ in range( 5 ): tmp.append( self.tiles["wall_north"] )
            tmp.append( self.tiles["door_open_north"] )
            for _ in range( 5 ): tmp.append( self.tiles["wall_north"] )

        tmp.append( self.tiles["edge_north_east"] )

        # between
        with open( heightmap, "r" ) as file:
            content: list = self.__map_tiles_to_binary( json.loads(file.read()) )

        for i in range( 8 ):
            tile_construct.append( tmp := [] )
            tmp.append( self.tiles["wall_west"] )
            for a in range( 13 ): tmp.append( content[i][a] )
            tmp.append( self.tiles["wall_east"] )
        
        # last row
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge_south_west"] )

        if not self.door_south:
            for _ in range( 13 ): tmp.append( self.tiles["wall_south"] )
        else: 
            for _ in range( 5 ): tmp.append( self.tiles["wall_south"] )
            tmp.append( self.tiles["door_open_south"] )
            for _ in range( 5 ): tmp.append( self.tiles["wall_south"] )

        tmp.append( self.tiles["edge_south_east"] )

        self.__render(tile_construct)

    def __render( self, constuct: list ) -> None:
        """Render the map. -> Draws the tiles on the map surface."""

        tmp_height: int = 0

        for row_index, row in enumerate( constuct ):

            tmp_width: int = 0

            for column_index, tile in enumerate( row ):
                
                self.surface.blit(
                    source = tile.surface,
                    dest = (
                        column_index * tmp_width,
                        row_index * tmp_height 
                    ) 
                )

                tmp_height: int = tile.surface.get_height()
                tmp_width: int = tile.surface.get_width()

    def get_map( self ) -> list:
        # offset: x = 0, y = 32
        # return [(self.surface, (0, 32))]
        return [(pygame.transform.scale(self.surface, (1024, 832)), (0, 0))]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode( (1024, 832) )

    map: TilesMap = TilesMap( door_north=True )

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blits( map.get_map() )

        pygame.display.flip()
