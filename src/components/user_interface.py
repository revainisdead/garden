from typing import Any, Dict, List, Tuple

from collections import OrderedDict
from datetime import datetime
import time
import queue

import pygame

from . import helpers
from . import inventory
from . import item

from .. import binds
from .. import constants as c
from .. import gameinfo
from .. import setup
from .. import tools


menu_labels = {
    "play": "play",
    "load_game": "load game",
    "quit": "quit",
}


button_actions = {}
button_binds = {}


class MenuSelection(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, name: str) -> None:
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


    def load_sprites_from_sheet(self) -> List[pygame.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite, mult=c.MENU_MULT))
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite_selected, mult=c.MENU_MULT))
        return frames


    def update(self, selection: str) -> None:
        self.handle_state(selection)


    def handle_state(self, selection: str) -> None:
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


    def render_text(self) -> None:
        pass


    def scale_to_text_size(self) -> None:
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, name: str, color: Tuple[int, ...]) -> None:
        super().__init__()

        self.sprite = setup.GFX[name]

        self.frames = self.load_sprites_from_sheet()
        self.frames = tools.colorize(self.frames, color)
        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # XXX
        #self.pressed_rect = self.frames[1].get_rect()
        # "Inflate" duplicate image to smaller by using negatives.
        #self.frames[1].get_rect().inflate_ip((-c.PRESSED_BUTTON_OFFSET, -c.PRESSED_BUTTON_OFFSET))

        self.name = name
        self.action = button_actions[self.name]
        self.keybind = button_binds[self.name]
        # key: wood_axe_icon value: current keybind for action in binds file

        self.game_time = 0
        self.pressed_time = 0
        # Very fast animation when pressed.
        self.animation_speed = 80


    def load_sprites_from_sheet(self) -> List[pygame.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, c.ORIGINAL_ICON_SIZE, c.ORIGINAL_ICON_SIZE, self.sprite, mult=c.BUTTON_MULT))
        frames.append(helpers.get_image(0, 0, c.ORIGINAL_ICON_SIZE, c.ORIGINAL_ICON_SIZE, self.sprite, mult=c.PRESSED_BUTTON_MULT))
        return frames


    def update(self, game_time: int, inp: binds.Input, action_q: queue.Queue) -> None:
        self.game_time = game_time
        self.handle_state(inp, action_q)


    def handle_state(self, inp: binds.Input, action_q: queue.Queue) -> None:
        # Ex. if near_tree: cut.
        # Use * in a function call to unpack in one go.
        #if inp.pressed(self.keybind) or self.rect.collidepoint(*inp.last_mouse_click()):

        lmc = inp.last_mouse_click()
        if lmc == None:
            lmc = (0, 0)
        if inp.pressed(self.keybind) or self.rect.collidepoint(lmc):
            self.pressed_time = self.game_time
            action_q.put(self.action)
        else:
            self.pressed_animation()


    def pressed_animation(self) -> None:
        if self.game_time - self.pressed_time > self.animation_speed:
            self.image = self.frames[0]
        else:
            self.image = self.frames[1]


