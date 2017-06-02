import pygame as pg

from .. import constants as c
from .. import control
from .. import binds
from .. import setup
from .. components import user_interface


class MainMenu(control.State):
    def __init__(self):
        super().__init__()
        self.game_info = {
            "current_time": 0,
        }

        self.startup(self.game_info)

        self.options = ["play", "load_game", "quit"]
        self.selection = "play"
        self.allow_input = True


    def startup(self, game_info):
        """Called each time the state is entered

        Currently takes in game_info so that the main menu can
        flipped back to from the main game."""
        self.game_info = game_info
        self.next = self.set_next_state()
        self.setup_background()
        self.setup_menu()


    def setup_background(self):
        self.background = setup.GFX["nature_mountain_background"]
        self.background_rect = self.background.get_rect()

        size_delta = (int(self.background_rect.width*c.BACKGROUND_MULT), int(self.background_rect.height*c.BACKGROUND_MULT))
        self.background = pg.transform.scale(self.background, size_delta)


    def setup_menu(self):
        menu_height = c.MENU_Y
        menu_separation = c.MENU_SELECTION_OFFSET
        selection1 = user_interface.MenuSelection(c.SCREEN_WIDTH/2, menu_height, "play")
        menu_height += menu_separation
        selection2 = user_interface.MenuSelection(c.SCREEN_WIDTH/2, menu_height, "load_game")
        menu_height += menu_separation
        selection3 = user_interface.MenuSelection(c.SCREEN_WIDTH/2, menu_height, "quit")

        # Create a list of the menu sprites, so ensure text gets
        # drawn after the sprite group gets drawn.
        self.menu_list = [
            selection1,
            selection2,
            selection3
        ]

        self.menu_group = pg.sprite.Group(
                selection1,
                selection2,
                selection3)


    def set_next_state(self) -> c.MainState:
        return c.MainState.COMMONAREA


    def update(self, surface: pg.Surface, current_time: float) -> None:
        """Update the state every frame"""
        self.update_sprites(self.selection)
        self.handle_states()
        self.blit_images(surface)


    def handle_states(self):
        if binds.INPUT.pressed("enter"):
            if self.selection == "play":
                self.state_done = True
            elif self.selection == "load_game":
                # Load a saved json file into game_info
                pass
            elif self.selection == "quit":
                self.quit = True
        elif binds.INPUT.pressed("up"):
            index = self.options.index(self.selection)
            if index == 0:
                pass # Don't exceed the beginning of the list
            else:
                index -= 1
                self.selection = self.options[index]
            self.allow_input = False
        elif binds.INPUT.pressed("down"):
            index = self.options.index(self.selection)
            if index == len(self.options) - 1:
                pass # Don't exceed the end of the list
            else:
                index += 1
                self.selection = self.options[index]
            self.allow_input = False


    def update_sprites(self, selection):
        self.menu_group.update(selection)


    def blit_images(self, surface):
        surface.blit(self.background, (0, 0))

        self.menu_group.draw(surface)

        for menu_item in self.menu_list:
            menu_item.render_name(surface)
