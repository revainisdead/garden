import pygame as pg

from .. import setup
from .. import constants as c


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]

        self.image = self.get_image(14, 7, 35, 42)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        #image.set_colorkey(c.YELLOW)

        return image
