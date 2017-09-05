from typing import Optional

import pygame

import random

from . import helpers

from .. import constants as c
from .. import setup


class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeShadow(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["tree_shadow"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeBottom(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]


        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeTop(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__last_groups = None # type: List[pygame.sprite.Group]

        self.dead = False
        self.__kill_time = 0
        self.__respawn_rate = 10000

        # If treetop is harvested, kill it's shadow
        # Not necessary, maybe, I also want to kill trees so that they
        # can be walked through. Stumps should probably be walk-through
        # able, and they maybe still have a shadow but certain not the
        # same shadow as the whole tree.

        # If treetop is harvested, how to know whether to draw it? Need public method to see if it needs to be drawn


    def update(self) -> None:
        self.handle_state()


    def destroy(self) -> None:
        """
        Destroy this sprite. Provides a chance to get an item.

         - Save the groups this sprite is in, so that it can
           be re-added to them after a certain timer.
        """
        self.__last_groups = self.groups()
        self.__kill_time = self.game_time
        self.dead = True
        self.kill()


    def revive(self) -> None:
        for grp in self.__last_groups:
            grp.add(self)

        self.__kill_time = 0
        self.dead = False


    def handle_state(self, game_time: int) -> None:
        if self.dead:
            self.__check_respawn(game_time)


    def __check_respawn(self, game_time) -> None:
        if game_time - self.__kill_time > self.__respawn_rate:
            self.revive()


class FenceLink(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["fence_link"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class FenceEnd(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["fence_end"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class WaterCornerCut(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["water_top_left_corner_grass"]

        self.image = helpers.get_image(0, 0, c.CORNER_SIZE, c.CORNER_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Stairs(pygame.sprite.Sprite):
    def __init__(self, x, y, name) -> None:
        super().__init__()
        sprite = setup.GFX[name]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Flip some stairs around. So that it's realistic for the player
        # to "walk" down the correct side of the stairs. Should only be
        # left or right (because art).
        if random.randint(0, 2) == 0:
            self.stairs_dir = c.Direction.LEFT
        else:
            self.stairs_dir = c.Direction.RIGHT
            self.image = pygame.transform.flip(self.image, True, False)

        self.hit = False


    def update(self, player_rect: pygame.Rect) -> None:
        # Setting hit to true when hit should work even if it's just
        # for one frame.
        self.hit = False

        if self.stairs_dir == c.Direction.LEFT:
            if player_rect.right == self.rect.left:
                if player_rect.centery > self.rect.top and player_rect.centery < self.rect.bottom:
                    self.hit = True
        elif self.stairs_dir == c.Direction.RIGHT:
            if player_rect.left == self.rect.right:
                if player_rect.centery > self.rect.top and player_rect.centery < self.rect.bottom:
                    self.hit = True
