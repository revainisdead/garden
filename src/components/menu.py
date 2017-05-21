import pygame as pg

from .. import constants as c
from .. import setup


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()

        self.sprite = setup.GFX["green_button00"]
        self.sprite_overlay = setup.GFX["green_button13"]

        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = name
        self.selected = False


    def load_sprites_from_sheet(self):
        images = []
        images.append(self.get_image(0, 0, 190, 49, self.sprite))
        images.append(self.get_image(0, 0, 190, 49, self.sprite_overlay))
        return images


    def get_image(self, x, y, width, height, sprite):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(sprite, (0, 0), (x, y, width, height))
        image.set_colorkey(c.SAPPHIRE)

        size_delta = (int(rect.width*c.UI_MULT), int(rect.height*c.UI_MULT))
        image = pg.transform.scale(image, size_delta)
        return image


    def update(self, selection):
        self.handle_state(selection)


    def handle_state(self, selection):
        if selection == self.name:
            self.selected = True
            frame_index = 1
        else:
            self.selected = False
            frame_index = 0
