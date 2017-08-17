from typing import List, Set, Tuple

import random

import pygame

from . import helpers, scenery, util

from .. import constants as c
from .. import setup


#all_tile_names


class Tile(pygame.sprite.Sprite):
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
    def __init__(self, grid_width: int, grid_height: int, map_width: int, map_height: int, biome: c.Biome) -> None:
        self.tile_names = [
            "grass", # 0, Starting value for grid
            "black_brick", # 1, Fill in cell value
            "dirt", # XXX How to use dirt?
        ]

        self.biome = biome

        self.water_choices = {
            c.Direction.UP: "water_top_grass",
            c.Direction.DOWN: "water_bottom_grass",
            c.Direction.LEFT: "water_left_grass",
            c.Direction.RIGHT: "water_right_grass",
            c.Direction.LEFTUP: "water_top_left_grass",
            c.Direction.LEFTDOWN: "water_bottom_left_grass",
            c.Direction.RIGHTUP: "water_top_right_grass",
            c.Direction.RIGHTDOWN: "water_bottom_right_grass",
            c.Direction.NONE: "water",
        }

        # Ex. Left Up means top left corner is grass.
        self.water_corners = {
            c.Direction.LEFTUP: "water_top_left_corner_grass",
            c.Direction.LEFTDOWN: "water_bottom_left_corner_grass",
            c.Direction.RIGHTUP: "water_top_right_corner_grass",
            c.Direction.RIGHTDOWN: "water_bottom_right_corner_grass",
        }

        # Position 0 = default
        # Position 1 = fill
        if self.biome == c.Biome.FARMLAND:
            self.tile_names = [
                "grass",
                "water",
            ]
        elif self.biome == c.Biome.CAVE:
            self.tile_names = [
                "lightbrown_brick",
                "black_brick",
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

        self.bush_group = pygame.sprite.Group()
        self.tree_bottom_group = pygame.sprite.Group()
        self.tree_top_group = pygame.sprite.Group()
        self.tree_shadow_group = pygame.sprite.Group()
        self.water_corner_cut_group = pygame.sprite.Group()
        self.fence_link_group = pygame.sprite.Group()
        self.fence_end_group = pygame.sprite.Group()

        # Initialize grid size.
        self.width = grid_width
        self.height = grid_height
        #self.width = c.GRID_WIDTH
        #self.height = c.GRID_HEIGHT

        # cellular automata values
        self.num_sim_steps = 4
        self.death_limit = 4
        self.birth_limit = 6

        # Use this list the same as the grid.
        # But instead of 1 being water, make 1 represent a collidable.
        self.collidable_grid = [[0 for y in range(self.height)] for x in range(self.width)]

        self.__generate_grid()
        self.tiles = self.create_tiles()

        # Let the caller determine map size.
        self.map_surface = pygame.Surface((map_width, map_height)).convert()


    def __generate_grid(self) -> None:
        # Initialize grid with random values.
        # 60% chance a 1 will occur.
        self.grid = [[0 if random.randint(0, 4) == 0 else 1 for y in range(self.height)] for x in range(self.width)]

        for _ in range(self.num_sim_steps):
            self.simulation_step()

        if self.biome == c.Biome.FARMLAND:
            # Checking for swaps from water to grass is only done for
            # farmland, for now.
            num_check_swaps = 3
            for _ in range(num_check_swaps):
                # Do a check for swaps before actually creating tiles.
                for gridy in range(self.height):
                    for gridx in range(self.width):
                        __, swapped = self.solid_tilename_calculation(gridx, gridy, False)
        else:
            pass


    def create_tiles(self) -> Set[Tile]:
        """Grid must be created before running this method.

        Calculate tile sprite's based surroundings:
            If a tile is surrounded by solid points:
                Is full water image.
            If a tile has only water to it's left:
                Water and left grass image.
            Etc.
        """
        tiles = set()
        #tiles = {}
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

                created_bush = False
                created_tree = False
                created_fence = False


                # Select names based on biome.

                if self.biome == c.Biome.FARMLAND:
                    if solid_grid_point:
                        tile_name, swapped = self.solid_tilename_calculation(gridx, gridy, True)
                        if swapped:
                            solid_grid_point = False

                    else:
                        # Create a variety of grasses.
                        tile_name = self.grass_names[random.randint(0, len(self.grass_names) - 1)]

                        created_tree = self.__create_tree(x_pos, y_pos)

                        if not created_tree:
                            # Don't draw bushes under trees.
                            created_bush = self.__create_bush(x_pos, y_pos)

                            if not created_bush:
                                pass

                    created_fence = self.__create_fence(x_pos, y_pos, gridx, gridy)

                    tile = Tile(x_pos, y_pos, tile_name)
                    tiles.add(tile) # Tile as set.

                    #point = (gridx, gridy)
                    #tiles[point] = tile

                    if solid_grid_point or created_tree:
                        self.collidable_grid[gridx][gridy] = 1
                elif self.biome == c.Biome.CAVE:
                    tile_name = self.tile_names[grid_point]

                    tile = Tile(x_pos, y_pos, tile_name)
                    tiles.add(tile) # Tile as set.

                    if solid_grid_point:
                        self.collidable_grid[gridx][gridy] = 1

        return tiles


    # XXX: Unused
    def retry_swapped(self, x: int, y:int) -> Tuple[str, bool]:
        while True:
            tile_name, swapped = self.solid_tilename_calculation(x, y, True)
            if not swapped:
                return tile_name, swapped


    def solid_tilename_calculation(self, x: int, y: int, create_corner_cuts: bool) -> Tuple[str, bool]:
        """Choose a solid tilename based on surroundings.

        :returns Tuple: tilename, swapped
        :returns tilename: Tilename
        :returns swapped: If the tile was swapped from solid (1) to empty (0)
        """
        num_directions = 8
        init_ones = [0 for _ in range(0, num_directions)]
        up, down, left, right, leftup, rightup, leftdown, rightdown = init_ones
        try:
            up = self.grid[x][y-1]      # Tile above.
            down = self.grid[x][y+1]    # Tile below.
            right = self.grid[x+1][y]   # Tile to the right.
            left = self.grid[x-1][y]    # Tile to the left.
            leftup = self.grid[x-1][y-1]
            rightup = self.grid[x+1][y-1]
            leftdown = self.grid[x-1][y+1]
            rightdown = self.grid[x+1][y+1]
        except IndexError:
            pass

        swapped = False
        tilename = self.water_choices[c.Direction.NONE]
        #tilename = self.grass_names[0]
        if up and down and left and right:
            # Four sides are covered
            # Check corner cases first, literally.
            if leftup and rightup and leftdown and rightdown:
                # All sides are covered.
                return self.water_choices[c.Direction.NONE], swapped

            # 2 Opposite corners are not solid.
            elif not leftup and not rightdown:
                if create_corner_cuts:
                    # Cover left up corner
                    self.create_corner(x, y, movex=False, movey=False, flipx=False, flipy=False)
                    # Cover right down corner
                    self.create_corner(x, y, movex=True, movey=True, flipx=True, flipy=True)
            elif not leftdown and not rightup:
                if create_corner_cuts:
                    # Cover left down corner
                    self.create_corner(x, y, movex=False, movey=True, flipx=False, flipy=True)
                    # Cover right up corner
                    self.create_corner(x, y, movex=True, movey=False, flipx=True, flipy=False)

            # All four sides are covered, and 1 corner is not.
            elif leftup and rightup and leftdown and not rightdown:
                return self.water_corners[c.Direction.RIGHTDOWN], swapped
            elif leftup and rightup and not leftdown and rightdown:
                return self.water_corners[c.Direction.LEFTDOWN], swapped
            elif leftup and not rightup and leftdown and rightdown:
                return self.water_corners[c.Direction.RIGHTUP], swapped
            elif not leftup and rightup and leftdown and rightdown:
                return self.water_corners[c.Direction.LEFTUP], swapped

        # 3 water side tiles
        elif down and left and right and not up:
            # UP GRASS
            if create_corner_cuts:
                if not leftdown:
                    self.create_corner(x, y, movex=False, movey=True, flipx=False, flipy=True)
                if not rightdown:
                    self.create_corner(x, y, movex=True, movey=True, flipx=True, flipy=True)
            return self.water_choices[c.Direction.UP], swapped
        elif up and left and right and not down:
            # DOWN GRASS
            if create_corner_cuts:
                if not leftup:
                    self.create_corner(x, y, movex=False, movey=False, flipx=False, flipy=False)
                if not rightup:
                    self.create_corner(x, y, movex=True, movey=False, flipx=True, flipy=False)
            return self.water_choices[c.Direction.DOWN], swapped
        elif up and down and right and not left:
            # LEFT GRASS
            if create_corner_cuts:
                if not rightdown:
                    self.create_corner(x, y, movex=True, movey=True, flipx=True, flipy=True)
                if not rightup:
                    self.create_corner(x, y, movex=True, movey=False, flipx=True, flipy=False)
            return self.water_choices[c.Direction.LEFT], swapped
        elif up and down and left and not right:
            # RIGHT GRASS
            if create_corner_cuts:
                if not leftdown:
                    self.create_corner(x, y, movex=False, movey=True, flipx=False, flipy=True)
                if not leftup:
                    self.create_corner(x, y, movex=False, movey=False, flipx=False, flipy=False)
            return self.water_choices[c.Direction.RIGHT], swapped

        # 2 water side tiles
        elif not right and not up and left and down:
            if create_corner_cuts:
                if not leftdown:
                    self.create_corner(x, y, movex=False, movey=True, flipx=False, flipy=True)
            return self.water_choices[c.Direction.RIGHTUP], swapped
        elif not left and not up and right and down:
            if create_corner_cuts:
                if not rightdown:
                    self.create_corner(x, y, movex=True, movey=True, flipx=True, flipy=True)
            return self.water_choices[c.Direction.LEFTUP], swapped
        elif not right and not down and left and up:
            if create_corner_cuts:
                if not leftup:
                    corner = scenery.WaterCornerCut(x * c.TILE_SIZE, y * c.TILE_SIZE)
                    #corner.rect.x += (c.TILE_SIZE - c.CORNER_SIZE)
                    corner.image = pygame.transform.flip(corner.image, False, False)
                    self.water_corner_cut_group.add(corner)
            return self.water_choices[c.Direction.RIGHTDOWN], swapped
        elif not left and not down and right and up:
            if create_corner_cuts:
                if not rightup:
                    self.create_corner(x, y, movex=True, movey=False, flipx=True, flipy=False)
            return self.water_choices[c.Direction.LEFTDOWN], swapped
        else:
            # GENIUS! If a water is by itself, change it to grass!
            self.grid[x][y] = 0 # Set grid position to empty.
            swapped = True
            tilename = self.grass_names[0]
            return tilename, swapped

        return tilename, swapped


    def create_corner(self, x: int, y: int, movex: bool, movey: bool, flipx: bool, flipy: bool) -> None:
        corner = scenery.WaterCornerCut(x * c.TILE_SIZE, y* c.TILE_SIZE)
        if movex:
            corner.rect.x += (c.TILE_SIZE - c.CORNER_SIZE)
        if movey:
            corner.rect.y += (c.TILE_SIZE - c.CORNER_SIZE)
        corner.image = pygame.transform.flip(corner.image, flipx, flipy)
        self.water_corner_cut_group.add(corner)


    def create_farm_biome(self) -> None:
        pass


    def create_cave_biome(self) -> None:
        pass


    def simulation_step(self) -> None:
        # Copy grid
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
                    test_point = 0

                if i == 0 and j == 0:
                    pass
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_x >= self.width or neighbor_y >= self.height:
                    count += 1
                elif test_point > 0:
                    count += 1

        return count


    def __create_bush(self, x, y) -> bool:
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


    def __create_tree(self, x, y) -> bool:
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


    def __create_fence(self, x: int, y: int, gridx: int, gridy: int) -> bool:
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
            num_links = random.randint(c.MIN_FENCE_LENGTH, c.MAX_FENCE_LENGTH)

            for fence_index in range(num_links):
                current_point = 1   # Assume point is taken, at first.
                next_point = 1      # Assume point is taken, at first.
                try:
                    current_point = self.grid[gridx][gridy]
                    next_point = self.grid[gridx + 1][gridy]
                except IndexError:
                    pass

                if (current_point == 0 and next_point == 1) or (current_point == 0 and fence_index == num_links - 1):
                    # Current point is good but the next one is solid,
                    # assume the fence ends here.
                    fence_end = scenery.FenceEnd(x, y)
                    self.collidable_grid[gridx][gridy] = 1

                    self.fence_end_group.add(fence_end)
                    created = True
                    break
                elif current_point == 0 and next_point == 0:
                    # Current point and the next right point are available.
                    fence_link = scenery.FenceLink(x, y)
                    self.collidable_grid[gridx][gridy] = 1

                    self.fence_link_group.add(fence_link)
                    created = True
                elif current_point == 1:
                    # Current point solid. Don't create anything.
                    break

                gridx += 1
                x += c.TILE_SIZE

        return created


    #def __create_house(self, x, y):
    #for farmland: def __farm_area
    #for farmland: def __create_stash
    #for farmland: def __create_stairs
    #for cave: __create_minerals? gems?
    #for island: __do a completely different map


    def create_collidables(self) -> pygame.sprite.Group:
        collidable_group = pygame.sprite.Group()

        for y in range(self.height):
            for x in range(self.width):
                if self.collidable_grid[x][y] > 0:
                    collidable_group.add(util.Collidable(x * c.TILE_SIZE, y * c.TILE_SIZE))

        return collidable_group


    def find_random_open_location(self) -> Tuple[int, int]:
        """ Based on collidable spots, return a random, open location.
        Return an actual location on the map, not the grid location."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.collidable_grid[x][y] == 0:
                return x * c.TILE_SIZE, y * c.TILE_SIZE


    def update(self, surface: pygame.Surface, camera: pygame.Rect) -> None:
        # Test tiles as dict
        #for tile in list(self.tiles.values()):
        for tile in self.tiles:
            if camera.colliderect(tile):
                surface.blit(tile.image, (tile.rect.x, tile.rect.y), (0, 0, c.TILE_SIZE, c.TILE_SIZE))

        self.water_corner_cut_group.draw(surface)

        # Draw scenery after tiles
        self.bush_group.draw(surface)

        # Draw tree shadows under the tree base.
        self.tree_shadow_group.draw(surface)
        self.tree_bottom_group.draw(surface)

        self.fence_link_group.draw(surface)
        self.fence_end_group.draw(surface)

        # Ensure tree tops are drawn last, they should cover tree bottoms.
        # Let state draw tree tops, so that they can be drawn over npcs.
