import pygame

from . import helpers
from . import item

from .. import constants as c
from .. import setup


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
        self.font = setup.FONTS["game_kenvector_future_thin"]
        self.bg_color = c.BLACK

        self.w=c.TILE_SIZE*3
        self.h=c.TILE_SIZE*3
        self.rect = pygame.rect.Rect((x, y), (self.w, self.h))

        # Translate from x,y (topleft) given to where a tooltip should go.
        self.rect.centerx = x + c.SLOT_SIZE/2

        self.rect.bottom = y - 7
        if self.rect.top < 0:
            self.rect.top = y + c.SLOT_SIZE + 7

        self.slot = slot


    def show(self, surface: pygame.surface.Surface) -> None:
        pygame.draw.rect(surface, self.bg_color, self.rect)
        self.render_description(surface)


    def render_description(self, surface: pygame.surface.Surface) -> None:
        """
        Pygame text render can only one line at a time.
        Split by new lines and create a surface per line.
        """
        texts = {} # type: Dict[pygame.surface.Surface, pygame.rect.Rect]

        desc = self.slot.item.description.split("\n")
        offset = 5

        for ea in desc:
            text_surf = self.font.render(ea, True, self.slot.item.color)
            text_rect = text_surf.get_rect(top=self.rect.top + offset, left=self.rect.left)
            texts[text_surf] = text_rect

            offset += 10

        for text_surf, text_rect in texts.items():
            surface.blit(text_surf, text_rect)
