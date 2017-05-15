import pygame as pg

from .. import setup
from .. import constants as c

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies"]

        self.image = self.get_image(14, 7, 35, 42)


        # Get image's rect
        self.rect = self.image.get_rect()

        # Set rect's position
        self.rect.x = x
        self.rect.y = y


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.set_colorkey(c.YELLOW)

        return image
