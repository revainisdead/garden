from typing import List

import random

import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup
from .. import tools


class Glaive(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.dt = 0
        self.exists = True

        self.direction = c.Direction.LEFT
        self.max_move_distance = 120
        self.running_distance_total = 0

        self.animation_timer = 0
        self.animation_speed = 65


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        frames = []
        frames.append(helpers.get_image(68, 65, 16, 20, self.sprite_sheet, c.PROJECTILE_MULT, colorkey=c.PURPLE, transparent=False))
        frames.append(helpers.get_image(68, 65, 16, 20, self.sprite_sheet, c.PROJECTILE_MULT, colorkey=c.PURPLE, transparent=False))
        frames.append(helpers.get_image(32, 67, 21, 17, self.sprite_sheet, c.PROJECTILE_MULT, colorkey=c.PURPLE, transparent=False))
        frames.append(helpers.get_image(54, 63, 12, 24, self.sprite_sheet, c.PROJECTILE_MULT, colorkey=c.PURPLE, transparent=False))
        frames.append(helpers.get_image(8, 69, 24, 12, self.sprite_sheet, c.PROJECTILE_MULT, colorkey=c.PURPLE, transparent=False))
        return frames


    def set_velocity(self) -> None:
        if self.direction == c.Direction.LEFT:
            move = -c.speeds["projectile"]
        elif self.direction == c.Direction.RIGHT:
            move = c.speeds["projectile"]

        self.running_distance_total += move
        if not self.running_distance_total > self.max_move_distance:
            self.rect.x += move
        else:
            # Drawing is based on groups, if we remove the sprite
            # from all groups, it should also stop drawing it.
            self.kill()
            self.exists = False


    def handle_state(self) -> None:
        self.set_velocity()
        self.animate_glaive()


    def update(self, dt: float) -> None:
        self.dt = dt

        if self.exists:
            self.handle_state()


    def animate_glaive(self) -> None:
        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.shooting_timer = self.dt
        else:
            if self.dt - self.shooting_timer > self.animation_speed:
                self.frame_index += 1

                if self.frame_index >= len(self.frames):
                    self.frame_index = 1
                self.shooting_timer = self.dt

        self.image = self.frames[self.frame_index]


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walking_speed = c.speeds["enemy"]
        self.direction = c.Direction.UP
        self.set_velocity()
        self.walking_dir_change_interval = 0

        self.dt = 0
        self.shooting_timer = 0
        self.animation_speed = 80
        self.flip_speed = 400


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(57, 8, 34, 40, self.sprite_sheet, c.ENEMY_MULT, c.SAPPHIRE))
        images.append(images[0])
        images.append(helpers.get_image(95, 8, 34, 40, self.sprite_sheet, c.ENEMY_MULT, colorkey=c.SAPPHIRE))
        images.append(helpers.get_image(135, 8, 34, 40, self.sprite_sheet, c.ENEMY_MULT, colorkey=c.SAPPHIRE))
        images.append(helpers.get_image(180, 8, 34, 40, self.sprite_sheet, c.ENEMY_MULT, colorkey=c.SAPPHIRE))
        # Reverse animation, close the enemy door.
        images.append(images[3])
        images.append(images[2])
        # Original image, door is closed.
        images.append(images[0])
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


    def auto_walk(self) -> None:
        self.walking_dir_change_interval += 1

        if self.walking_dir_change_interval == 10:
            direction = random.randint(0, 7)
            self.walking_dir_change_interval = 0

            for ea in c.Direction:
                if direction == ea.value:
                    self.direction = ea
                    self.set_velocity()

        self.rect = tools.fix_bounds(rect=self.rect, highest_x=c.MAP_WIDTH, highest_y=c.MAP_HEIGHT, x_vel=self.x_vel, y_vel=self.y_vel)


    def handle_state(self, glaive_group: pg.sprite.Group) -> None:
        self.animate_shoot(glaive_group)
        self.auto_walk()


    def update(self, dt, glaive_group: pg.sprite.Group) -> None:
        self.dt = dt

        self.handle_state(glaive_group)


    def animate_shoot(self, glaive_group: pg.sprite.Group) -> None:
        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.shooting_timer = self.dt
        else:
            if self.dt - self.shooting_timer > self.animation_speed:
                self.frame_index += 1

                # If the image is the shooting image, shoot glaive.
                if self.frame_index == 4:
                    self.shoot_glaive(glaive_group)

                if self.frame_index >= len(self.frames):
                    self.frame_index = 1
                self.shooting_timer = self.dt

        self.image = self.frames[self.frame_index]


    def shoot_glaive(self, glaive_group: pg.sprite.Group) -> None:
        glaive = Glaive(self.rect.x, self.rect.y + self.rect.height/2)
        glaive_group.add(glaive)
