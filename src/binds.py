from typing import Optional, Tuple

import pygame as pg

from . import constants as c


# XXX Load keys from json file
# Allow json file to be manipulated from main menu
# To allow changing of keybinds
# Note: Don't implement until decided what the keys actually do by
# default because the strings will name them: move_left, move_right, etc.
#
# Need to have a list of all available keybinds: shift, letters, numbers, etc.

#default_keybinds = {}

keybinds = {
    "up": pg.K_w,
    "down": pg.K_s,
    "left": pg.K_a,
    "right": pg.K_d,
    "escape": pg.K_ESCAPE,
    "enter": pg.K_RETURN,
    "arrow_up": pg.K_UP,
    "arrow_down": pg.K_DOWN,
    "one": pg.K_1,
    "two": pg.K_2,
}


# Some keys should be able to be set, like "use_wood_axe",
# But moving a menu item, aka up and down, should be unchanging.
# NOTE: This is not actually frozen. It can be changed but shouldn't be.
frozen_binds = {
    "arrow_up": pg.K_UP,
    "arrow_down": pg.K_DOWN,
}


def reset_keybinds(self) -> None:
    #keybinds = default_keybinds
    pass


class Input:
    """
    A class that handles all input and keybinds.
        - Other objects like states and the player, camera, etc.
          should interface with this one, so that that input is streamline
          and not affecting everything in muliple places.
        - In general should only be read from. Also reset should be called
          once per frame. All setters are internal.

    Pressed:
        - Every time a key is pressed down, that is one press. A press can
          only happen in one frame. Whether or not the key was let go does
          not matter.

    Held:
        - Key sends a keydown for every frame it is held down for.
    """
    def __init__(self):
        self.__last_keys_pressed = []
        self.__held_keys = tuple(0 for _ in range(c.PG_GET_PRESSED_LENGTH))
        self.__mouse_pos = (0, 0)
        self.__last_mouse_click = (0, 0)
        self.__last_mouse_drop = (0, 0)


    def __set_last_keys_pressed(self, key: Optional[int]) -> None:
        """Add key that generates a KEYDOWN event in one frame.
        Because many different keys can be pressed in a short amount
        of time. Make this a list of the last keys pressed
        """
        if key is None:
            self.__last_keys_pressed = []
        else:
            self.__last_keys_pressed.append(key)


    def __set_held_keys(self, keys: Tuple[int, ...]) -> None:
        """Add keys gathered from event.get_pressed."""
        self.__held_keys = keys


    def __set_mouse_pos(self, point: Optional[Tuple[int, int]]) -> None:
        self.__mouse_pos = point


    def __set_last_mouse_click(self, point: Optional[Tuple[int, int]]) -> None:
        if point is None:
            self.__last_mouse_click = (0, 0)
        else:
            self.__last_mouse_click = point


    def __set_last_mouse_drop(self, point: Optional[Tuple[int, int]]) -> None:
        if point is None:
            self.last_mouse_drop = (0, 0)
        else:
            self.__last_mouse_drop = point


    def update(self, event: Optional[pg.event.Event]) -> None:
        if event.type == pg.KEYDOWN:
            self.__set_last_keys_pressed(event.key)
            self.__set_held_keys(pg.key.get_pressed())
        elif event.type == pg.KEYUP:
            self.__set_held_keys(pg.key.get_pressed())
        elif event.type == pg.MOUSEMOTION:
            point = pg.mouse.get_pos()
            self.__set_mouse_pos(point)
        elif event.type == pg.MOUSEBUTTONDOWN:
            point = pg.mouse.get_pos()
            self.__set_last_mouse_click(point)
        elif event.type == pg.MOUSEBUTTONUP:
            point = pg.mouse.get_pos()
            self.__set_last_mouse_drop(point)

        #self.button_lock = True
        #if event.type != pg.KEYDOWN:
            # If no keydown was sent, reset last key pressed value.
            #self.__set_last_key_pressed(None)
        if event.type != pg.MOUSEBUTTONDOWN:
            self.__set_last_mouse_click(None)
        if event.type != pg.MOUSEBUTTONUP:
            self.__set_last_mouse_drop(None)


    def last_keys_pressed(self) -> Optional[int]:
        return self.__last_keys_pressed


    def held_keys(self) -> Optional[Tuple[int, ...]]:
        return self.__held_keys


    def mouse_pos(self) -> Optional[Tuple[int, int]]:
        return self.__mouse_pos


    def last_mouse_click(self) -> Optional[Tuple[int, int]]:
        return self.__last_mouse_click


    def last_mouse_drop(self) -> Optional[Tuple[int, int]]:
        return self.__last_mouse_drop


    def pressed(self, value: str) -> bool:
        """Convenience function for testing last pressed keybind"""
        return keybinds[value] in self.__last_keys_pressed


    def held(self, value: str) -> bool:
        """Convenience function for testing held keybinds."""
        return bool(self.__held_keys[keybinds[value]])


    def reset(self) -> None:
        """This should be called once per frame to reset
        keys that need to be read Once Per Frame.
        """
        self.__set_last_keys_pressed(None)
        self.__set_last_mouse_click(None)
        self.__set_last_mouse_drop(None)


INPUT = Input()
