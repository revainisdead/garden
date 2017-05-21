import pygame as pg

from .. import constants as c
from .. import binds
from .. import setup

from .. components import menu
from .. tools import State


class MainMenu(State):
    def __init__(self):
        super().__init__()
        self.startup()

        self.options = {
            "play": 0,
            "load_game": 0,
            "exit": 0,
        }

        self.selection = "play"


    def startup(self):
        """Called each time the state is entered"""
        self.next = self.set_next_state()
        self.setup_background()
        self.setup_menu()


    def setup_background(self):
        self.background = setup.GFX["cloud_background"]
        self.background_rect = self.background.get_rect()

        size_delta = (int(self.background_rect.width*c.BACKGROUND_MULT), int(self.background_rect.height*c.BACKGROUND_MULT))
        self.background = pg.transform.scale(self.background, size_delta)

        self.entire_area = pg.Surface((self.background_rect.width, self.background_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)


    def setup_menu(self):
        menu_height = 200
        menu_separation = 40
        #selection1 = menu.MenuSelection(self.entire_area_rect.width/2, menu_height, "play")
        selection1 = menu.MenuSelection(200, 200, "play")
        menu_height += menu_separation
        selection2 = menu.MenuSelection(self.entire_area_rect.width/2, menu_height, "load_game")
        menu_height += menu_separation
        selection3 = menu.MenuSelection(self.entire_area_rect.width/2, menu_height, "exit")

        self.menu_group = pg.sprite.Group(
                selection1,
                selection2,
                selection3)


    def set_next_state(self):
        return c.MainState.COMMONAREA


    def update(self, surface, keys, current_time):
        """Update the state every frame"""
        self.update_sprites(self.selection)
        self.handle_states(keys)
        self.blit_images(surface)


    def handle_states(self, keys):
        if keys[binds.keybinds["enter"]]:
            if self.selection == "play":
                self.state_done = True
            elif self.selection == "load_game":
                # Load a saved json file into game_info
                pass
            elif self.selection == "exit":
                self.quit = True
        elif keys[binds.keybinds["up"]] or keys[binds.keybinds["arrow_up"]]:
            pass # Move selection up
        elif keys[binds.keybinds["down"]] or keys[binds.keybinds["arrow_down"]]:
            pass # Move select down
        elif keys[binds.keybinds["escape"]]:
            self.quit = True


    def update_sprites(self, selection):
        self.menu_group.update(selection)


    def blit_images(self, surface):
        surface.blit(self.background, self.viewport, self.viewport)
        self.menu_group.draw(self.entire_area)
