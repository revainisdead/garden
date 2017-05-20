import random

import pygame as pg

from .. import setup
from .. import constants as c


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.frames = self.load_images_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Get image's rect
        self.rect = self.image.get_rect()

        # Set rect's position
        self.rect.x = x
        self.rect.y = y

        self.direction = c.Direction.UP
        self.set_velocity()

        self.change_interval = 0


    def load_images_from_sheet(self):
        images = []

        images.append(self.get_image(57, 8, 34, 40))
        images.append(self.get_image(95, 8, 34, 40))
        images.append(self.get_image(135, 8, 34, 40))
        images.append(self.get_image(180, 8, 34, 40))

        return images


    def set_velocity(self):
        """
        if self.direction == c.Direction.LEFT:
            self.x_vel = -2
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = 2
        elif self.direction == c.Direction.UP:
            self.y_vel = -2
        elif self.direction == c.Direction.DOWN:
            self.y_vel = 2
        """
        self.x_vel = 0
        self.y_vel = 0

        if self.direction == c.Direction.LEFT:
            self.x_vel = -2
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = 2
        elif self.direction == c.Direction.UP:
            self.y_vel = -2
        elif self.direction == c.Direction.DOWN:
            self.y_vel = 2
        elif self.direction == c.Direction.LEFTUP:
            self.x_vel = -2
            self.y_vel = -2
        elif self.direction == c.Direction.LEFTDOWN:
            self.x_vel = -2
            self.y_vel = 2
        elif self.direction == c.Direction.RIGHTUP:
            self.x_vel = 2
            self.y_vel = -2
        elif self.direction == c.Direction.RIGHTDOWN:
            self.x_vel = 2
            self.y_vel = 2



    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*1.5), int(rect.height*1.5))
        image = pg.transform.scale(image, size_delta)

        return image


    def auto_walk(self):
        self.change_interval += 1

        if self.change_interval == 10:
            direction = random.randint(0, 7)
            self.change_interval = 0

            for ea in c.Direction:
                if direction == ea.value:
                    self.direction = ea
                    self.set_velocity()

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def handle_state(self):
        # AI States
        # - Dead
        # - Attacking        # Increment first, then check if out of range.
        # - Etc
        self.auto_walk()


    def update(self):
        self.handle_state()
        self.animate_door()


    def animate_door(self):
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[self.frame_index]


    def full_animation(self):
        # Can work if based on time
        #for i in len(self.frames):
            #self.image[i]
        pass
