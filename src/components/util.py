import pygame as pg

from .. import constants as c


class Collidable(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int=c.TILE_SIZE, height: int=c.TILE_SIZE) -> None:
        super().__init__()

        self.image = pg.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
