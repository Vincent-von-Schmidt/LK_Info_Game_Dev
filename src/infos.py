import pygame

import core

class Infos:

    def __init__(self) -> None:
        """Initialisation of info bar objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Infos

        pygame.font.init()
        # self.font = font = pygame.font.SysFont('Comic Sans MS', 10)
        self.font = pygame.font.SysFont('Arial', 10)

        self.fps = 0
        self.time = (0, 0)
        self.kills = 15
        self.level = 3
        self.live = 1.5
        self.hearts = []

        self.background = pygame.image.load("./assets/hotbar/hotbar_background.png")
        self.sword = pygame.image.load("./assets/hotbar/sword.png")
        self.bow = pygame.image.load("./assets/hotbar/bow.png")
        self.border = pygame.image.load("./assets/hotbar/border.png")
        self.heart_full = pygame.image.load("./assets/hotbar/heart_full.png")
        self.heart_half = pygame.image.load("./assets/hotbar/heart_half.png")
        self.heart_empty = pygame.image.load("./assets/hotbar/heart_empty.png")
        self.skull = pygame.image.load("./assets/hotbar/skull.png")
    
    def set_time(self, minute: int, second: int) -> None:
        """Set the time of the info bar."""

        ################################################################
        # 1. Set the time.                                             #
        ################################################################

        self.time = minute, second
    
    def set_fps(self, fps: float) -> None:
        """Set the fps of the info bar."""

        ################################################################
        # 1. Set the fps.                                              #
        ################################################################

        self.fps = fps

    def update_kills(self, kills: int) -> None:
        """Update the kill count."""

        self.kills += kills
    
    def set_level(self, level: int) -> None:
        """Set the level count."""

        self.level = level
    
    def update_hearts(self, hearts: int) -> None:
        """Update the health count."""

        live = self.live
        
        for i in range (3):
            
            if (live - (2-i)) == 1:
                self.hearts.append((self.heart_full, (48 + (2 - i)*16, 3)))
            
            elif (live - (2-i)) == 0.5:
                self.hearts.append((self.heart_half, (48 + (2 - i)*16, 3)))
            
            else:
                self.hearts.append((self.heart_empty, (48 + (2 - i)*16, 3)))
            
            live -= 1
    
    def render(self) -> list[tuple[pygame.surface.Surface, tuple[float]]]:
        """Render the info graphic."""

        ################################################################
        # 1. Create the surfaces.                                      #
        ################################################################

        timesurface = self.font.render(
            f"{self.time[0]}:{self.time[1]:02d}", False, (255, 255, 255)
        )

        fpssurface = self.font.render(
            f"{self.fps:.0f} FPS", False, (255, 255, 255)
        )

        levelsurface = self.font.render(f"{self.level:.0f} LVL", False, (255, 255, 255))

        killsurface = self.font.render(f"{self.kills:.0f}", False, (255, 255, 255))

        return [
            (self.background, (0, 0)),
            (timesurface, (10, 2)),
            (fpssurface, (200, 2)),
            (levelsurface, (10, 15)),
            (killsurface, (50, 15)),
            (self.skull, (72, 15)),
            self.hearts[0],
            self.hearts[1],
            self.hearts[2],
            (self.border, (96, 2)),
            (self.border, (125, 2)),
            (self.sword, (100, 7)),
            (self.bow, (130, 8))
        ]
