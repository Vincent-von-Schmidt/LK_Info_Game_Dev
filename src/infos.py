import pygame

import core
import objects.archer
import objects.bullet

class Infos:

    def __init__(self) -> None:
        """Initialisation of info bar objects and variables."""

        ################################################################
        # 1. Set the start properties.                                 #
        ################################################################

        # Infos

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 10)
        self.font2 = pygame.font.SysFont('Arial', 20)

        self.fps = 0
        self.time = (0, 0)
        self.kills = 0
        self.level = 0
        self.live = 0
        self.hearts = []

        self.background = pygame.image.load("./assets/hotbar/hotbar_background.png")
        self.sword = pygame.image.load("./assets/hotbar/sword.png")
        self.bow = pygame.image.load("./assets/hotbar/bow.png")
        self.border = pygame.image.load("./assets/hotbar/border.png")
        self.heart_full = pygame.image.load("./assets/hotbar/heart_full.png")
        self.heart_half = pygame.image.load("./assets/hotbar/heart_half.png")
        self.heart_empty = pygame.image.load("./assets/hotbar/heart_empty.png")
        self.skull = pygame.image.load("./assets/hotbar/skull.png")
    
    def update_time(self, minute: int, second: int) -> None:
        """Set the time of the info bar."""

        ################################################################
        # 1. Set the time.                                             #
        ################################################################

        self.time = minute, second
    
    def update_fps(self, fps: float) -> None:
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
    
    def update_hearts(self, hearts: float) -> None:
        """Update the health count."""

        self.live = hearts
        self.hearts.clear()

        for i in range (3):
            
            if (hearts-1) >= 0:
                
                self.hearts.append((self.heart_full, (48 + (i)*16, 3)))
                hearts -= 1
            
            elif (hearts-1) == -0.5:
                
                self.hearts.append((self.heart_half, (48 + (i)*16, 3)))
                hearts -= 0.5
            
            else:
                self.hearts.append((self.heart_empty, (48 + (i)*16, 3)))
    
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

        levelsurface = self.font.render("LVL " + f"{self.level:.0f}", False, (255, 255, 255))

        killsurface = self.font.render(f"{self.kills:.0f}", False, (255, 255, 255))

        return [
            (self.background, (0, 0)),
            (timesurface, (10, 2)),
            (fpssurface, (230, 2)),
            (levelsurface, (10, 15)),
            (killsurface, (50, 17)),
            (self.skull, (72, 15)),
            self.hearts[0],
            self.hearts[1],
            self.hearts[2],
            (self.border, (109, 2)),
            (self.border, (138, 2)),
            (self.sword, (113, 7)),
            (self.bow, (143, 8))
        ]
    
    def kill_screen(self, killer):
        match type(killer):
            case objects.archer.Archer:
                killer = "Archer"
            case objects.bullet.Bullet:
                killer = "Bullet"
            case _:
                killer = "Unknown"
        screen = pygame.surface.Surface((160,120))
        screen.fill((0,0,0))
        screen.blit(self.font.render("You were killed by " + killer, False, (255, 255, 255)), (30, 60))
        screen.blit(self.font2.render("You Died", False, (255, 255, 255)), (30, 20))
        screen.blit(self.font.render("Press Enter to quit", False, (255, 255, 255)), (30, 80))
        return [(screen, (50, 50))]

