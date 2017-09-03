import pygame

from . import helpers

from .. import constants as c


class Tooltip:
    """
    Instead of an sprite and an image, draw a rect and another tilted rect
    (or triangle) on the bottom side, like a speech box.

    - Include a border
    - Colored text
    - Bold title
    - Either very dark or very light background for contrast.
    _________
    |       |
    |       |
    |__  ___|
       \/

    """
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.rect = pygame.rect.Rect((x, y),
        self.rect.x = x
        self.rect.y = y



