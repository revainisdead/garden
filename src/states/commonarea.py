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

        #self.setup_enemies()
        self.npc_group = self.setup_npcs()
        self.setup_player()
        #self.glaive_group = pg.sprite.Group()

        self.state = c.MainState.COMMONAREA

        self.direction = c.Direction.DOWN
        self.camera_speed = c.speeds["camera"]
        self.set_camera_velocity()


    def setup_map(self) -> None:
        self.tilemap = tilemap.Map()
        self.collidables = self.tilemap.create_collidables()
        self.tilemap_rect = self.tilemap.map_surface.get_rect()
        self.entire_area = pg.Surface((self.tilemap_rect.width, self.tilemap_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        #self.camera = setup.SCREEN.get_rect(bottom=self.entire_area_rect.bottom)
        if not c.DEBUG_MAP:
            # XXX Can adjust the starting area later.
            # For now just start the camera at 0, 0
            #self.camera = pg.Rect((c.MAP_WIDTH/2, c.MAP_HEIGHT/2), (c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
            self.camera = pg.Rect((0, 0), (c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        else:
            self.camera = pg.Rect((0, 0), (self.entire_area_rect.w, self.entire_area_rect.h))


    def setup_npcs(self) -> pg.sprite.Group:
        npcs = [] # type: List[non_player_controlled.Npc]
        npc_group = pg.sprite.Group()

        # min_npc_amount
        # max_npc_amount
        random_npcs_limit = random.randint(c.MIN_NPC_AMOUNT, c.MAX_NPC_AMOUNT)

        for _ in range(random_npcs_limit):
            x, y = self.tilemap.find_random_open_location()
            npc_group.add(non_player_controlled.Npc(x * c.TILE_SIZE, y * c.TILE_SIZE))

        return npc_group


    def setup_enemies(self) -> None:
        #enemy1 = enemy.Enemy(300, 300)
        #enemy2 = enemy.Enemy(350, 350)
        #enemy3 = enemy.Enemy(500, 500)
        #enemy4 = enemy.Enemy(600, 800)
        #enemy5 = enemy.Enemy(800, 400)
        #enemy6 = enemy.Enemy(400, 800)
        #self.enemy_group = pg.sprite.Group(
                #enemy1, enemy2, enemy3,
                #enemy4, enemy5, enemy6
                #)
        pass


    def setup_player(self) -> None:
        # Is also going to need to find_open_location method
        # But should the player's location be random? Maybe, go find your farm!
        #self.player = player.Player(500, 400)
        #self.player_group = pg.sprite.Group(self.player)
        pass


    def update(self, surface: pg.Surface, current_time: float) -> None:
        """Update the state every frame"""
        self.game_info["current_time"] = current_time

        self.update_sprites()
        self.handle_states()
        self.blit_images(surface)


    def handle_states(self) -> None:
        if binds.INPUT.held("left"):
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
        elif binds.INPUT.held("escape"):
            self.quit = True


    def update_sprites(self) -> None:
        #self.enemy_group.update(self.game_info["current_time"], self.glaive_group)
        #self.glaive_group.update(self.game_info["current_time"])

        #self.player_group.update()
        self.npc_group.update(self.game_info["current_time"], self.collidables)


    def move_camera(self) -> None:
        self.set_camera_velocity()

        tools.fix_bounds(rect=self.camera, highest_x=self.tilemap_rect.right, highest_y=self.tilemap_rect.bottom, x_vel=self.camera_x_vel, y_vel=self.camera_y_vel)


    def set_camera_velocity(self) -> None:
        # Before setting new velocity, reset to 0
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


    def blit_images(self, surface: pg.Surface) -> None:
        # This is responsible for showing only a certain area
        # of the tilemap surface, the area shown is the area of the camera.
        self.entire_area.blit(self.tilemap.map_surface, self.camera, self.camera)

        self.tilemap.update(self.entire_area, self.camera)
        #self.player_group.draw(self.entire_area)
        #self.enemy_group.draw(self.entire_area)
        self.npc_group.draw(self.entire_area)

        # Put things here that should be drawn over npcs
        self.tilemap.tree_top_group.draw(self.entire_area)

        #self.glaive_group.draw(self.entire_area)

        # Finally, draw everything to the screen surface.
        surface.blit(self.entire_area, (0, 0), self.camera)