class Hud:
    def __init__(self) -> None:
        self.font = setup.FONTS["game_kenvector_future_thin"]

        #self.x = setup.screen_size.get_width() - c.IMMUTABLE_HUD_X_OFFSET
        self.x = 0 + c.IMMUTABLE_HUD_X_OFFSET
        self.y = c.IMMUTABLE_HUD_Y
        self.clock = ""
        self.coords = ""


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            self.x = 0 + c.IMMUTABLE_HUD_X_OFFSET
            self.y = c.IMMUTABLE_HUD_Y


    def update(self, screen: pygame.Surface, c_fps: int, player: pygame.sprite.Sprite, map_height: int) -> None:
        if setup.screen_size.changed():
            self.update_sizes()

        self.update_clock()
        self.update_coords(player.rect.x, player.rect.y, map_height)
        self.c_fps = c_fps

        self.render_clock(screen)
        self.render_coords(screen)
        self.render_fps(screen)


    def update_clock(self) -> None:
        """Get the real time and save it as a string.
        Ex. 8:15 AM
        """
        dt_t = datetime.now()

        # Don't overwrite dt_t (for mypy), because it has a different type.
        t = dt_t.strftime("%I:%M %p")
        if t.startswith("0"):
            time = t[1:]
        self.clock = t


    def update_coords(self, x: int, y: int, map_height: int) -> None:
        self.coords = "({}, {})".format(x, map_height - y)


    def render_clock(self, surface: pygame.Surface) -> None:
        text = self.font.render(self.clock, True, c.WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)


    def render_coords(self, surface: pygame.Surface) -> None:
        text = self.font.render(self.coords, True, c.SELECTED_GRAY)
        text_rect = text.get_rect(center=(self.x + c.IMMUTABLE_HUD_X_OFFSET*2, self.y))
        surface.blit(text, text_rect)


    def render_fps(self, surface: pygame.surface.Surface) -> None:
        text = self.font.render(str(round(self.c_fps)), True, c.SELECTED_GRAY)
        text_rect = text.get_rect(center=(self.x + c.IMMUTABLE_HUD_X_OFFSET*4, self.y))
        surface.blit(text, text_rect)

    def notification(self) -> None: pass
    def detect_item_change(self) -> None:
        # XXX
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
        # XXX Later can dynamically add or remove items depending on
        # which items are equipped (some items might give special power)
        self.button_icon_and_color = [] # type: List[Tuple[str, Tuple[int, int, int]]]

        # Create base buttons list here
        self.add_new_button("wood_axe_icon", c.DARK_PALE, "cut", c.Action.Cut)
        self.add_new_button("tree_icon", c.FOREST_GREEN, "tree", c.Action.Grow)
        self.add_new_button("grabbers_icon", c.AUTUMN, "search", c.Action.Search)
        self.add_new_button("flip_icon", c.NICE_VIOLET, "flip", c.Action.SwapWorker)

        self.button_x = c.IMMUTABLE_BUTTON_X
        self.button_y = setup.screen_size.get_height() - c.IMMUTABLE_BUTTON_Y_OFFSET
        self.re_setup_buttons()

        self.inv = inventory.Inventory()


    def add_new_button(self, icon_name: str, color: Tuple[int, int, int], bind: str, action: c.Action) -> None:
        self.button_icon_and_color.append((icon_name, color))
        button_actions[icon_name] = action
        button_binds[icon_name] = bind


    def re_setup_buttons(self) -> None:
        """
        This is responsible for the initial setup of buttons and also
        re-setting them up when the size of the screen changes.
        """
        self.button_group = pygame.sprite.Group()
        button_y = self.button_y
        button_separation = 0

        for entry in self.button_icon_and_color:
            name, color = entry
            self.button_group.add(Button(self.button_x + button_separation, button_y, name, color))
            button_separation += c.BUTTON_OFFSET


    def update(self, screen: pygame.Surface, mainstate: c.StateName, game_info: gameinfo.GameInfo) -> None:
        item_tmp = None # type: item.Item
        if not game_info.new_items.empty():
            #print(list(game_info.new_items.queue))
            item_tmp = game_info.new_items.get()

        self.handle_state(mainstate)

        if self.state == c.Switch.ON:
            self.inv.update(screen, game_info.inp, item_tmp)
            self.update_sizes()
            self.button_group.update(game_info.game_time, game_info.inp, game_info.action_attempts)
            self.blit_images(screen)


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            self.button_y = setup.screen_size.get_height() - c.IMMUTABLE_BUTTON_Y_OFFSET
            self.re_setup_buttons() # Re-setup buttons after y changes.


    def handle_state(self, mainstate) -> None:
        if mainstate == c.StateName.MAINMENU or mainstate == c.StateName.INGAMEMENU:
            self.state = c.Switch.OFF
        else:
            self.state = c.Switch.ON


    def blit_images(self, screen: pygame.Surface) -> None:
        self.button_group.draw(screen)
