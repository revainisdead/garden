from typing import List, Optional

import random

import pygame as pg

from . import helpers, util

from .. import binds
from .. import constants as c
from .. import setup
from .. import tools


class Player(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.sprite_sheet = setup.GFX["hero"]
        self.current_frames = self.load_up_sprites_from_sheet()

        self.frames_dict = {
            c.Direction.UP: self.load_up_sprites_from_sheet(),
            c.Direction.DOWN: self.load_down_sprites_from_sheet(),
            c.Direction.LEFT: self.load_left_sprites_from_sheet(),
            c.Direction.RIGHT: self.load_right_sprites_from_sheet(),
            c.Direction.LEFTUP: self.load_left_sprites_from_sheet(),
            c.Direction.RIGHTUP: self.load_right_sprites_from_sheet(),
            c.Direction.LEFTDOWN: self.load_left_sprites_from_sheet(),
            c.Direction.RIGHTDOWN: self.load_right_sprites_from_sheet(),
        }

        self.current_frames = self.load_up_sprites_from_sheet()
        self.frame_index = 0

        self.image = self.current_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walking_speed = c.speeds["player"]
        self.direction = c.Direction.NONE
        self.previous_direction = c.Direction.NONE
        self.x_vel = 0
        self.y_vel = 0

        self.current_time = 0
        self.walking_timer = 0
        self.animation_speed_static = 120


    def load_up_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(79, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(79, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(335, 283, 98, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(591, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(847, 283, 98, 198, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_down_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(335, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(591, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(847, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_left_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(67, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(67, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(323, 535, 106, 194, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(579, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(835, 535, 106, 194, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_right_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(83, 791, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(83, 791, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(339, 791, 106, 194, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(595, 791, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(851, 791, 106, 194, self.sprite_sheet, c.NPC_MULT))
        return images


    def set_velocity(self) -> None:
        """Set the speed based on the direction"""
        if self.direction == c.Direction.LEFT:
            self.x_vel = -self.walking_speed
            self.y_vel = 0
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = self.walking_speed
            self.y_vel = 0
        elif self.direction == c.Direction.UP:
            self.x_vel = 0
            self.y_vel = -self.walking_speed
        elif self.direction == c.Direction.DOWN:
            self.x_vel = 0
            self.y_vel = self.walking_speed
        elif self.direction == c.Direction.LEFTUP:
            self.x_vel = -self.walking_speed
            self.y_vel = -self.walking_speed
        elif self.direction == c.Direction.LEFTDOWN:
            self.x_vel = -self.walking_speed
            self.y_vel = self.walking_speed
        elif self.direction == c.Direction.RIGHTUP:
            self.x_vel = self.walking_speed
            self.y_vel = -self.walking_speed
        elif self.direction == c.Direction.RIGHTDOWN:
            self.x_vel = self.walking_speed
            self.y_vel = self.walking_speed
        else:
            self.x_vel = 0
            self.y_vel = 0


    def walk(self) -> None:
        # The camera and the hero should set the velocity
        # at the same time, so that they are in sync.

        if binds.INPUT.held("left"):
            if binds.INPUT.held("up"):
                self.direction = c.Direction.LEFTUP
            elif binds.INPUT.held("down"):
                self.direction = c.Direction.LEFTDOWN
            else:
                self.direction = c.Direction.LEFT

        elif binds.INPUT.held("right"):
            if binds.INPUT.held("up"):
                self.direction = c.Direction.RIGHTUP
            elif binds.INPUT.held("down"):
                self.direction = c.Direction.RIGHTDOWN
            else:
                self.direction = c.Direction.RIGHT

        elif binds.INPUT.held("up"):
            self.direction = c.Direction.UP
        elif binds.INPUT.held("down"):
            self.direction = c.Direction.DOWN
        else:
            self.direction = c.Direction.NONE
        self.set_velocity()


        new_x, new_y = tools.fix_bounds(rect=self.rect, highest_x=c.MAP_WIDTH, highest_y=c.MAP_HEIGHT, x_vel=self.x_vel, y_vel=self.y_vel)

        self.rect.x = new_x
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_x_collisions(collided)

        self.rect.y = new_y
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_y_collisions(collided)

        #hit_wall = tools.test_collide(rect=self.rect, x_vel=self.x_vel, y_vel=self.y_vel, collidables=collidables)


    def check_x_collisions(self, collided: pg.sprite.Sprite) -> None:
        if self.rect.x < collided.rect.x:
            self.rect.right = collided.rect.left
        #elif self.rect.x > collided.rect.x:
        else:
            self.rect.left = collided.rect.right
        self.x_vel = 0


    def check_y_collisions(self, collided: pg.sprite.Sprite) -> None:
        if self.rect.y > collided.rect.y:
            self.rect.y = collided.rect.bottom
        #elif self.rect.y < collided.rect.y
        else:
            self.rect.bottom = collided.rect.top
        self.y_vel = 0


    def get_closest_collisions(self) -> Optional[pg.sprite.Sprite]:
        # XXX Check for the collidable that is the closest to the player's
        # center.
        return pg.sprite.spritecollideany(self, self.collidable_group)


    def handle_state(self) -> None:
        # Let walking handle input.
        # XXX Later if the player has a certain state, such as set to worker
        # mode, when I can change the worker to auto_walking, pathfinding,
        # searching for tree, etc etc. Right now he's just walking...
        self.walk()


    def update(self, current_time: float, collidable_group: pg.sprite.Group) -> None:
        self.current_time = current_time
        self.collidable_group = collidable_group

        self.handle_state()
        self.animate_walk()


    def animate_walk(self) -> None:
        if not self.direction == c.Direction.NONE:
            # If the sprite is moving, set the animation frames based on direction.
            self.current_frames = self.frames_dict[self.direction]

        if self.direction == c.Direction.NONE:
            self.animation_speed = 0
        else:
            self.animation_speed = self.animation_speed_static

        if self.frame_index == 0:
            self.frame_index += 1

            # Setting timer for the first time
            self.walking_timer = self.current_time
        elif self.direction == c.Direction.NONE:
            # Select standing still images.
            if self.previous_direction == c.Direction.UP or self.previous_direction == c.Direction.DOWN:
                self.frame_index = 1
            elif self.previous_direction == c.Direction.LEFT \
                    or self.previous_direction == c.Direction.RIGHT \
                    or self.previous_direction == c.Direction.LEFTUP \
                    or self.previous_direction == c.Direction.RIGHTUP \
                    or self.previous_direction == c.Direction.LEFTDOWN \
                    or self.previous_direction == c.Direction.RIGHTDOWN:
                self.frame_index = 2
        else:
            if self.current_time - self.walking_timer > self.animation_speed:
                self.frame_index += 1

                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 1
                self.walking_timer = self.current_time

        self.image = self.current_frames[self.frame_index]
