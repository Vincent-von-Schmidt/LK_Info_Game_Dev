import json
import pygame

import map.tiles as tiles


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
        self.tile_construct: list = []

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
                    case 0: tmp.append( tiles.Ground() )
                    case 1: tmp.append( tiles.Block() )
                    case _: raise FileExistsError( "File not in binary." )

        return output

    def load_height_map( self, heightmap: str ) -> None:
        """
        Creates a list with all Tiles in the right order to draw the map.
        The Rows represent the lists in the main list.
        """

        # save the new heightmap
        self.heightmap: str = heightmap
        
        tile_construct: list = []

        # first row ---------------------------------------------

        # append row list
        tile_construct.append( tmp := [] )

        # append edge
        tmp.append( tiles.Edge( "north_west" ) )

        # append first set of walls
        for _ in range( 6 ): tmp.append( tiles.Wall( "north" ) )

        # door state
        match self.door_north:
            case "open": tmp.append( tiles.Door( open = True, facing = "north", split = 1 ))
            case "closed": tmp.append( tiles.Door( open = False, facing = "north", split = 2 ))
            case _:

                # append 2 walls, to compensate the missing door (door -> 2 blocks)
                for _ in range( 2 ): tmp.append( tiles.Wall( "north" ))

        # append second set of walls
        for _ in range( 6 ): tmp.append( tiles.Wall( "north" ))

        # append the edge to complete the first row
        tmp.append( tiles.Edge( "north_east" ))

        # between -----------------------------------------------

        # map content of the hightmap to tiles.Tiles
        with open( heightmap, "r" ) as file:
            content: list = self.__map_tiles_to_binary( json.loads(file.read()) )

        tmp_i: int = 0
        for i in range( 3 ):
            tile_construct.append( tmp := [] )
            tmp.append( tiles.Wall( "west" ))
            for a in range( 14 ): tmp.append( content[tmp_i][a] )
            tmp.append( tiles.Wall( "east" ) )

            tmp_i += 1

        for i in range( 2 ):
            tile_construct.append( tmp := [] )

            match self.door_west:
                case "open": tmp.append( tiles.Door( open = True, facing = "west", split = i + 1 ))
                case "closed": tmp.append( tiles.Door( open = False, facing = "west", split = i + 1 ))
                case _: tmp.append( tiles.Wall( "west" ) )

            for a in range( 14 ): tmp.append( content[tmp_i][a] )

            match self.door_east:
                case "open": tmp.append( tiles.Door( open = True, facing = "east", split = i + 1 ))
                case "closed": tmp.append( tiles.Door( open = False, facing = "east", split = i + 1 ))
                case _: tmp.append( tiles.Wall( "east" ) )

            tmp_i += 1


        for i in range( 3 ):
            tile_construct.append( tmp := [] )
            tmp.append( tiles.Wall( "west" ) )
            for a in range( 14 ): tmp.append( content[tmp_i][a] )
            tmp.append( tiles.Wall( "east" ) )

            tmp_i += 1


        # last row ----------------------------------------------
        tile_construct.append( tmp := [] )
        tmp.append( tiles.Edge( "south_west" ) )

        for _ in range( 6 ): tmp.append( tiles.Wall( "south" ))

        # door state
        match self.door_south:
            case "open": tmp.append( tiles.Door( open = True, facing = "south" ))
            case "closed": tmp.append( tiles.Door( open = False, facing = "south" ))
            case _:
                for _ in range( 2 ): tmp.append( tiles.Wall( "south" ))

        for _ in range( 6 ): tmp.append( tiles.Wall( "south" ))

        tmp.append( tiles.Edge( "south_east" ))

        self.__render(tile_construct)

        # save tile_construct
        self.tile_construct: list = tile_construct

    def __render( self, construct: list ) -> None:
        """Render the map. -> Draws the tiles on the map surface."""

        # default height for the first row
        tmp_height: list = [0]

        # for each row
        for row in construct:

            # default width for the first column
            tmp_width: list = [0]

            # tile cache -> tmp_heigt save
            tmp_tile: tiles.Tile | None = None

            # for each column
            for tile in row:

                # calc cordinates
                x: int = sum( tmp_width )
                y: int = sum( tmp_height )

                # set cordinates of the entity
                tile.set_cordinates( x, y )
                
                # map draw
                self.surface.blit(
                    source = tile.surface,
                    dest = ( x, y ) 
                )

                # save current width for the next column
                tmp_width.append( tile.surface.get_width())

                # save the current tile
                tmp_tile: tiles.Tile | None = tile

            # save height of last tile for next row
            tmp_height.append( tmp_tile.surface.get_height())


    def get_map( self ) -> list:
        # offset: x = 0, y = 32
        return [(self.surface, (0, 32))]

    def get_tile_map( self ) -> list:
        return self.tile_construct
