import pygame

import core

class Player:
    """Sprite class for player movement, etc."""

    def __init__(self, **kwargs) -> None:

        self.step_speed = kwargs["speed"] # pix / s
        self.step_change = kwargs["change"] # s
        self.dir = kwargs["dir"]

        self.images_up = (
            pygame.image.load("./assets/player/player_up_0.png"),
            pygame.image.load("./assets/player/player_up_1.png"),
            pygame.image.load("./assets/player/player_up_2.png")
        )
        self.images_down = (
            pygame.image.load("./assets/player/player_down_0.png"),
            pygame.image.load("./assets/player/player_down_1.png"),
            pygame.image.load("./assets/player/player_down_2.png")
        )
        self.images_left = (
            pygame.image.load("./assets/player/player_left_0.png"),
            pygame.image.load("./assets/player/player_left_1.png"),
            pygame.image.load("./assets/player/player_left_2.png")
        )
        self.images_right = (
            pygame.image.load("./assets/player/player_right_0.png"),
            pygame.image.load("./assets/player/player_right_1.png"),
            pygame.image.load("./assets/player/player_right_2.png")
        )

        self.step_max = 3 - 1 # Num
        self.step_last = 0 # Time
        self.step_idx = 0 # Index
        self.step_stop = True # Bool

    def move_up(self, elapsed_time: float = 0) -> float:
        """Move the sprite up."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.y -= dis

        self.dir = core.UP
        self.step_stop = False

        return dis
    
    def move_down(self, elapsed_time: float = 0) -> float:
        """Move the sprite down."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.y += dis
        
        self.dir = core.DOWN
        self.step_stop = False

        return dis
    
    def move_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite left."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.x -= dis

        self.dir = core.LEFT
        self.step_stop = False

        return dis
    
    def move_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite right."""

        ################################################################
        # 1. Change the player position.                               #
        ################################################################

        dis = self.step_speed * elapsed_time
        self.x += dis

        self.dir = core.RIGHT
        self.step_stop = False

        return dis
    
    def move_up_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite up right."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x += dis

        self.dir = core.RIGHT
        self.step_stop = False
        
        return 2*dis

    def move_up_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite up left."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y -= dis
        self.x -= dis

        self.dir = core.LEFT
        self.step_stop = False
        
        return 2*dis
    
    def move_down_left(self, elapsed_time: float = 0) -> float:
        """Move the sprite down left."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y += dis
        self.x -= dis
    
        self.dir = core.LEFT
        self.step_stop = False
        
        return 2*dis
    
    def move_down_right(self, elapsed_time: float = 0) -> float:
        """Move the sprite down right."""

        dis = self.step_speed * elapsed_time / 2**0.5

        self.y += dis
        self.x += dis

        self.dir = core.RIGHT
        self.step_stop = False
        
        return 2*dis
    
    def revert(self, rect):
        """Handles the collision"""
        
        f = 6
        tmp_up = [self.rect.x, self.rect.y, self.rect.w, 1]
        tmp_down = [self.rect.x, self.rect.y + self.rect.h, self.rect.w, -1]
        tmp_left = [self.rect.x, self.rect.y, 1, self.rect.h]
        tmp_right = [self.rect.x + self.rect.w, self.rect.y, -1, self.rect.h]
        tmp_rect = pygame.Rect(rect.x - self.rect.w/2 - f, rect.y - self.rect.h/2 - f, rect.w + self.rect.w + 2*f, rect.h + self.rect.h + 2*f)
        if tmp_rect.contains(tmp_up) and not tmp_rect.contains(tmp_left) and not tmp_rect.contains(tmp_right): 
            dis = rect.y + rect.h - self.rect.y
            self.y += dis
        elif tmp_rect.contains(tmp_down) and not tmp_rect.contains(tmp_left) and not tmp_rect.contains(tmp_right): 
            dis = -self.rect.y - self.rect.h + rect.y
            self.y += dis
        elif tmp_rect.contains(tmp_left) and not tmp_rect.contains(tmp_up) and not tmp_rect.contains(tmp_down): 
            dis = rect.x + rect.w - self.rect.x
            self.x += dis
        elif tmp_rect.contains(tmp_right) and not tmp_rect.contains(tmp_up) and not tmp_rect.contains(tmp_down): 
            dis = -self.rect.x - self.rect.w + rect.x
            self.x += dis
    
    def update_sprite(self, elapsed_time: float) -> None:
        """Updates the players movement."""
        
        # Movement

        if not self.step_stop:
            self.step_last += elapsed_time

        while self.step_last >= self.step_change:

            self.step_idx += 1
            self.step_last -= self.step_change
        
        if self.step_idx > self.step_max:
            self.step_idx = 0 # 1
        
        if self.step_stop:
            self.step_idx = 0
        
        self.step_stop = True

    def _render(self) -> pygame.surface.Surface:
        """Render the sprite graphic."""

        # Movement

        if self.dir == core.RIGHT:
            return self.images_right[self.step_idx]
        
        elif self.dir == core.LEFT:
            return self.images_left[self.step_idx]
        
        elif self.dir == core.UP:
            return self.images_up[self.step_idx]
        
        elif self.dir == core.DOWN:
            return self.images_down[self.step_idx]
    
