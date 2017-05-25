import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup


class Bush(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()

        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
