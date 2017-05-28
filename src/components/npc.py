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
    c.Direction.NONE,
]


class Npc(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.sprite_sheet = setup.GFX["hero"]
        self.current_frames = self.load_up_sprites_from_sheet()

        self.frames_dict = {
            c.Direction.UP: self.load_up_sprites_from_sheet(),
            c.Direction.DOWN: self.load_down_sprites_from_sheet(),
            c.Direction.LEFT: self.load_left_sprites_from_sheet(),
            c.Direction.RIGHT: self.load_right_sprites_from_sheet(),
        }

        self.current_frames = self.load_up_sprites_from_sheet()
        self.frame_index = 0

        self.image = self.current_frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walking_speed = c.speeds["npc_roaming"]
        self.direction = c.Direction.UP
        self.previous_direction = c.Direction.UP
        self.set_velocity()

        self.walking_dir_change_counter = 0
        self.walking_dir_change_interval = None
        self.standing_still_interval = 40
        self.standing_still_direction_index = 4 # Index for c.Direction.NONE in direction

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

        if not self.direction == c.Direction.NONE:
            self.current_frames = self.frames_dict[self.direction]


    def pick_new_direction(self, ran_into_wall: bool=False) -> c.Direction:
        # Make c.Direction.NONE Much more likely to happen.
        increase_standing_still_chance = 7
        direction_chance = random.randint(0, increase_standing_still_chance)

        if direction_chance > len(directions) - 1:
            direction_index = self.standing_still_direction_index
        else:
            direction_index = direction_chance

        self.walking_dir_change_counter = 0
        self.walking_dir_change_interval = None

        # Save previous direction.
        self.previous_direction = self.direction

        direction_choice = directions[direction_index]
        if ran_into_wall and direction_choice == self.previous_direction:
            # When we run into a wall, go left.
            # Based on ability to always complete a maze if always going left,
            direction_choice = c.Direction.LEFT

        return direction_choice


    def auto_walk(self) -> None:
        if self.walking_dir_change_interval is None:
            if self.direction == c.Direction.NONE:
                self.walking_dir_change_interval = self.standing_still_interval
            else:
                self.walking_dir_change_interval = random.randint(c.FPS * 0.7, c.FPS)
        else:
            self.walking_dir_change_counter += 1

        if self.walking_dir_change_counter == self.walking_dir_change_interval:
            self.direction = self.pick_new_direction()

        old_rect = self.rect
        self.rect, hit_wall = tools.fix_bounds(rect=old_rect, highest_x=c.MAP_WIDTH, highest_y=c.MAP_HEIGHT, x_vel=self.x_vel, y_vel=self.y_vel)

        # If the rect's x and y are the same as they were before
        # but the direction is not NONE, then the bounds were fixed.
        # We can use this to not let the npc not continually run into things.
        #if old_rect.x == self.rect.x and old_rect.y == self.rect.y and self.direction != c.Direction.NONE:
        if hit_wall:
            self.direction = self.pick_new_direction(ran_into_wall=True)

        self.set_velocity()


    def handle_state(self) -> None:
        self.animate_walk()
        self.auto_walk()


    def update(self, current_time: float) -> None:
        self.current_time = current_time

        self.handle_state()


    def animate_walk(self) -> None:
        if self.direction == c.Direction.NONE:
            self.animation_speed = 0
        else:
            self.animation_speed = self.animation_speed_static

        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.walking_timer = self.current_time
        elif self.direction == c.Direction.NONE:
            # Select standing still images.
            if self.previous_direction == c.Direction.UP or self.previous_direction == c.Direction.DOWN:
                self.frame_index = 1
            elif self.previous_direction == c.Direction.LEFT or self.previous_direction == c.Direction.RIGHT:
                self.frame_index = 2
        else:
            if self.current_time - self.walking_timer > self.animation_speed:
                self.frame_index += 1

                # If the image is the shooting image, shoot glaive.
                #if self.frame_index == 4:
                    #self.shoot_glaive(glaive_group)

                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 1
                self.walking_timer = self.current_time

        self.image = self.current_frames[self.frame_index]


    #def shoot_glaive(self, glaive_group: pg.sprite.Group) -> None:
        #glaive = Glaive(self.rect.x, self.rect.y + self.rect.height/2)
        #glaive_group.add(glaive)
