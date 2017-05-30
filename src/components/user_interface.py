from typing import List, Tuple

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


button_icon_color = {
    "wood_axe_icon": c.LIGHT_YELLOW,
    "tree_icon": c.SOFT_GREEN,
}


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name) -> None:
        super().__init__()

        self.sprite = setup.GFX["green_button01"]
        self.sprite_selected = setup.GFX["green_button00"]

        self.font = setup.FONTS["kenvector_future_thin"]

        self.frames = self.load_sprites_from_sheet()
        self.image = self.frames[0]

        self.rect = self.image.get_rect()

        # To center the menu item, take half of the width away from x.
        self.rect.x = x - self.rect.width/2
        self.rect.y = y

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
            text = self.font.render(menu_labels[self.name], True, c.WHITE)
        else:
            text = self.font.render(menu_labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(c.SCREEN_WIDTH/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


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

        self.name = name
        #self.keybind = button_binds[self.name]
        self.keybind = pg.K_1

        # key: wood_axe_icon value: current keybind for action in binds file

        self.current_time = 0
        self.pressed_time = 0
        # Very fast animation when pressed.
        self.animation_speed = 40


    def load_sprites_from_sheet(self) -> List[pg.Surface]:
        frames = []
        frames.append(helpers.get_image(0, 0, 400, 400, self.sprite, mult=c.BUTTON_MULT))
        frames.append(helpers.get_image(0, 0, 400, 400, self.sprite, mult=c.PRESSED_BUTTON_MULT))
        return frames


    #def update(self, key_pressed: int) -> None:
        #self.handle_state(key_pressed)
    def update(self, keys: Tuple[int, ...]) -> None:
        self.current_time = time.time()

        self.handle_state(keys)


    #def handle_state(self, key_pressed) -> None:
        # Ex. if near_tree: cut.
        #if self.keybind == key_pressed:
            #self.action()
    def handle_state(self, keys: Tuple[int, ...]) -> None:
        # Ex. if near_tree: cut.
        if keys[self.keybind]:
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


    def render_name(self, surface) -> None:
        if self.pressed:
            text = self.font.render(menu_labels[self.name], True, c.WHITE)
        else:
            text = self.font.render(menu_labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(c.SCREEN_WIDTH/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


    #def set_keybind?


class GameUI:
    def __init__(self) -> None:
        self.setup_buttons()


    def setup_buttons(self) -> None:
        # XXX UI button area?
        # Don't set area and don't name it button1, loop over to create buttons?
        # And loop over a list of button sprite names
        # Well I need to map each button to an action, so I need to know them by variable.
        self.button_group = pg.sprite.Group()
        button_starting_x = 120
        button_y = 500

        button_separation = 0
        for name in button_icon_color.keys():
            self.button_group.add(Button(button_starting_x + button_separation, button_y, name))
            button_separation += c.BUTTON_OFFSET


    def update(self, screen: pg.Surface, keys: Tuple[int, ...]) -> None:
        # XXX Access Input to get key pressed
        key_pressed = None

        #self.handle_state()

        #self.button_group.update(key_pressed)
        self.button_group.update(keys)

        # if state is off: don't blit
        self.blit_images(screen)


    def handle_state(self) -> None:
        pass


    def blit_images(self, screen: pg.Surface) -> None:
        # Draw sprites onto the screen
        self.button_group.draw(screen)
