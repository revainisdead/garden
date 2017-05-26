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

        # Not stored in object
        sprite = setup.GFX[sprite_name]

        # Stored in object
        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Map:
    def __init__(self) -> None:
        self.tile_names = [
            "grass", # 0, Starting value for grid
            "black_brick", # 1, Fill in cell value
            "water_bottom_right_corner_grass",
            "dirt",
        ]

        # Test a grass biome
        biome = "island"

        # Position 0 = default
        # Position 1 = fill
        if biome == "island":
            self.tile_names = [
                "grass",
                "water",
            ]
        elif biome == "cave":
            self.tile_names = [
                "black_brick",
                "gray_brick",
            ]


        self.grass_names = [
            "grass",
            "grass2",
        ]

        self.bush_names = [
            "small_green_bush",
            "small_forest_green_bush",
            "small_brown_bush",
            "green_bush",
            "brown_bush",
        ]

        self.bush_group = pg.sprite.Group()

        self.width = int(c.MAP_WIDTH / c.TILE_SIZE)
        self.height = int(c.MAP_HEIGHT / c.TILE_SIZE)

        # cellular automata values
        self.num_sim_steps = 2
        self.death_limit = 2
        self.birth_limit = 3

        self.tiles = self.generate()
        self.map_surface = pg.Surface((c.MAP_WIDTH, c.MAP_HEIGHT))


    def generate(self) -> Set[Tile]:
        tiles = set()

        # Initialize grid with random values.
        # 40% chance a 1 will occur.
        self.grid = [[1 if random.randint(0, 4) == 0 else 0 for y in range(self.height)] for x in range(self.width)]

        for _ in range(self.num_sim_steps):
            self.simulation_step()

        # x and y here represent the virtual values of the map.
        # Real point: (64, 64)
        # Virtual point: (1, 1)
        for y in range(self.height):
            for x in range(self.width):
                # Stop choosing randomly for now
                #choice = random.randint(0, names_max)
                #if self.biome == "grass":
                    #tile_name = self.grass_names[choice]
                #else:
                    #tile_name = self.tile_names[choice]

                # Actual position on the map.
                x_pos = x * c.TILE_SIZE
                y_pos = y * c.TILE_SIZE

                grid_point = self.grid[x][y]
                tile_name = self.tile_names[grid_point]

                if tile_name in self.grass_names:
                    bush = self.create_bush(x_pos, y_pos)
                    if bush:
                        self.bush_group.add(bush)

                tiles.add(Tile(x_pos, y_pos, tile_name))


        return tiles


    def simulation_step(self):
        # copy grid
        new_grid = self.grid

        for y in range(self.height):
            for x in range(self.width):
        #for x, row in enumerate(self.grid):
            #for y, _ in enumerate(row):

                neighbors = self.count_alive_neighbors(x, y)

                # Cell rules.
                # Living cell has less than 2 living neighbors: dies.
                # Living cell has 2 or 3 living neighbors: lives.
                # Living cell has more than 3 living neighbors: dies.
                # Dead cell has exactly 3 living neighbors: lives.
                if self.grid[x][y]: # Living cell
                    if neighbors < self.death_limit:
                        new_grid[x][y] = 0
                    elif neighbors == 2 or neighbors == 3:
                        new_grid[x][y] = 1
                    elif neighbors > 3:
                        new_grid[x][y] = 0
                else: # Dead cell
                    if neighbors > self.birth_limit:
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0

        # replace grid
        self.grid = new_grid

    def count_alive_neighbors(self, x: int, y: int) -> int:
        """Returns the number of cells around the point that are alive"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = x+i
                neighbor_y = y+j

                try:
                    test_point = self.grid[neighbor_x][neighbor_y]
                except IndexError:
                    test_point = 0

                if i == 0 and j == 0:
                    pass
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_x >= self.width or neighbor_y >= self.height:
                    count += 1
                elif test_point:
                    count += 1

        return count


    def create_bush(self, x, y) -> Optional[scenery.Bush]:
        """
        Chance to create a bush = 1 / density
        """
        density = c.BUSH_DENSITY
        choice = random.randint(1, density)
        bush_name = self.bush_names[random.randint(0, len(self.bush_names) - 1)]
        bush = None

        if choice == 1:
            bush = scenery.Bush(x, y, bush_name)

        return bush


    def update(self, surface: pg.Surface, camera: pg.Rect) -> None:
        #tiles = [tile for tile in self.tiles if camera.colliderect(tile))
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))

        # Draw scenery after tiles
        self.bush_group.draw(surface)
