from dataclasses import dataclass
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
    def __init__( self, heightmap: str ) -> None:
        self.surface: pygame.surface.Surface = pygame.surface.Surface( (16, 16) )

        self.tiles: dict = {
            "wall_north": Tile( texture = "./assets/map/wall_north.png", collision = True ),
            "wall_east": Tile( texture = "./assets/map/wall_east.png", collision = True ),
            "wall_south": Tile( texture = "./assets/map/wall_south.png", collision = True ),
            "wall_west": Tile( texture = "./assets/map/wall_west.png", collision = True ),
            "ground": Tile( texture = "./assets/map/ground.png" ),
            "edge": Tile( texture = "./assets/map/edge.png" ),
            "block": Tile( texture = "./assets/map/block.png", collision = True ),
        }

        self.tile_construct: list = self.load_height_map(heightmap)

    def load_height_map( self, heightmap: str ) -> list:
        
        tile_construct: list = []

        # first row
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge"] )
        for _ in range( 13 ): tmp.append( self.tiles["wall_north"] )
        tmp.append( self.tiles["edge"] )

        # between
        with open( heightmap, "r" ) as file:
            print(file.read())
        
        # last row
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge"] )
        for _ in range( 13 ): tmp.append( self.tiles["wall_south"] )
        tmp.append( self.tiles["edge"] )

        return tile_construct

    def __render( self ) -> None:
        """Render the map. -> Draws the tiles on the map surface."""

        for row_index, row in enumerate( self.tile_construct ):
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

    def get_map( self ) -> pygame.surface.Surface:
        return self.surface


if __name__ == "__main__":
    ...
    # map: TilesMap = TilesMap()
    # map.load_height_map("./assets/map/heightmaps/blank.pbm")
