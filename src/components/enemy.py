import pygame as pg

from .. import setup
from .. import constants as c


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = setup.GFX["enemies_by_o_fiveasone_o_88"]
        self.image = self.get_image(180, 8, 34, 40)

        # Get image's rect
        self.rect = self.image.get_rect()

        # Set rect's position
        self.rect.x = x
        self.rect.y = y

        self.direction = c.Direction.UP
        self.set_velocity()


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
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*1.75), int(rect.height*1.75))
        image = pg.transform.scale(image, size_delta)

        return image


    def autowalk(self):
        pass


    def handle_state(self):
        pass


    def update(self):
        pass
