from typing import Tuple

import pygame as pg

from .. import constants as c


def get_image(
        x: int,
        y: int,
        width: int,
        height: int,
        sprite_sheet: pg.Surface,
        mult: float=1,
        colorkey: Tuple[int, int, int]=c.BLACK,
        transparent: bool=True) -> pg.Surface:
    """Extracts from the sprite sheet, or just the sprite."""
    if transparent:
        # For images without transparency in them
        image = pg.Surface([width, height], pg.SRCALPHA, 32)
    else:
        image = pg.Surface([width, height]).convert()
        image.set_colorkey(colorkey)

    rect = image.get_rect()

    image.blit(sprite_sheet, (0, 0), (x, y, width, height))

    #image.set_colorkey(colorkey)

    size_delta = (int(rect.width * mult), int(rect.height * mult))
    image = pg.transform.scale(image, size_delta)
    return image
