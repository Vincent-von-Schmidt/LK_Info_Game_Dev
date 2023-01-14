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
        
        self.set_texture( path = texture )
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
            facing: str = "north",
            split: int = 1

    ) -> None:

        self.facing: str = facing
        self.split: int = split
        self.set_state( open )

    def __set_tile( self ) -> None:

        if self.facing == "west" or self.facing == "east":
            texture: str = f"./assets/map/door/{self.state}/{self.facing}_{self.split}.png"

        else: 
            texture: str = f"./assets/map/door/{self.state}/{self.facing}.png"

        super().__init__( texture )

    def get_state( self ) -> str:
        return self.state

    def set_state( self, open: bool ) -> None:

        self.state: str = "open" if open else "closed"
        self.__set_tile()


class TilesMap:
    def __init__( 

        self,
        heightmap: str = "./assets/map/heightmaps/blank.json",
        door_north: bool | str = False,
        door_east: bool | str = False,
        door_south: bool | str = False,
        door_west: bool | str = False,

    ) -> None:

        # -> main - radio : 256, 208
        self.surface: pygame.surface.Surface = pygame.surface.Surface( (272, 176) )
        self.heightmap: str = heightmap
        self.entity_list: list = []
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
            "door_closed_north": Door( open = False, facing = "north" ),
            "door_closed_east_1": Door( open = False, facing = "east", split = 1 ),
            "door_closed_east_2": Door( open = False, facing = "east", split = 2 ),
            "door_closed_south": Door( open = False, facing = "south" ),
            "door_closed_west_1": Door( open = False, facing = "west", split = 1 ),
            "door_closed_west_2": Door( open = False, facing = "west", split = 2 ),
            "door_open_north": Door( open = True, facing = "north" ),
            "door_open_east_1": Door( open = True, facing = "east", split = 1 ),
            "door_open_east_2": Door( open = True, facing = "east", split = 2 ),
            "door_open_south": Door( open = True, facing = "south" ),
            "door_open_west_1": Door( open = True, facing = "west", split = 1 ),
            "door_open_west_2": Door( open = True, facing = "west", split = 2 ),
        }

        self.door_north: bool | str = door_north
        self.door_east: bool | str = door_east
        self.door_south: bool | str = door_south
        self.door_west: bool | str = door_west

        self.load_height_map( self.heightmap )

    def set_door_state( 

        self,
        north: str = "open",
        east: str = "open",
        south: str = "open",
        west: str = "open"

    ) -> None:

        if self.door_north: self.door_north = north
        if self.door_east: self.door_east = east
        if self.door_south: self.door_south = south
        if self.door_west: self.door_west = west

        self.load_height_map( self.heightmap )

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

        # save the new heightmap
        self.heightmap: str = heightmap
        
        tile_construct: list = []

        # first row ---------------------------------------------
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge_north_west"] )

        if not self.door_north:
            for _ in range( 14 ): tmp.append( self.tiles["wall_north"] )
        else: 
            for _ in range( 6 ): tmp.append( self.tiles["wall_north"] )

            # door state
            match self.door_north:
                case "open": tmp.append( self.tiles["door_open_north"] )
                case "closed": tmp.append( self.tiles["door_closed_north"] )

            for _ in range( 6 ): tmp.append( self.tiles["wall_north"] )

        tmp.append( self.tiles["edge_north_east"] )

        # between -----------------------------------------------

        # map content of the hightmap to Tiles
        with open( heightmap, "r" ) as file:
            content: list = self.__map_tiles_to_binary( json.loads(file.read()) )

        # append Tiles to list
        if not self.door_east or not self.door_west:
            for i in range( 8 ):
                tile_construct.append( tmp := [] )
                tmp.append( self.tiles["wall_west"] )
                for a in range( 14 ): tmp.append( content[i][a] )
                tmp.append( self.tiles["wall_east"] )

        else:
            tmp_i: int = 0
            for i in range( 3 ):
                tile_construct.append( tmp := [] )
                tmp.append( self.tiles["wall_west"] )
                for a in range( 14 ): tmp.append( content[tmp_i][a] )
                tmp.append( self.tiles["wall_east"] )

                tmp_i += 1

            for i in range( 2 ):
                tile_construct.append( tmp := [] )

                match self.door_west:
                    case "open": tmp.append( self.tiles[f"door_open_west_{i + 1}"] )
                    case "closed": tmp.append( self.tiles[f"door_closed_west_{i + 1}"] )

                for a in range( 14 ): tmp.append( content[tmp_i][a] )

                match self.door_east:
                    case "open": tmp.append( self.tiles[f"door_open_east_{i + 1}"] )
                    case "closed": tmp.append( self.tiles[f"door_closed_east_{i + 1}"] )

                tmp_i += 1


            for i in range( 3 ):
                tile_construct.append( tmp := [] )
                tmp.append( self.tiles["wall_west"] )
                for a in range( 14 ): tmp.append( content[tmp_i][a] )
                tmp.append( self.tiles["wall_east"] )

                tmp_i += 1


        # last row ----------------------------------------------
        tile_construct.append( tmp := [] )
        tmp.append( self.tiles["edge_south_west"] )

        if not self.door_south:
            for _ in range( 14 ): tmp.append( self.tiles["wall_south"] )
        else: 
            for _ in range( 6 ): tmp.append( self.tiles["wall_south"] )

            # door state
            match self.door_south:
                case "open": tmp.append( self.tiles["door_open_south"] )
                case "closed": tmp.append( self.tiles["door_closed_south"] )

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
                
                # map draw
                self.surface.blit(
                    source = tile.surface,
                    dest = (
                        sum( tmp_width ),
                        sum( tmp_height )
                    ) 
                )

                # entity list -> collision
                match tile.type:
                    case core.WALL: fac = core.MAP
                    case core.DOOR: fac = core.SPECIAL
                    case core.GROUND: fac = core.NEUTRAL
                    case _:
                        print(tile)
                        raise TypeError("Tile not defined by CORE")
                
                if "north" in tile.texture and not "edge" in tile.texture:
                    h_dif = 12
                else: 
                    h_dif = 0
                self.entity_list.append(
                    entity.Entity(
                        x = sum( tmp_width ),
                        y = sum( tmp_height ) + 32,
                        fac = fac
                    )
                )
                self.entity_list[-1].w = tile.surface.get_width()
                self.entity_list[-1].h = tile.surface.get_height() - h_dif

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

    def get_entity_list( self ) -> list:
        return self.entity_list


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode( (1280, 720) )

    map: TilesMap = TilesMap( door_north=True, door_south=True )
    map.set_door_state()

    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT: pygame.quit()

        screen.blits( map.get_map() )

        pygame.display.flip()
