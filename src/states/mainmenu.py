import pygame as pg

from .. import constants as c
from .. import setup

from .. tools import State


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.setup_background()

    def startup(self):
        pass

    def setup_background(self):
        self.background = setup.GFX["level_1"]
        self.background_rect = self.background.get_rect()

        width = self.background_rect.width
        height = self.background_rect.height

        self.entire_area = pg.Surface((width, height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()


    def next_state(self):
        return c.States.MAINMENU


    def update(self, surface, keys):
        """Update the state every frame"""
        self.surface = surface

        self.handle_update(keys)
        self.blit_images(surface)


    def handle_update(self, keys):
        if keys[c.binds["enter"]]:
            self.state_done = True


    def blit_images(self, surface):
        self.entire_area.blit(self.background, (0, 0), (0, 0))
        surface.blit(self.entire_area, (0, 0), (0, 0))
