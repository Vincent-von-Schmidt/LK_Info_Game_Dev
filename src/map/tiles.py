from dataclasses import dataclass
import json
import pygame

import entity
import core


@dataclass
class Tile:
    def __init__(

        self, 
        texture: str,
        collision: bool = False,

    ) -> None:
        
        self.texture: str = texture
        self.surface: pygame.surface.Surface = pygame.image.load( self.texture )
        self.collision: bool = collision

        # type definition
        if "wall" in self.texture: self.type: str = core.WALL
        elif "door" in self.texture: self.type: str = core.DOOR
        elif "ground" in self.texture: self.type: str = core.GROUND
        elif "block" in self.texture: self.type: str = core.WALL
        elif "edge" in self.texture: self.type: str = core.WALL

    def set_texture( self, path: str ) -> None:
        self.texture: str = path
        self.surface: pygame.surface.Surface = pygame.image.load( self.texture )


class Door(Tile):
    def __init__( self,

            open: bool = True,
            facing: str = "north"

    ) -> None:

        self.facing: str = facing
        self.set_state( open )


    def __set_tile( self ) -> None:
        super().__init__(
            texture = f"./assets/map/door/{self.state}/{self.facing}.png"
        )

    def get_state( self ) -> str:
        return self.state

    def set_state( self, open: bool ) -> None:

        self.state: str = "open" if open else "closed"
        self.__set_tile()


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
        self.surface: pygame.surface.Surface = pygame.surface.Surface( (272, 176) )

        self.tile_construct: list = []

        self.tiles: dict = {
            "wall_north": Tile( texture = "./assets/map/wall/north.png", collision = True ),
            "wall_east": Tile( texture = "./assets/map/wall/east.png", collision = True ),
            "wall_south": Tile( texture = "./assets/map/wall/south.png", collision = True ),
            "wall_west": Tile( texture = "./assets/map/wall/west.png", collision = True ),
            "ground": Tile( texture = "./assets/map/ground.png" ),
            "edge_north_east": Tile( texture = "./assets/map/edge/north_east.png" ),
            "edge_north_west": Tile( texture = "./assets/map/edge/north_west.png" ),
            "edge_south_west": Tile( texture = "./assets/map/edge/south_west.png" ),
            "edge_south_east": Tile( texture = "./assets/map/edge/south_east.png" ),
            "block": Tile( texture = "./assets/map/block.png", collision = True ),
            "door_closed_north": Tile( texture = "./assets/map/door/closed/north.png" ),
            "door_closed_east": Tile( texture = "./assets/map/door/closed/east.png" ),
            "door_closed_south": Tile( texture = "./assets/map/door/closed/south.png" ),
            "door_closed_west": Tile( texture = "./assets/map/door/closed/west.png" ),
            "door_open_north": Tile( texture = "./assets/map/door/open/north.png" ),
            "door_open_east": Tile( texture = "./assets/map/door/open/east.png" ),
            "door_open_south": Tile( texture = "./assets/map/door/open/south.png" ),
            "door_open_west": Tile( texture = "./assets/map/door/open/west.png" ),
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

        # first row ---------------------------------------------
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge_north_west"] )

        if not self.door_north:
            for _ in range( 14 ): tmp.append( self.tiles["wall_north"] )
        else: 
            for _ in range( 6 ): tmp.append( self.tiles["wall_north"] )
            tmp.append( self.tiles["door_open_north"] )
            for _ in range( 6 ): tmp.append( self.tiles["wall_north"] )

        tmp.append( self.tiles["edge_north_east"] )

        # between -----------------------------------------------

        # map content of the hightmap to Tiles
        with open( heightmap, "r" ) as file:
            content: list = self.__map_tiles_to_binary( json.loads(file.read()) )

        # append Tiles to list
        for i in range( 8 ):
            tile_construct.append( tmp := [] )
            tmp.append( self.tiles["wall_west"] )
            for a in range( 14 ): tmp.append( content[i][a] )
            tmp.append( self.tiles["wall_east"] )
        
        # last row ----------------------------------------------
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge_south_west"] )

        if not self.door_south:
            for _ in range( 14 ): tmp.append( self.tiles["wall_south"] )
        else: 
            for _ in range( 6 ): tmp.append( self.tiles["wall_south"] )
            tmp.append( self.tiles["door_closed_south"] )
            for _ in range( 6 ): tmp.append( self.tiles["wall_south"] )

        tmp.append( self.tiles["edge_south_east"] )

        self.__render(tile_construct)

        # save tile_construct
        self.tile_construct: list = tile_construct

    def __render( self, constuct: list ) -> None:
        """Render the map. -> Draws the tiles on the map surface."""

        # default height for the first row
        tmp_height: list = [0]

        # for each row
        for row in constuct:

            # default width for the first column
            tmp_width: list = [0]

            # tile cache -> tmp_heigt save
            tmp_tile: Tile | None = None

            # for each column
            for tile in row:
                
                self.surface.blit(
                    source = tile.surface,
                    dest = (
                        sum( tmp_width ),
                        sum( tmp_height )
                    ) 
                )

                # save current width for the next column
                tmp_width.append( tile.surface.get_width() )

                # save the current tile
                tmp_tile: Tile | None = tile

            # save height of last tile for next row
            tmp_height.append( tmp_tile.surface.get_height() )


    def get_map( self ) -> list:
        # offset: x = 0, y = 32
        return [(self.surface, (0, 32))]

    def get_tile_map( self ) -> list:
        return self.tile_construct

    def get_tile_entities( self ) -> list:

        entity_list = []

        tmp_height: list = [0]

        for row in self.tile_construct:

            tmp_width: list = [0]

            tmp_tile: Tile | None = None

            for tile in row:
                
                width = tile.surface.get_width()
                height = tile.surface.get_height()
                if tile.type == core.WALL: fac = core.MAP
                elif tile.type == core.DOOR: fac = core.SPECIAL
                elif tile.type == core.GROUND: fac = core.NEUTRAL
                else:
                    print(tile)
                    raise TypeError("Tile not defined by CORE")

                entity_list.append(
                    entity.Entity(
                        x = sum( tmp_width ),
                        y = sum( tmp_height ) + 32,
                        fac = fac
                    )
                )
                entity_list[-1].w = width
                entity_list[-1].h = height
                entity_list[-1].init_rect()

                tmp_width.append( tile.surface.get_width() )

                tmp_tile: Tile | None = tile

            tmp_height.append( tmp_tile.surface.get_height() )
        return entity_list

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode( (1280, 720) )

    map: TilesMap = TilesMap( door_north=True, door_south=True )

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blits( map.get_map() )

        pygame.display.flip()
