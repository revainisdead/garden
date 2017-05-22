import random

import pygame as pg

from .. import constants as c
from .. import setup


class Glaive(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.current_time = 0
        self.exists = True

        self.direction = c.Direction.LEFT
        self.max_move_distance = 120
        self.running_distance_total = 0

        self.animation_timer = 0
        self.animation_speed = 65


    def load_sprites_from_sheet(self):
        frames = []
        frames.append(self.get_image(68, 65, 16, 20))
        frames.append(self.get_image(68, 65, 16, 20))
        frames.append(self.get_image(32, 67, 21, 17))
        frames.append(self.get_image(54, 63, 12, 24))
        frames.append(self.get_image(8, 69, 24, 12))
        return frames


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*c.PROJECTILE_MULT), int(rect.height*c.PROJECTILE_MULT))
        image = pg.transform.scale(image, size_delta)
        return image


    def set_velocity(self):
        if self.direction == c.Direction.LEFT:
            move = -10
        elif self.direction == c.Direction.RIGHT:
            move = 10

        self.running_distance_total += move
        if not self.running_distance_total > self.max_move_distance:
            self.rect.x += move
        else:
            # Drawing is based on groups, if we remove the sprite
            # from all groups, it should also stop drawing it.
            self.kill()
            self.exists = False


    def handle_state(self):
        self.set_velocity()
        self.animate_glaive()


    def update(self, current_time):
        self.current_time = current_time

        if self.exists:
            self.handle_state()


    def animate_glaive(self):
        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.shooting_timer = self.current_time
        else:
            if self.current_time - self.shooting_timer > self.animation_speed:
                self.frame_index += 1

                if self.frame_index >= len(self.frames):
                    self.frame_index = 1
                self.shooting_timer = self.current_time

        self.image = self.frames[self.frame_index]


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.walking_speed = 4
        self.direction = c.Direction.UP
        self.set_velocity()
        self.walking_dir_change_interval = 0

        self.current_time = 0
        self.shooting_timer = 0
        self.animation_speed = 80


    def load_sprites_from_sheet(self):
        images = []
        # Duplicate first image, use first image as a placeholder
        # indicating that the animation hasn't ran yet
        images.append(self.get_image(57, 8, 34, 40))
        images.append(images[0])
        images.append(self.get_image(95, 8, 34, 40))
        images.append(self.get_image(135, 8, 34, 40))
        images.append(self.get_image(180, 8, 34, 40))
        # Reverse animation, close the enemy door.
        images.append(images[3])
        images.append(images[2])
        # Original image, door is closed.
        images.append(images[0])
        return images


    def set_velocity(self):
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



    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*c.ENEMY_MULT), int(rect.height*c.ENEMY_MULT))
        image = pg.transform.scale(image, size_delta)
        return image


    def auto_walk(self):
        self.walking_dir_change_interval += 1

        if self.walking_dir_change_interval == 10:
            direction = random.randint(0, 7)
            self.walking_dir_change_interval = 0

            for ea in c.Direction:
                if direction == ea.value:
                    self.direction = ea
                    self.set_velocity()

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def handle_state(self, glaive_group):
        # AI States
        # - Dead
        # - Attacking
        # - Etc

        # if state == SHOOT:
        self.animate_shoot(glaive_group)
        self.auto_walk()


    def update(self, current_time, glaive_group):
        self.current_time = current_time

        self.handle_state(glaive_group)


    def animate_shoot(self, glaive_group):
        if self.frame_index == 0:
            self.frame_index += 1

            # Setting shooting timer for the first time
            self.shooting_timer = self.current_time
        else:
            if self.current_time - self.shooting_timer > self.animation_speed:
                self.frame_index += 1

                # If the image is the shooting image, shoot glaive.
                if self.frame_index == 4:
                    self.shoot_glaive(glaive_group)

                if self.frame_index >= len(self.frames):
                    self.frame_index = 1
                self.shooting_timer = self.current_time

        self.image = self.frames[self.frame_index]


    def shoot_glaive(self, glaive_group):
        glaive = Glaive(self.rect.x, self.rect.y + self.rect.height/2)
        glaive_group.add(glaive)


