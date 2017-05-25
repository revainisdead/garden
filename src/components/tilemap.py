from typing import Optional, Set

import random

import pygame as pg

from . import helpers
from . import scenery

from .. import constants as c
from .. import setup


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()

        # Private
        sprite = setup.GFX[sprite_name]

        # Public
        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Map:
    def __init__(self) -> None:
        self.tile_names = [
            "grass",
            "dirt",
            "black_brick",
            "water_bottom_right_corner_grass",
        ]

        self.bush_names = [
            "small_green_bush",
        ]

        self.bush_group = pg.sprite.Group()

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
                tile_name = self.tile_names[choice]

                x_pos = x * c.TILE_SIZE
                y_pos = y * c.TILE_SIZE

                if tile_name == "grass":
                    bush = self.create_bush(x_pos, y_pos)
                    if bush:
                        self.bush_group.add(bush)

                tiles.add(Tile(x_pos, y_pos, tile_name))

        return tiles


    def create_bush(self, x, y) -> Optional[scenery.Bush]:
        """
        Chance to create a bush = 1 / density
        """
        density = 9
        choice = random.randint(0, density)
        bush_name = self.bush_names[random.randint(0, len(self.bush_names) - 1)]
        bush = None

        if choice == 0:
            bush = scenery.Bush(x, y, bush_name)

        return bush


    def update(self, surface: pg.Surface, camera: pg.Rect) -> None:
        #tiles = [tile for tile in self.tiles if camera.colliderect(tile))
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))

        # Draw scenery after tiles
        self.bush_group.draw(surface)
