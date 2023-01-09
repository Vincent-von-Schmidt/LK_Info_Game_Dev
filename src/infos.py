import pygame

import core

class Infos:

    def __init__(self):
        """Initialisation of info bar objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Infos

        pygame.font.init()
        self.font = font = pygame.font.SysFont('Comic Sans MS', 30)

        self.fps = 0
        self.time = (0, 0)
    
    def set_time(self, minute, second):
        """Set the time of the info bar."""

        ################################################################
        # 1. Set the time.                                             #
        ################################################################

        self.time = minute, second
    
    def set_fps(self, fps):
        """Set the fps of the info bar."""

        ################################################################
        # 1. Set the fps.                                              #
        ################################################################

        self.fps = fps
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the info graphic."""

        ################################################################
        # 1. Create the surfaces.                                      #
        ################################################################

        boxsurface = pygame.Surface((640, 50))
        boxsurface.fill((0, 0, 0))

        timesurface = self.font.render(
            f"{self.time[0]}:{self.time[1]:02d}", False, (255, 255, 255)
        )

        fpssurface = self.font.render(
            f"{self.fps:.0f} FPS", False, (255, 255, 255)
        )

        return [
            (boxsurface, (0, 0)),
            (timesurface, (25, 3)),
            (fpssurface, (520, 3))
        ]
