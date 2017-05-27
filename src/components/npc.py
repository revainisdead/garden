from typing import List

import random

import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup
from .. import tools


directions = [
    c.Direction.UP,
    c.Direction.DOWN,
    c.Direction.LEFT,
    c.Direction.RIGHT,
]


class Npc(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.sprite_sheet = setup.GFX["hero"]
        self.frames = self.load_sprites_from_sheet()

        #self.frames = {
            #c.Direction.UP: self.load_up_sprites_from_sheet(),
            #c.Direction.DOWN: self.load_down_sprites_from_sheet(),
            #c.Direction.LEFT: self.load_left_sprites_from_sheet(),
            #c.Direction.RIGHT: self.load_right_sprites_from_sheet(),
        #}

        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walking_speed = c.speeds["npc"]
        self.direction = c.Direction.UP
        self.set_velocity()
        self.walking_dir_change_interval = 0

        self.current_time = 0
        self.walking_timer = 0
        self.animation_speed = 120


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(335, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(591, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(847, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        return images


    def set_velocity(self) -> None:
        """Set the speed based on the direction"""
        self.x_vel = 0
        self.y_vel = 0

        if self.direction == c.Direction.LEFT:
            self.x_vel = -self.walking_speed
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = self.walking_speed
        elif self.direction == c.Direction.UP:
            self.y_vel = -self.walking_speed
        elif self.direction == c.Direction.DOWN:
            self.y_vel = self.walking_speed


    def auto_walk(self) -> None:
        self.walking_dir_change_interval += 1

        if self.walking_dir_change_interval == 10:
            direction_index = random.randint(0, len(directions) - 1)
            self.walking_dir_change_interval = 0

            self.direction = directions[direction_index]
            self.set_velocity()

        self.rect = tools.fix_bounds(rect=self.rect, highest_x=c.MAP_WIDTH, highest_y=c.MAP_HEIGHT, x_vel=self.x_vel, y_vel=self.y_vel)


    def handle_state(self) -> None:
        self.animate_walk()
        self.auto_walk()


    def update(self, current_time) -> None:
        self.current_time = current_time

        self.handle_state()


    def animate_walk(self) -> None:
        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.walking_timer = self.current_time
        else:
            if self.current_time - self.walking_timer > self.animation_speed:
                self.frame_index += 1

                # If the image is the shooting image, shoot glaive.
                #if self.frame_index == 4:
                    #self.shoot_glaive(glaive_group)

                if self.frame_index >= len(self.frames):
                    self.frame_index = 1
                self.walking_timer = self.current_time

        self.image = self.frames[self.frame_index]


    #def shoot_glaive(self, glaive_group: pg.sprite.Group) -> None:
        #glaive = Glaive(self.rect.x, self.rect.y + self.rect.height/2)
        #glaive_group.add(glaive)
