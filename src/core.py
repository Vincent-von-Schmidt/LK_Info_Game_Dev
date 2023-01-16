# Events

MOVE = "move"
ACTION = "action"
APP = "app"

# Directions

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
UP_LEFT = "up_down"
UP_RIGHT = "up_right"
DOWN_LEFT = "down_left"
DOWN_RIGHT = "down_right"

SHOOT = "bullets"

# Map

WALL = "wall"
GROUND = "ground"
DOOR = "door"

# Factions

NEUTRAL = "neutral"
MAP = "map"
FRIEND = "friend"
ENEMY = "enemy"
FAUNA = "fauna"
SPECIAL = "special"

QUIT = "quit"

# Funktions

def _distance_two_points(x1: float, y1: float, x2: float, y2: float) -> float:
    return ( (x2-x1)**2 + (y2-y1)**2 )**0.5