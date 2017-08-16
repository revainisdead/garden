from typing import Tuple

import pygame as pygame

from .. import constants as c


def get_image(
        x: int,
        y: int,
        width: int,
        height: int,
        sprite_sheet: pygame.Surface,
        mult: float=1,
        y_mult: float=None,
        colorkey: Tuple[int, int, int]=c.BLACK,
        transparent: bool=True) -> pygame.Surface:
    """Extracts from the sprite sheet, or just the sprite."""
    if transparent:
        # For images without transparency in them
        image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    else:
        image = pygame.Surface((width, height)).convert()
        image.set_colorkey(colorkey)

    rect = image.get_rect()

    image.blit(sprite_sheet, (0, 0), (x, y, width, height))

    #image.set_colorkey(colorkey)

    if y_mult is None:
        y_mult = mult
    size_delta = (int(rect.width * mult), int(rect.height * y_mult))
    image = pygame.transform.scale(image, size_delta)
    return image
