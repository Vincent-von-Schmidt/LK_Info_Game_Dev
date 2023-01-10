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

        print( f"{self.surface.get_height() = }" )


class TilesMap:
    def __init__( self ) -> None:
        ...

    def load_height_map( self, heightmap_file: str ) -> None:
        ...
