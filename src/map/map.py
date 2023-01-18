import json

import map.tiles as tiles 
import map.t_map as tilesMap


class Map:
    def __init__( self, path: str = "./assets/map/heightmaps/test_map.json" ) -> None:

        with open( path, "r" ) as file:
            content: dict = json.loads( file.read() )

        map: tilesMap.TilesMap = tilesMap.TilesMap(
            door_north = content["door_north"],
            door_east = content["door_east"],
            door_south = content["door_south"],
            door_west = content["doow_west"],
        )

        self.__map_tiles_to_binary( content["heightmap"] )

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


if __name__ == "__main__":
    import pygame

    pygame.init()
    screen = pygame.display.set_mode( (816, 624) )

    map: Map = Map( path = "./assets/map/heightmaps/test_map.json" )

    tmp_surf = pygame.surface.Surface( (272, 208) )
    tmp_surf.fill( (0, 0, 0) )
    tmp_surf.blits( map.get_map() )

    scale_surf = pygame.transform.scale( tmp_surf, (816, 624) )

    screen.blit( scale_surf, (0, 0) )

    while True:
        pygame.display.flip()
    
