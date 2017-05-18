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
        self.x_vel = 0
        self.y_vel = 0


    def set_velocity(self):
        if self.direction == c.Direction.LEFT:
            self.x_vel = -2
        elif self.direction == c.Direction.RIGHT:
            self.x_vel = 2
        elif self.direction == c.Direction.UP:
            self.y_vel = -2
        elif self.direction == c.Direction.DOWN:
            self.y_vel = 2


    def get_image(self, x, y, width, height):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*1.75), int(rect.height*1.75))
        image = pg.transform.scale(image, size_delta)
        return image


    def walk(self):
        self.set_velocity()
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel


    def handle_state(self, keys):
        if keys[c.binds["left"]]:
            self.direction = c.Direction.LEFT
            self.walk()
        elif keys[c.binds["right"]]:
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
