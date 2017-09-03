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
    def __init__(self, x: int, y: int, slot: "inventory.Slot"=None) -> None:
        w=c.TILE_SIZE*2
        h=c.TILE_SIZE*2
        self.rect = pygame.rect.Rect((x, y), (w, h))

        # Translate from x,y (topleft) given to where a tooltip should go.
        self.rect.centerx = x + c.SLOT_SIZE/2
        self.rect.bottom = y - 7

        self.slot = slot

        self.bg_color = c.BLACK


    def show(self, surface: pygame.surface.Surface) -> None:
        # background, border, text
        pygame.draw.rect(surface, self.bg_color, self.rect)
