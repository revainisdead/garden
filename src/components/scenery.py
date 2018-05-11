from typing import Optional

import pygame

import random

from . import helpers

from .. import constants as c
from .. import gameinfo
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


class _Tree(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, sprite_name: str, other_half_id: int=None) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.available_actions = [
            c.Action.Cut,
        ]

        self.__other_half_id = other_half_id
        self.__last_groups = None # type: List[pygame.sprite.Group]

        self.dead = False
        self.__kill_time = None
        self.__respawn_rate = 60


    def destroy(self, game_time: int) -> None:
        """
        Destroy this sprite. Provides a chance to get an item.

         - Save the groups this sprite is in, so that it can
           be re-added to them after a certain timer.
        """
        self.__last_groups = self.groups()
        self.__kill_time = game_info.game_time
        self.dead = True
        self.kill()


class TreeBottom(_Tree):
    def update(self, game_info: gameinfo.GameInfo) -> None:
        """
        Update will only be called on a collision, assume a collision was made.
        """
        #collided = pygame.sprite.spritecollideany(game_info.player, self.groups()[0])
        #if collided:
        if not game_info.action_attempts.empty():
            if action in self.available_actions:
                action = game_info.action_attempts.get()
                self.activate_action(action, game_info)

        self.handle_state(game_info.game_time)


    def activate_action(self, action: c.Action, game_info: gameinfo.GameInfo) -> None:
        if action == self.available_actions[0]:
            if not self.dead:
                self.destroy(game_info.game_time)
                game_info.new_items.put(game_info.item_gen_proc.drop())


    def revive(self) -> None:
        for grp in self.__last_groups:
            grp.add(self)

        self.__kill_time = None
        self.dead = False


    def handle_state(self, game_time: int) -> None:
        self.__check_respawn(game_time)


    def __check_respawn(self, game_time) -> None:
        if self.dead and self.__kill_time:
            if game_time - self.__kill_time > self.__respawn_rate:
                self.revive()



class TreeTop(_Tree):
    def update(self, tree_bottom_id: int=None) -> None:
        if self.__other_half_id == tree_bottom_id:
            self.destroy(game_time)


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
