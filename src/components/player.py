import pygame as pg

from .. import setup
from .. import constants as c


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]

        self.image = self.get_image(14, 7, 35, 42)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = c.Direction.UP
        self.walking_speed = 6


    def set_velocity(self):
        # Before setting new velocity, reset to 0
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
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*1.5), int(rect.height*1.5))
        image = pg.transform.scale(image, size_delta)
        return image


    def walk(self):
        self.set_velocity()
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel


    def handle_state(self, keys) -> bool:
        if keys[c.binds["left"]]:
            if keys[c.binds["up"]]:
                self.direction = c.Direction.LEFTUP
            elif keys[c.binds["down"]]:
                self.direction = c.Direction.LEFTDOWN
            else:
                self.direction = c.Direction.LEFT
            self.walk()

        elif keys[c.binds["right"]]:
            if keys[c.binds["up"]]:
                self.direction = c.Direction.RIGHTUP
            elif keys[c.binds["down"]]:
                self.direction = c.Direction.RIGHTDOWN
            else:
                self.direction = c.Direction.RIGHT
            self.walk()

        elif keys[c.binds["up"]]:
            self.direction = c.Direction.UP
            self.walk()
        elif keys[c.binds["down"]]:
            self.direction = c.Direction.DOWN
            self.walk()
        elif keys[c.binds["escape"]]:
            self.quit = True


    def update(self, keys):
        self.handle_state(keys)
