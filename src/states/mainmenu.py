import pygame as pg

from .. import constants as c
from .. import setup

from .. tools import State


class MainMenu(State):
    def __init__(self):
        super().__init__()

        self.startup()


    def startup(self):
        """Called each time the state is entered"""
        self.next = self.set_next_state()

        self.setup_background()


    def setup_background(self):
        self.background = setup.GFX["tile_map_silver"]
        self.background_rect = self.background.get_rect()

        width = self.background_rect.width
        height = self.background_rect.height

        self.entire_area = pg.Surface((width, height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)


    def set_next_state(self):
        return c.States.COMMONAREA


    def update(self, surface, keys):
        """Update the state every frame"""
        self.handle_update(keys)

        surface.blit(self.background, self.viewport, self.viewport)


    def handle_update(self, keys):
        if keys[c.binds["enter"]]:
            self.state_done = True
