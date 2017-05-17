import enum

import pygame as pg

from .. import setup
from .. import constants as c


class EnemyType(enum.Enum):
    # Is this necessary? Just make Enemy a base class
    TURTLE = 0
    FISH = 1


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        # Can also set on creation what this enemy contains
        # contents
        # Or start an initial state for the enemy
        # initial_state

        super().__init__()

        self.sprite_sheet = setup.GFX["enemies"]

        self.image = self.get_image(180, 8, 34, 40)

        # Get image's rect
        self.rect = self.image.get_rect()

        # Set rect's position
        self.rect.x = x
        self.rect.y = y


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        #image.set_colorkey(c.YELLOW)

        return image
