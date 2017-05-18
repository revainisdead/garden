import enum

import pygame as pg

from .. import setup
from .. import constants as c


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.image = self.get_image(180, 8, 34, 40)

        # Get image's rect
        self.rect = self.image.get_rect()

        # Set rect's position
        self.rect.x = x
        self.rect.y = y


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()

        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # THIS IS THE COLOR YOU WANT TO BE TRANSPARENT
        # HINT: The background color of the sprite sheet bmp
        image.set_colorkey(c.SAPPHIRE)


        return image


