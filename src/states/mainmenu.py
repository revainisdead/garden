import pygame

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

        self.background_x_mult = c.DEFAULT_BACKGROUND_X_MULT
        self.background_y_mult = c.DEFAULT_BACKGROUND_Y_MULT
        self.menu_y = c.STARTING_MENU_Y

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
        self.re_setup_menu()


    def setup_background(self):
        self.background = setup.GFX["nature_mountain_background"]
        self.background_rect = self.background.get_rect()
        self.view = pygame.Rect((0, 0), (setup.screen_size.get_width(), setup.screen_size.get_height()))

        size_delta = (int(self.background_rect.width*self.background_x_mult), int(self.background_rect.height*self.background_y_mult))
        self.background = pygame.transform.scale(self.background, size_delta)


    def re_setup_menu(self):
        x = setup.screen_size.get_width()/2 - c.MENU_WIDTH/2
        y = self.menu_y
        menu_separation = c.MENU_SELECTION_OFFSET
        selection1 = user_interface.MenuSelection(x, y, "play")
        y += menu_separation
        selection2 = user_interface.MenuSelection(x, y, "load_game")
        y += menu_separation
        selection3 = user_interface.MenuSelection(x, y, "quit")

        # Create a list of the menu sprites, so ensure text gets
        # drawn after the sprite group gets drawn.
        self.menu_list = [
            selection1,
            selection2,
            selection3
        ]

        self.menu_group = pygame.sprite.Group(
                selection1,
                selection2,
                selection3)


    def set_next_state(self) -> c.MainState:
        return c.MainState.COMMONAREA


    def update(self, surface: pygame.Surface, current_time: float) -> None:
        """Update the state every frame"""
        self.update_sizes()

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


    def update_sizes(self) -> None:
        """Update sizes if screen size has changed."""
        if setup.screen_size.changed():
            self.re_setup_menu()
            self.background_x_mult = setup.screen_size.get_width() * c.BACKGROUND_X_SCALER
            self.background_y_mult = setup.screen_size.get_height() * c.BACKGROUND_Y_SCALER
            self.menu_y = int(setup.screen_size.get_height() / 3.5)

            self.view = pygame.Rect((0, 0), (setup.screen_size.get_width(), setup.screen_size.get_height()))

            size_delta = (int(self.background_rect.width*self.background_x_mult), int(self.background_rect.height*self.background_y_mult))
            self.background = pygame.transform.scale(self.background, size_delta)


    def update_sprites(self, selection: user_interface.MenuSelection) -> None:
        self.menu_group.update(selection)


    def blit_images(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0), self.view)

        self.menu_group.draw(surface)

        for menu_item in self.menu_list:
            menu_item.render_name(surface)
