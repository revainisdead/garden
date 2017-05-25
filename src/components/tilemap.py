from typing import Set

import random

import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()

        # Private
        sprite = setup.GFX[sprite_name]

        # Public
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Map:
    def __init__(self) -> None:
        self.tile_names = [
            "grass_tile",
            "dirt_tile",
            "black_brick_tile",
            "water_bottom_right_corner_grass",
        ]

        width = int(c.MAP_WIDTH / c.TILE_SIZE)
        height = int(c.MAP_HEIGHT / c.TILE_SIZE)

        self.tiles = self.generate(width, height)
        self.map_surface = pg.Surface((c.MAP_WIDTH, c.MAP_HEIGHT))


    def generate(self, width: int, height: int) -> Set[Tile]:
        tiles = set()

        names_max = len(self.tile_names) - 1
        for y in range(0, height):
            for x in range(0, width):
                choice = random.randint(0, names_max)
                tiles.add(Tile(x * c.TILE_SIZE, y * c.TILE_SIZE, self.tile_names[choice]))

        return tiles


    def update(self, surface: pg.Surface, camera: pg.Rect) -> None:
        #tiles = [tile for tile in self.tiles if camera.colliderect(tile))
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))
