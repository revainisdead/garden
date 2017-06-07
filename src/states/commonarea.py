from typing import Any, Dict, Tuple

import time
import random

import pygame as pg

from .. import binds
from .. import constants as c
from .. import control
from .. import setup
from .. import tools

from .. components import non_player_controlled, player, tilemap, user_interface


class CommonArea(control.State):
    def __init__(self) -> None:
        super().__init__()
        self.setup_map()


    def startup(self, game_info: Dict[str, Any]) -> None:
        self.game_info = game_info
        self.state = c.MainState.COMMONAREA

        self.setup_player()
        self.npc_group = self.setup_npcs()
        self.setup_camera()


    def setup_map(self) -> None:
        self.tilemap = tilemap.Map()
        self.collidable_group = self.tilemap.create_collidables()
        self.tilemap_rect = self.tilemap.map_surface.get_rect()
        self.entire_area = pg.Surface((self.tilemap_rect.width, self.tilemap_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()


    def setup_camera(self) -> None:
        # Start the camera on top of the player.
        self.camera = pg.Rect((self.player.rect.x, self.player.rect.y), (setup.screen_size.get_width(), setup.screen_size.get_height()))
        self.camera.centerx = self.player.rect.centerx
        self.camera.centery = self.player.rect.centery

        self.direction = c.Direction.NONE
        self.camera_speed = c.speeds["camera"]
        self.set_camera_velocity()

        # Call move_camera once in setup to force the camera to center
        # on the player.
        self.move_camera()


    def setup_npcs(self) -> pg.sprite.Group:
        npcs = [] # type: List[non_player_controlled.Npc]
        npc_group = pg.sprite.Group()

        # min_npc_amount
        # max_npc_amount
        random_npcs_limit = random.randint(c.MIN_NPC_AMOUNT, c.MAX_NPC_AMOUNT)

        for _ in range(random_npcs_limit):
            x, y = self.tilemap.find_random_open_location()
            npc_group.add(non_player_controlled.Npc(x, y))

        return npc_group


    def setup_player(self) -> None:
        # But should the player's location be random? Maybe, go find your farm!
        x, y = self.tilemap.find_random_open_location()
        self.player = player.Player(x, y)
        self.player_group = pg.sprite.Group(self.player)


    def update(self, surface: pg.Surface, current_time: float) -> None:
        """Update the state every frame"""
        self.game_info["current_time"] = current_time

        self.update_sizes()
        self.update_sprites()
        self.handle_states()
        self.blit_images(surface)


    def handle_states(self) -> None:
        if binds.INPUT.pressed("escape"):
            self.quit = True
        else:
            self.move_camera()


    def update_sizes(self) -> None:
        """Used when changing the screen resolution"""
        if setup.screen_size.changed():
            # Start new camera at the same position as before.
            self.camera = pg.Rect((self.camera.x, self.camera.y), (setup.screen_size.get_width(), setup.screen_size.get_height()))


    def update_sprites(self) -> None:
        self.player_group.update(self.game_info["current_time"], self.collidable_group)
        self.npc_group.update(self.game_info["current_time"], self.collidable_group)


    def move_camera(self) -> None:
        """
        if binds.INPUT.held("left"):
            # XXX Hacking different directions into each of these directions
            # doesn't help. The if statement priority still takes
            # precedence. How to make it so that the new button pressed
            # is the one that takes priority? Maybe change Input class.
            if binds.INPUT.held("up"):
                self.direction = c.Direction.LEFTUP
            elif binds.INPUT.held("down"):
                self.direction = c.Direction.LEFTDOWN
            else:
                self.direction = c.Direction.LEFT
            self.move_camera()

        elif binds.INPUT.held("right"):
            if binds.INPUT.held("up"):
                self.direction = c.Direction.RIGHTUP
            elif binds.INPUT.held("down"):
                self.direction = c.Direction.RIGHTDOWN
            else:
                self.direction = c.Direction.RIGHT
            self.move_camera()
        elif binds.INPUT.held("up"):
            self.direction = c.Direction.UP
            self.move_camera()
        elif binds.INPUT.held("down"):
            self.direction = c.Direction.DOWN
            self.move_camera()
        else:
            self.direction = c.Direction.NONE
        """

        self.direction = self.player.direction
        self.set_camera_velocity()

        new_x, new_y = tools.fix_edge_bounds(rect=self.camera, highest_x=self.tilemap_rect.right, highest_y=self.tilemap_rect.bottom, x_vel=self.camera_x_vel, y_vel=self.camera_y_vel)

        check_gt_x = lambda x: x if x > self.camera.centerx else self.camera.centerx
        check_lt_x = lambda x: x if x < self.camera.centerx else self.camera.centerx
        check_gt_y = lambda y: y if y > self.camera.centery else self.camera.centery
        check_lt_y = lambda y: y if y < self.camera.centery else self.camera.centery

        if self.camera.x != new_x:
            if self.direction == c.Direction.LEFT:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHT:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.LEFTUP:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHTUP:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.LEFTDOWN:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHTDOWN:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)

        if self.camera.x < 0:
            self.camera.x = 0
        elif self.camera.x + self.camera.w > self.tilemap_rect.right:
            self.camera.x = new_x

        if self.camera.y < 0:
            self.camera.y = 0
        elif self.camera.y + self.camera.h > self.tilemap_rect.bottom:
            self.camera.y = new_y

        new_x, new_y = tools.fix_edge_bounds(rect=self.camera, highest_x=self.tilemap_rect.right, highest_y=self.tilemap_rect.bottom, x_vel=self.camera_x_vel, y_vel=self.camera_y_vel)

        if self.camera.y != new_y:
            if self.direction == c.Direction.UP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.DOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)
            elif self.direction == c.Direction.LEFTUP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.RIGHTUP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.LEFTDOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)
            elif self.direction == c.Direction.RIGHTDOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)


        if self.camera.x < 0:
            self.camera.x = 0
        elif self.camera.x + self.camera.w > self.tilemap_rect.right:
            self.camera.x = new_x

        if self.camera.y < 0:
            self.camera.y = 0
        elif self.camera.y + self.camera.h > self.tilemap_rect.bottom:
            self.camera.y = new_y

        # Debug.
        #print("camera.y: {}".format(self.camera.y))
        #print("new_y:    {}".format(new_y))
        #self.camera.centerx = self.player.rect.centerx
        #self.camera.centery = self.player.rect.centery


    def set_camera_velocity(self) -> None:
        self.camera_x_vel = 0
        self.camera_y_vel = 0

        if self.direction == c.Direction.LEFT:
            self.camera_x_vel = -self.camera_speed
        elif self.direction == c.Direction.RIGHT:
            self.camera_x_vel = self.camera_speed
        elif self.direction == c.Direction.UP:
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.DOWN:
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.LEFTUP:
            self.camera_x_vel = -self.camera_speed
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.LEFTDOWN:
            self.camera_x_vel = -self.camera_speed
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.RIGHTUP:
            self.camera_x_vel = self.camera_speed
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.RIGHTDOWN:
            self.camera_x_vel = self.camera_speed
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.NONE:
            self.camera_x_vel = 0
            self.camera_y_vel = 0


    def blit_images(self, surface: pg.Surface) -> None:
        # This is responsible for showing only a certain area
        # of the tilemap surface, the area shown is the area of the camera.
        self.entire_area.blit(self.tilemap.map_surface, self.camera, self.camera)

        self.tilemap.update(self.entire_area, self.camera)
        self.npc_group.draw(self.entire_area)

        # Draw player over npc's, to make player feel more important...
        self.player_group.draw(self.entire_area)
        self.tilemap.tree_top_group.draw(self.entire_area)

        # Finally, draw everything to the screen surface.
        surface.blit(self.entire_area, (0, 0), self.camera)
