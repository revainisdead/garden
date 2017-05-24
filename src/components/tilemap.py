import random

import pygame as pg

from .. import constants as c
from .. import setup


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name):
        super().__init__()

        self.sprite = setup.GFX[sprite_name]
        self.image = self.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)

        size_delta = (int(rect.width*c.TILE_MULT), int(rect.height*c.TILE_MULT))
        image = pg.transform.scale(image, size_delta)
        return image


class Map:
    def __init__(self):
        self.width = int(c.MAP_WIDTH / c.TILE_SIZE)
        self.height = int(c.MAP_HEIGHT / c.TILE_SIZE)

        self.tile_names = [
            "grass_tile",
            "dirt_tile",
            "black_brick_tile",
        ]

        self.generate()


    def generate(self):
        self.tiles = set()

        names_max = len(self.tile_names) - 1

        for y in range(0, self.height):
            for x in range(0, self.width):
                choice = random.randint(0, names_max)
                tile = Tile(x * c.TILE_SIZE, y * c.TILE_SIZE, self.tile_names[choice])
                self.tiles.add(tile)

    def update(self, surface):
        for tile in self.tiles:
            surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))
