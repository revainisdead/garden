import pygame as pg

from .. import constants as c
from .. import binds
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
        self.background = setup.GFX["cloud_background"]
        self.background_rect = self.background.get_rect()

        size_delta = (int(self.background_rect.width*c.BACKGROUND_MULT), int(self.background_rect.height*c.BACKGROUND_MULT))
        self.background = pg.transform.scale(self.background, size_delta)

        self.entire_area = pg.Surface((self.background_rect.width, self.background_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)


    def set_next_state(self):
        return c.MainState.COMMONAREA


    def update(self, surface, keys, current_time):
        """Update the state every frame"""
        self.handle_update(keys)

        surface.blit(self.background, self.viewport, self.viewport)


    def handle_update(self, keys):
        if keys[binds.keybinds["enter"]]:
            self.state_done = True
        if keys[binds.keybinds["escape"]]:
            self.quit = True
