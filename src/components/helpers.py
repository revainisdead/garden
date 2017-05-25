from typing import Tuple

import pygame as pg

from .. import constants as c


# XXX Include alpha argument: alpha: bool=False
# if not alpha:
#   image = pg.Surface([width, height]).convert_alpha()
# else:
#   image = pg.Surface([width, height]).convert()
def get_image(
        x: int,
        y: int,
        width: int,
        height: int,
        sprite_sheet: pg.Surface,
        mult: float=1,
        colorkey: Tuple[int, int, int]=c.BLACK) -> pg.Surface:
    """Extracts from the sprite sheet, or just the sprite."""
    image = pg.Surface([width, height]).convert()
    rect = image.get_rect()

    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)

    size_delta = (int(rect.width * mult), int(rect.height * mult))
    image = pg.transform.scale(image, size_delta)
    return image
