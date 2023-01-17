from dataclasses import dataclass
import pygame

import core
import entity


@dataclass
class Tile( entity.Entity ):
    def __init__(

        self, 
        texture: str,
        collision: bool = False,

    ) -> None:

        self.set_texture( path = texture )
        self.collision: bool = collision

        # type definition
        if "wall" in self.texture: self.type: str = core.MAP
        elif "door" in self.texture: self.type: str = core.SPECIAL
        elif "ground" in self.texture: self.type: str = core.NEUTRAL
        elif "block" in self.texture: self.type: str = core.MAP
        elif "edge" in self.texture: self.type: str = core.MAP

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        self.set_entitiy()

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

