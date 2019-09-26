from typing import List, Optional

import random

import pygame

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

opposite_directions = {
    c.Direction.UP: c.Direction.DOWN,
    c.Direction.DOWN: c.Direction.UP,
    c.Direction.LEFT: c.Direction.RIGHT,
    c.Direction.RIGHT: c.Direction.LEFT,
}


class Npc(pygame.sprite.Sprite):
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
        self.walking_dir_change_interval = None # type: int
        self.standing_still_direction_index = 4 # Index for c.Direction.NONE in direction

        # Affect standing still frequency.
        self.standing_still_interval = 20
        # For every one added, double the standing still chance.
        self.increase_standing_still_chance = len(directions) + 1

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
        direction_chance = random.randint(0, self.increase_standing_still_chance)

        if direction_chance > len(directions) - 1:
            direction_index = self.standing_still_direction_index
        else:
            direction_index = direction_chance

        self.walking_dir_change_counter = 0
        self.walking_dir_change_interval = None # type: int

        # Save previous direction.
        self.previous_direction = self.direction

        direction_choice = directions[direction_index]
        if ran_into_wall and direction_choice == self.previous_direction:
            # When we run into a wall, go left.
            # Based on ability to always complete a maze if always going left
            if direction_choice is not c.Direction.NONE:
                direction_choice = opposite_directions[direction_choice]

        return direction_choice


    def auto_walk(self) -> None:
        interval_change_sec_min = c.FPS * 1
        interval_change_sec_max = c.FPS * 2
        self.set_velocity()

        if self.walking_dir_change_interval is None:
            if self.direction == c.Direction.NONE:
                self.walking_dir_change_interval = self.standing_still_interval
            else:
                self.walking_dir_change_interval = random.randint(interval_change_sec_min, interval_change_sec_max)
        else:
            self.walking_dir_change_counter += 1

        if self.walking_dir_change_counter == self.walking_dir_change_interval:
            self.direction = self.pick_new_direction()

        new_x, new_y = tools.fix_edge_bounds(rect=self.rect, highest_x=setup.map_size.get_width(), highest_y=setup.map_size.get_height(), x_vel=self.x_vel, y_vel=self.y_vel)

        hit_edge = False
        if new_x == self.rect.x and new_y == self.rect.y:
            # If the rect hasn't moved when checking for end of map
            # bounds, then it hit the end of the map. Save for later.
            hit_edge = True

        hit_wall = False

        # Set and then correct x and y one at a time.
        self.rect.x = new_x
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_x_collisions(collided)
            hit_wall = True

        self.rect.y = new_y
        collided = self.get_closest_collisions()
        if collided is not None:
            self.check_y_collisions(collided)
            hit_wall = True

        #hit_wall = tools.test_collide(sprite=self, x_vel=self.x_vel, y_vel=self.y_vel, collidable_group=self.collidable_grid)

        if hit_edge or hit_wall:
            # If the end of the map prevented the npc from moving,
            # pick a new direction. Don't let npcs run into walls...
            self.direction = self.pick_new_direction(ran_into_wall=True)


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


    def handle_state(self, game_time: int) -> None:
        self.animate_walk(game_time)

        # XXX Rework. Player should inherit from npc.
        self.auto_walk()


    def update(self, dt: int, game_time: int, collidable_grid: List[List[int]]) -> None:
        self.dt = dt
        self.collidable_grid = collidable_grid

        self.handle_state(game_time)


    def animate_walk(self, game_time: int) -> None:
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
            elif self.previous_direction == c.Direction.LEFT or self.previous_direction == c.Direction.RIGHT:
                self.frame_index = 2
        else:
            if game_time - self.walking_timer > self.animation_speed:
                self.frame_index += 1

                if self.frame_index >= len(self.current_frames):
                    self.frame_index = 1
                self.walking_timer = game_time

        self.image = self.current_frames[self.frame_index]


class Worm: pass
class Bat: pass
