from typing import Set

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

        self.tree_name_pairs = [
            ["small_brown_treebottom", "small_brown_treetop"],
            ["brown_treebottom", "brown_treetop"],
        ]

        self.collidables = []
        self.bush_group = pg.sprite.Group()
        self.tree_group = pg.sprite.Group()
        self.tree_shadow_group = pg.sprite.Group()

        self.width = int(c.MAP_WIDTH / c.TILE_SIZE)
        self.height = int(c.MAP_HEIGHT / c.TILE_SIZE)

        # cellular automata values
        self.num_sim_steps = 2
        self.death_limit = 2
        self.birth_limit = 3

        self.tiles = self.generate()
        self.map_surface = pg.Surface((c.MAP_WIDTH, c.MAP_HEIGHT)).convert()


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
                # Actual position on the map.
                x_pos = x * c.TILE_SIZE
                y_pos = y * c.TILE_SIZE

                grid_point = self.grid[x][y]
                tile_name = self.tile_names[grid_point]

                if tile_name in self.grass_names:
                    # Create a variety of grasses.
                    tile_name = self.grass_names[random.randint(0, len(self.grass_names) - 1)]
                    created_tree = self.create_tree(x_pos, y_pos)

                    if not created_tree:
                        # Don't draw bushes under trees.
                        created_bush = self.create_bush(x_pos, y_pos)

                # If the rect is 1, it should be added to a list
                # that is parsed to create collidable rects.

                #self.collidables.append
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
                    test_point = 1

                if i == 0 and j == 0:
                    pass
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_x >= self.width or neighbor_y >= self.height:
                    count += 1
                elif test_point:
                    count += 1

        return count


    def create_bush(self, x, y) -> bool:
        """
        Chance to create a bush = 1 / density
        """
        density = c.BUSH_DENSITY
        choice = random.randint(1, density)
        bush_name = self.bush_names[random.randint(0, len(self.bush_names) - 1)]

        created = False
        if choice == 1:
            bush = scenery.Bush(x, y, bush_name)
            self.bush_group.add(bush)
            created = True

        return created


    def create_tree(self, x, y) -> bool:
        """
        Chance to create a tree = 1 / density
        """
        density = c.BUSH_DENSITY
        choice = random.randint(1, density)
        tree_names = self.tree_name_pairs[random.randint(0, len(self.tree_name_pairs) - 1)]

        created = False
        if choice == 1:
            treebottom = scenery.TreeBottom(x, y, tree_names[0])
            treetop = scenery.TreeTop(x, y - c.TILE_SIZE, tree_names[1])
            self.tree_group.add(treebottom, treetop)

            treeshadow = scenery.TreeShadow(x, y + 9)
            self.tree_shadow_group.add(treeshadow)

            created = True

        return created


    #def create_house(self, x, y):


    def update(self, surface: pg.Surface, camera: pg.Rect) -> bool:
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))

        # Draw scenery after tiles
        self.bush_group.draw(surface)
        self.tree_group.draw(surface)

        # Draw tree shadows on top of the tree base.
        self.tree_shadow_group.draw(surface)
