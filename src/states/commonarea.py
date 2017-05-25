from typing import Any, Dict, Tuple

import time

import pygame as pg

from .. import binds
from .. import constants as c
from .. import setup

from .. components import enemy, player, tilemap
from .. tools import State


class CommonArea(State):
    def __init__(self) -> None:
        super().__init__()
        self.setup_map()


    def startup(self, game_info: Dict[str, Any]) -> None:
        self.game_info = game_info

        self.setup_enemies()
        self.setup_player()
        self.glaive_group = pg.sprite.Group()

        self.state = c.MainState.COMMONAREA

        self.direction = c.Direction.UP
        self.camera_speed = c.speeds["camera"]
        self.set_camera_velocity()


    def setup_map(self) -> None:
        self.tilemap = tilemap.Map()
        self.tilemap_rect = self.tilemap.map_surface.get_rect()
        self.entire_area = pg.Surface((self.tilemap_rect.width, self.tilemap_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        #self.camera = setup.SCREEN.get_rect(bottom=self.entire_area_rect.bottom)
        if not c.DEBUG_MAP:
            self.camera = pg.Rect((MAP_WIDTH/2, MAP_HEIGHT/2), (c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        else:
            self.camera = pg.Rect((0, 0), (self.entire_area_rect.w, self.entire_area_rect.h))


    def setup_enemies(self) -> None:
        enemy1 = enemy.Enemy(300, 300)
        enemy2 = enemy.Enemy(350, 350)

        self.enemy_group = pg.sprite.Group(enemy1, enemy2)


    def setup_player(self) -> None:
        self.player = player.Player(500, 400)

        self.player_group = pg.sprite.Group(self.player)


    def update(self, surface, keys, current_time) -> None:
        """Update the state every frame
        print(self.camera.x)
        print(self.camera.y)
        print(self.entire_area.get_width())
        print(self.entire_area.get_height())
        print(self.entire_area_rect.w)
        print(self.entire_area_rect.h)
        print(self.entire_area_rect.x)
        print(self.entire_area_rect.y)
        """
        self.game_info["current_time"] = current_time
        self.update_sprites(keys)
        self.handle_states(keys)
        self.blit_images(surface)


    def handle_states(self, keys: Tuple[int]) -> None:
        if keys[binds.keybinds["left"]]:
            if keys[binds.keybinds["up"]]:
                self.direction = c.Direction.LEFTUP
            elif keys[binds.keybinds["down"]]:
                self.direction = c.Direction.LEFTDOWN
            else:
                self.direction = c.Direction.LEFT
            self.move_camera()

        elif keys[binds.keybinds["right"]]:
            if keys[binds.keybinds["up"]]:
                self.direction = c.Direction.RIGHTUP
            elif keys[binds.keybinds["down"]]:
                self.direction = c.Direction.RIGHTDOWN
            else:
                self.direction = c.Direction.RIGHT
            self.move_camera()

        elif keys[binds.keybinds["up"]]:
            self.direction = c.Direction.UP
            self.move_camera()
        elif keys[binds.keybinds["down"]]:
            self.direction = c.Direction.DOWN
            self.move_camera()
        elif keys[binds.keybinds["escape"]]:
            self.quit = True


    def update_sprites(self, keys: Tuple[int]) -> None:
        self.enemy_group.update(self.game_info["current_time"], self.glaive_group)
        self.glaive_group.update(self.game_info["current_time"])

        self.player_group.update(keys)


    def move_camera(self) -> None:
        self.set_camera_velocity()
        self.camera.x += self.camera_x_vel
        self.camera.y += self.camera_y_vel


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

    def blit_images(self, surface) -> None:
        self.entire_area.blit(self.tilemap.map_surface, self.camera, self.camera)

        self.tilemap.update(self.entire_area)
        self.player_group.draw(self.entire_area)
        self.enemy_group.draw(self.entire_area)
        self.glaive_group.draw(self.entire_area)

        surface.blit(self.entire_area, (0, 0), self.camera)
