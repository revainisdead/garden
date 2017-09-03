from typing import List, Optional

import random

import pygame

from . import helpers

from .. import binds
from .. import constants as c
from .. import phys
from .. import setup
from .. import tools


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
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

        self.vel = c.speeds["player"] * c.FPS

        self.direction = c.Direction.NONE
        self.previous_direction = c.Direction.NONE
        self.x_vel = 0
        self.y_vel = 0

        self.dt = 0
        self.walking_timer = 0
        self.animation_speed_static = 120


    def load_up_sprites_from_sheet(self) -> List[pygame.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(79, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(79, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(335, 283, 98, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(591, 283, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(847, 283, 98, 198, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_down_sprites_from_sheet(self) -> List[pygame.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(79, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(335, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(591, 27, 98, 202, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(847, 27, 98, 198, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_left_sprites_from_sheet(self) -> List[pygame.Surface]:
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(helpers.get_image(67, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(67, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(323, 535, 106, 194, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(579, 535, 106, 198, self.sprite_sheet, c.NPC_MULT))
        images.append(helpers.get_image(835, 535, 106, 194, self.sprite_sheet, c.NPC_MULT))
        return images


    def load_right_sprites_from_sheet(self) -> List[pygame.Surface]:
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
        # Convert dt to seconds (milliseconds / 1000)
        dt_s = self.dt / 1000
        self.walk_sp = round(self.vel * dt_s)
        self.diag_sp = round(phys.normalize(self.vel, self.vel) * dt_s)

        if self.direction == c.Direction.LEFT:
            self.x_vel = -self.walk_sp
            self.y_vel = 0
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = self.walk_sp
            self.y_vel = 0
        elif self.direction == c.Direction.UP:
            self.x_vel = 0
            self.y_vel = -self.walk_sp
        elif self.direction == c.Direction.DOWN:
            self.x_vel = 0
            self.y_vel = self.walk_sp
        elif self.direction == c.Direction.LEFTUP:
            self.x_vel = -self.diag_sp
            self.y_vel = -self.diag_sp
        elif self.direction == c.Direction.LEFTDOWN:
            self.x_vel = -self.diag_sp
            self.y_vel = self.diag_sp
        elif self.direction == c.Direction.RIGHTUP:
            self.x_vel = self.diag_sp
            self.y_vel = -self.diag_sp
        elif self.direction == c.Direction.RIGHTDOWN:
            self.x_vel = self.diag_sp
            self.y_vel = self.diag_sp
        else:
            self.x_vel = 0
            self.y_vel = 0


    def walk(self, inp: binds.Input) -> None:
        self.previous_direction = self.direction

        if inp.held("move_left"):
            if inp.held("move_up"):
                self.direction = c.Direction.LEFTUP
            elif inp.held("move_down"):
                self.direction = c.Direction.LEFTDOWN
            else:
                self.direction = c.Direction.LEFT

        elif inp.held("move_right"):
            if inp.held("move_up"):
                self.direction = c.Direction.RIGHTUP
            elif inp.held("move_down"):
                self.direction = c.Direction.RIGHTDOWN
            else:
                self.direction = c.Direction.RIGHT

        elif inp.held("move_up"):
            self.direction = c.Direction.UP
        elif inp.held("move_down"):
            self.direction = c.Direction.DOWN
        else:
            self.direction = c.Direction.NONE
        self.set_velocity()


        new_x, new_y = tools.fix_edge_bounds(rect=self.rect, highest_x=setup.map_size.get_width(), highest_y=setup.map_size.get_height(), x_vel=self.x_vel, y_vel=self.y_vel)

        self.rect.x = new_x
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_x_collisions(collided)

        self.rect.y = new_y
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_y_collisions(collided)


    def check_x_collisions(self, collided: pygame.rect.Rect) -> None:
        if self.rect.x < collided.x:
            self.rect.right = collided.left
        elif self.rect.x > collided.x:
            self.rect.left = collided.right
        self.x_vel = 0


    def check_y_collisions(self, collided: pygame.rect.Rect) -> None:
        if self.rect.y > collided.y:
            self.rect.y = collided.bottom
        elif self.rect.y < collided.y:
            self.rect.bottom = collided.top
        self.y_vel = 0


    def get_closest_collisions(self) -> Optional[pygame.rect.Rect]:
        """
        # XXX Later check for the collidable that is the closest to the player's
        # center.
        Inefficient method: return pygame.sprite.spritecollideany(self, self.collidable_group)
        """
        # Find the tiles around the current tile. Loop through (-1, 0, 1).
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                try:
                    x = self.rect.x
                    y = self.rect.y
                    ts = c.TILE_SIZE

                    # Get the nearest grid point. Truncate to the nearest
                    # multiple of 64 (Eg. 130 - 130 % 64 => 128 / 64 => 2)
                    grid_x = int((self.rect.x - (self.rect.x % ts)) / ts)
                    grid_y = int((self.rect.y - (self.rect.y % ts)) / ts)

                    if self.collidable_grid[grid_x + i][grid_y + j] > 0:
                        # Expand grid_x and grid_y  back into normal
                        # coords (*64), then add the current i and j.
                        rect = pygame.rect.Rect((grid_x*64 + i*ts, grid_y*64 + j*ts), (c.TILE_SIZE, c.TILE_SIZE))
                        if self.rect.colliderect(rect):
                            return rect
                except IndexError:
                    pass


    def handle_state(self, inp: binds.Input) -> None:
        # Let walking handle input.
        # XXX Later if the player has a certain state, such as set to worker
        # mode, when I can change the worker to auto_walking, pathfinding,
        # searching for tree, etc etc. Right now he's just walking...
        self.walk(inp)

        #if self.state == "sliding":
        #   don't allow user input
        #   and slide in that x or y direction until a wall is hit.


    def update(self, dt: int, game_time: int, collidable_grid: List[List[int]], inp: binds.Input) -> None:
        self.dt = dt
        self.collidable_grid = collidable_grid

        self.handle_state(inp)
        self.animate_walk(game_time)


    def animate_walk(self, game_time: int) -> None:
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
            self.walking_timer = game_time
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
            if game_time - self.walking_timer > self.animation_speed:
                self.frame_index += 1

                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 1
                self.walking_timer = game_time

        self.image = self.current_frames[self.frame_index]
