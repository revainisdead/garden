from typing import List, Set

import random

import pygame as pg

from . import helpers, scenery, util

from .. import constants as c
from .. import setup


#all_tile_names


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
            ["small_green_treebottom", "small_green_treetop"],
            ["green_treebottom", "green_treetop"],
        ]

        self.collidables = []
        self.bush_group = pg.sprite.Group()

        self.tree_bottom_group = pg.sprite.Group()
        self.tree_top_group = pg.sprite.Group()
        self.tree_shadow_group = pg.sprite.Group()

        self.fence_link_group = pg.sprite.Group()
        self.fence_end_group = pg.sprite.Group()

        self.width = c.GRID_WIDTH
        self.height = c.GRID_HEIGHT

        # cellular automata values
        self.num_sim_steps = 4
        self.death_limit = 4
        self.birth_limit = 6

        self.tiles = self.generate()
        self.map_surface = pg.Surface((c.MAP_WIDTH, c.MAP_HEIGHT)).convert()


    def generate(self) -> Set[Tile]:
        tiles = set()

        # Initialize grid with random values.
        # 60% chance a 1 will occur.
        self.grid = [[0 if random.randint(0, 4) == 0 else 1 for y in range(self.height)] for x in range(self.width)]

        for _ in range(self.num_sim_steps):
            self.simulation_step()

        # x and y here represent the virtual values of the map.
        # Real point: (64, 64)
        # Virtual point: (1, 1)
        for gridy in range(self.height):
            for gridx in range(self.width):
                x_pos = gridx * c.TILE_SIZE
                y_pos = gridy * c.TILE_SIZE

                grid_point = self.grid[gridx][gridy]
                solid_grid_point = grid_point == 1
                tile_name = self.tile_names[grid_point]

                if tile_name in self.grass_names:
                    # Create a variety of grasses.
                    tile_name = self.grass_names[random.randint(0, len(self.grass_names) - 1)]
                    created_bush = False
                    created_tree = self.create_tree(x_pos, y_pos)
                    created_fence = False

                    if not created_tree:
                        # Don't draw bushes under trees.
                        created_bush = self.create_bush(x_pos, y_pos)

                        if not created_bush:
                            created_fence = self.create_fence(x_pos, y_pos, gridx, gridy)

                tile = Tile(x_pos, y_pos, tile_name)
                tiles.add(tile)

                if solid_grid_point or created_fence or created_tree:
                    self.collidables.append(tile.rect)

        return tiles


    def simulation_step(self):
        # copy grid
        new_grid = self.grid

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_alive_neighbors(x, y)

                # Cell rules.
                # DL - Death limit
                # BL - Birth limit
                # Living cell has less than DL living neighbors: dies.
                # Living cell has DL or BL living neighbors: lives.
                # Living cell has more than BL living neighbors: dies.
                # Dead cell has exactly BL living neighbors: lives.
                if self.grid[x][y]: # Living cell
                    if neighbors < self.death_limit:
                        new_grid[x][y] = 0
                    elif neighbors == self.death_limit or neighbors == self.birth_limit:
                        new_grid[x][y] = 1
                    elif neighbors > self.birth_limit:
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
        Chance to create the object = 1 / density
        """
        density = c.BUSH_DENSITY
        choice = random.randint(1, density)
        name = self.bush_names[random.randint(0, len(self.bush_names) - 1)]

        created = False
        if choice == 1:
            bush = scenery.Bush(x, y, name)
            self.bush_group.add(bush)
            created = True

        return created


    def create_tree(self, x, y) -> bool:
        """
        Chance to create the object = 1 / density
        """
        density = c.TREE_DENSITY
        choice = random.randint(1, density)
        names = self.tree_name_pairs[random.randint(0, len(self.tree_name_pairs) - 1)]

        created = False
        if choice == 1:
            tree_bottom = scenery.TreeBottom(x, y, names[0])
            tree_top = scenery.TreeTop(x, y - c.TILE_SIZE, names[1])
            self.tree_bottom_group.add(tree_bottom)
            self.tree_top_group.add(tree_top)

            tree_shadow = scenery.TreeShadow(x, y + c.TREE_SHADOW_OFFSET)
            self.tree_shadow_group.add(tree_shadow)

            created = True

        return created


    def create_fence(self, x: int, y: int, gridx: int, gridy: int) -> bool:
        """
        Chance to create the object = 1 / density

        :param x: Real x location
        :param y: Real y location
        :param gridx: Grid x location
        :param gridy: Grid y location
        """
        density = c.FENCE_DENSITY
        choice = random.randint(1, density)

        created = False
        if choice == 1:
            num_links = random.randint(0, c.MAX_FENCE_LENGTH)

            for fence_index in range(num_links):
                gridx += 1
                x += c.TILE_SIZE
                try:
                    current_point = self.grid[gridx][gridy]
                    next_point = self.grid[gridx + 1][gridy]
                except IndexError:
                    break

                if (current_point == 0 and next_point == 1) or fence_index == num_links - 1:
                    # Current point is good but the next one is solid,
                    # assume the fence ends here.
                    fence_end = scenery.FenceEnd(x, y)
                    self.fence_end_group.add(fence_end)
                    created = True
                    break
                elif current_point == 0 and next_point == 0:
                    # Current point and the next right point is available.
                    fence_link = scenery.FenceLink(x, y)
                    self.fence_link_group.add(fence_link)
                    created = True
                elif current_point > 1:
                    break

        return created


    #def create_house(self, x, y):


    def create_collidables(self) -> List[util.Collidable]:
        collidables = []

        for rect in self.collidables:
            collidable = util.Collidable(rect.x, rect.y)
            collidables.append(collidable)
        return collidables


    def update(self, surface: pg.Surface, camera: pg.Rect) -> bool:
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))

        # Draw scenery after tiles
        self.bush_group.draw(surface)

        # Draw tree shadows under the tree base.
        self.tree_shadow_group.draw(surface)
        self.tree_bottom_group.draw(surface)

        self.fence_link_group.draw(surface)
        self.fence_end_group.draw(surface)

        # Ensure tree tops are drawn last, they should cover tree bottoms.
        # Let state draw tree tops, so that they can be drawn over npcs.
