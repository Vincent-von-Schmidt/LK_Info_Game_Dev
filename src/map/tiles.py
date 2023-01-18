from dataclasses import dataclass
import pygame

import core
import entity


@dataclass
class Tile( entity.Entity ):
    def __init__(

        self, 
        texture: str,
        type: str,

    ) -> None:

        self.set_texture( path = texture )
        self.type: str = type

        self.x = 0
        self.y = 0
        self.w = self.surface.get_width()
        self.h = self.surface.get_height()

        self.set_entitiy( self.x, self.y, self.w, self.h )

    def set_entitiy(

        self,
        x: float = 0.0,
        y: float = 0.0,
        w: float = 0.0,
        h: float = 0.0

    ) -> None:

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        super().__init__(
            x = x,
            y = y,
            w = w,
            h = h,
            fac = self.type
        )

        self.init_rect()

    def set_cordinates( self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.set_entitiy( x, y, self.w, self.h )

    def set_texture( self, path: str ) -> None:
        self.texture: str = path
        self.surface: pygame.surface.Surface = pygame.image.load( self.texture )


class Wall( Tile ):
    def __init__( self, facing: str ) -> None:

        super().__init__(
            texture = f"./assets/map/wall/{facing}.png",
            type = core.MAP,
        )

        # special hitbox for the north facing wall
        if facing == "north":
            self.set_entitiy(
                w = self.surface.get_width(),
                h = self.surface.get_height() - 12
            )


class Edge( Tile ):
    def __init__( self, facing: str ) -> None:

        super().__init__(
            texture = f"./assets/map/edge/{facing}.png",
            type = core.MAP,
        )


class Ground( Tile ):
    def __init__( self ) -> None:

        super().__init__(
            texture = "./assets/map/ground.png",
            type = core.NEUTRAL,
        )


class Block( Tile ):
    def __init__( self ) -> None:

        super().__init__(
            texture = "./assets/map/block.png",
            type = core.MAP,
        )


class Door( Tile ):
    def __init__( 

        self,
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

        super().__init__( texture, type = core.SPECIAL )

    def get_state( self ) -> str:
        return self.state

    def set_state( self, open: bool ) -> None:

        self.state: str = "open" if open else "closed"
        self.__set_tile()

