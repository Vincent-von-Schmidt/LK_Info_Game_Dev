import pygame

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

# Debug functions

def _downscale_coordinates(
    point: tuple[float, float],
    size_is: tuple[float, float],
    size_should: tuple[float, float]
) -> tuple[float, float]:
    """Projects the coordinates from a rect into another."""

    x_fac = size_should[0] / size_is[0]
    y_fac = size_should[1] / size_is[1]

    return (point[0] * x_fac, point[1] * y_fac)


def _render_coordinates(
    point: tuple[float, float] | None = None
) -> list[tuple[pygame.surface.Surface, tuple[float, float]]]:
    """Render a coordinate system for the map."""

    offset = (0, 32) # Integer
    maximum = (272, 208) # Integer
    steps = (20, 20) # Integer
    color = pygame.Color("Red")
    font = pygame.font.SysFont('Arial', 10)

    width = 2
    lenght = 5

    dis = 5

    # Create surface
    
    surface = pygame.Surface((272, 208), pygame.SRCALPHA)
    surface.convert_alpha()
    surface.fill([0, 0, 0, 0])

    # Draw axes

    x_start = (offset[0], offset[1])
    x_end = (maximum[0], offset[1])
    y_start = (offset[0], offset[1])
    y_end = (offset[0], maximum[1])

    pygame.draw.line(surface, color, x_start, x_end, width=width)
    pygame.draw.line(surface, color, y_start, y_end, width=width)

    # Draw steps

    for x in range(offset[0], maximum[0], steps[0]):

        if x == offset[0]:
            continue

        start = (x, offset[1])
        end = (x, offset[1] + lenght)
        text = font.render(str(x), True, color)
        pos = (x - text.get_rect().w / 2, offset[1] + lenght)
        
        pygame.draw.line(surface, color, start, end, width=width)
        surface.blit(text, pos)
    
    for y in range(offset[1], maximum[1], steps[1]):

        if y == offset[1]:
            continue
        
        start = (offset[0], y)
        end = (offset[0] + lenght, y)
        text = font.render(str(y), True, color)
        pos = (offset[0] + lenght, y - text.get_rect().h / 2)
        
        pygame.draw.line(surface, color, start, end, width=width)
        surface.blit(text, pos)

    # Draw point

    if point:

        px_start = (point[0], offset[1])
        py_start = (offset[0], point[1])

        pygame.draw.line(surface, color, px_start, point, width=width)
        pygame.draw.line(surface, color, py_start, point, width=width)
        pygame.draw.circle(surface, color, point, radius=width)

        text = font.render(f"{point[0]:.0f}, {point[1]:.0f}", True, color)
        pos = (point[0] + dis, point[1] + dis)
        surface.blit(text, pos)

    return [(surface, (0, 0))]