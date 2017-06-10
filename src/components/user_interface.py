from typing import Any, Dict, List, Tuple

from collections import OrderedDict
from datetime import datetime
import time

import pygame as pg

from . import helpers

from .. import binds
from .. import constants as c
from .. import setup
from .. import tools


menu_labels = {
    "play": "play",
    "load_game": "load game",
    "quit": "quit",
}


button_binds = {
    "wood_axe_icon": "one",
    "tree_icon": "two",
}


button_icon_color = OrderedDict([
    ("wood_axe_icon", c.DARK_PALE),
    ("tree_icon", c.FOREST_GREEN),
])


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name) -> None:
        super().__init__()

        self.sprite = setup.GFX["green_button01"]
        self.sprite_selected = setup.GFX["green_button00"]
        self.font = setup.FONTS["menu_kenvector_future_thin"]

        self.frames = self.load_sprites_from_sheet()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.state = c.Switch.OFF
        self.name = name
        self.selected = False


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite, mult=c.MENU_MULT))
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite_selected, mult=c.MENU_MULT))
        return frames


    def update(self, selection) -> None:
        self.handle_state(selection)


    def handle_state(self, selection) -> None:
        if selection == self.name:
            self.selected = True
            frame_index = 1
            self.image = self.frames[frame_index]
        else:
            self.selected = False
            frame_index = 0
            self.image = self.frames[frame_index]


    def render_name(self, surface) -> None:
        if self.selected:
            text = self.font.render(menu_labels[self.name], True, c.SELECTED_GRAY)
        else:
            text = self.font.render(menu_labels[self.name], True, c.RESTING_GRAY)

        text_rect = text.get_rect(center=(setup.screen_size.get_width()/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


class Tooltip(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        sprite = setup.GFX["tooltip_bubble"]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TOOLTIP_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def render_text(self) -> None:
        pass


    def scale_to_text_size(self) -> None:
        pass


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, name) -> None:
        super().__init__()

        self.sprite = setup.GFX[name]
        #self.font = setup.FONTS["kenvector_future_thin"]

        self.frames = self.load_sprites_from_sheet()
        self.frames = tools.colorize(self.frames, button_icon_color[name])
        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # XXX
        #self.pressed_rect = self.frames[1].get_rect()
        # "Inflate" duplicate image to smaller by using negatives.
        #self.frames[1].get_rect().inflate_ip((-c.PRESSED_BUTTON_OFFSET, -c.PRESSED_BUTTON_OFFSET))

        self.name = name
        self.keybind = button_binds[self.name]
        # key: wood_axe_icon value: current keybind for action in binds file

        self.current_time = 0
        self.pressed_time = 0
        # Very fast animation when pressed.
        self.animation_speed = 40


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, c.ORIGINAL_ICON_SIZE, c.ORIGINAL_ICON_SIZE, self.sprite, mult=c.BUTTON_MULT))
        frames.append(helpers.get_image(0, 0, c.ORIGINAL_ICON_SIZE, c.ORIGINAL_ICON_SIZE, self.sprite, mult=c.PRESSED_BUTTON_MULT))
        return frames


    def update(self, current_time: int) -> None:
        self.current_time = current_time
        self.handle_state()


    def handle_state(self) -> None:
        # Ex. if near_tree: cut.
        if binds.INPUT.pressed(self.keybind) or self.rect.collidepoint(*binds.INPUT.last_mouse_click()):
            self.pressed_animation()
            self.action()
        else:
            # Only finished animation if the button is no longer pressed.
            self.finished_animation_check()


    def action(self) -> None:
        pass


    def pressed_animation(self) -> None:
        self.pressed_timer = time.time()
        self.image = self.frames[1]


    def finished_animation_check(self) -> None:
        if self.current_time - self.pressed_time > self.animation_speed:
            self.image = self.frames[0]


    # XXX Unused but can be used to either write to keybind onto the
    # button or used to draw the tooltip, which can include the description
    # and probably the keybind as well.
    def render_name(self, surface) -> None:
        if self.pressed:
            text = self.font.render(menu_labels[self.name], True, c.WHITE)
        else:
            text = self.font.render(menu_labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(setup.screen_size.get_width()/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


class Hud:
    def __init__(self) -> None:
        self.font = setup.FONTS["game_kenvector_future_thin"]

        self.x = setup.screen_size.get_width() - c.IMMUTABLE_HUD_X_OFFSET
        self.y = c.IMMUTABLE_HUD_Y
        self.clock = ""
        self.coords = ""


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            self.x = setup.screen_size.get_width() - c.IMMUTABLE_HUD_X_OFFSET
            self.y = c.IMMUTABLE_HUD_Y


    def update(self, screen: pg.Surface, game_info: Dict[str, Any], player: pg.sprite.Sprite, map_height: int) -> None:
        self.update_sizes()

        # Don't need game_info for clock but will still need it later.
        self.update_clock()
        self.update_coords(player.rect.x, player.rect.y, map_height)

        self.render_clock(screen)
        self.render_coords(screen)


    def update_clock(self) -> None:
        """Get the real time and save it as a string.
        Ex. 8:15 AM
        """
        time = datetime.now()
        time = time.strftime("%I:%M %p")

        # Remove the starting zero from the hour if it exists.
        if time.startswith("0"):
            time = time[1:]
        self.clock = time


    def update_coords(self, x: int, y: int, map_height: int) -> None:
        self.coords = "({}, {})".format(x, map_height - y)


    def render_clock(self, surface: pg.Surface) -> None:
        text = self.font.render(self.clock, True, c.WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)


    def render_coords(self, surface: pg.Surface) -> None:
        text = self.font.render(self.coords, True, c.SELECTED_GRAY)
        text_rect = text.get_rect(center=(self.x - c.IMMUTABLE_HUD_X_OFFSET*2, self.y))
        surface.blit(text, text_rect)


    def notification(self) -> None: pass
    def detect_item_change(self) -> None:
        # Compare stored game info inventory to new game info
        # and display a notification for a period of time that
        # displays the items gained? But also if the items gained
        # are within the period of time that the notification would
        # be displayed, then add it to the notifcation instead of
        # overwriting. Show Lumber + 1! and if another lumber is
        # gained within the time of the notification being displayed,
        # show Lumber + 2! and reset the display timer.
        pass


class GameUI:
    def __init__(self) -> None:
        self.button_x = c.IMMUTABLE_BUTTON_X
        self.button_y = setup.screen_size.get_height() - c.IMMUTABLE_BUTTON_Y_OFFSET
        self.re_setup_buttons()


    def re_setup_buttons(self) -> None:
        self.button_group = pg.sprite.Group()
        button_y = self.button_y
        button_separation = 0

        for name in list(button_icon_color.keys()):
            self.button_group.add(Button(self.button_x + button_separation, button_y, name))
            button_separation += c.BUTTON_OFFSET


    def update(self, screen: pg.Surface, current_time: int, mainstate: c.MainState) -> None:
        self.handle_state(mainstate)

        if self.state == c.Switch.ON:
            self.update_sizes()
            self.button_group.update(current_time)
            self.blit_images(screen)


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            self.button_y = setup.screen_size.get_height() - c.IMMUTABLE_BUTTON_Y_OFFSET
            self.re_setup_buttons() # Re-setup buttons after y changes.


    def handle_state(self, mainstate) -> None:
        if mainstate == c.MainState.MAINMENU or mainstate == c.MainState.INGAMEMENU:
            self.state = c.Switch.OFF
        else:
            self.state = c.Switch.ON


    def blit_images(self, screen: pg.Surface) -> None:
        # Draw sprites onto the screen
        self.button_group.draw(screen)
