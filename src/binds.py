from typing import Optional, List, Sequence, Tuple

import pygame

from . import keys
from . import constants as c
from . import setup


# XXX Put this info in the game info object.
# KB can be a member of input, since it's the only class
# that can access it. Then keybinds can be put in the game_info
# object, so that it can be accessed everywhere using "action"!!!
# Boom no more global variables and then the game_info object
# can
# - be cleaned up on state exit
# - can be cleaned up on game exit
# - can be accessed by evertying in the game
# - can allow multithreaded data access if game_info is made thread safe
#KB = keys.Keybinds() # do this so that KB can be called separately
                     # for clean up. in this case it's to dump the
                     # keybinds file.
#keybinds = KB.keybinds


# XXX Load keys from json file
# Allow json file to be manipulated from main menu
# To allow changing of keybinds
# Note: Don't implement until decided what the keys actually do by
# default because the strings will name them: move_left, move_right, etc.
#
# Need to have a list of all available keybinds: shift, letters, numbers, etc.

#default_keybinds = {}

# Key: unchangable: action
# Value: changable: { current_key_in_config }

# config layout:
# "move_up" = "w"
# "move_down" = "s"

# translate = confirm first word exists:
# all_actions = {"move_up", "move_down", "move_left", "move_right"} # unordered set of strings
# all_keys = { "w": pygame.K_w }
# action in all_actions
# key in all_keys

# modifiers
# ex.
# "move_up" = shift+"w"
# "move_down" = ctrl+"s"
# "move_left" = alt+"a"
# NOTE: Or don't use quotes in text file, just get word and convert to string.

# all_mods = { "none": KMOD_NONE, "shift": KMOD_SHIFT, "ctrl": KMOD_CTRL, "alt": KMOD_ALT }


# XXX Need?
frozen_binds = {
    "arrow_up": pygame.K_UP,
    "arrow_down": pygame.K_DOWN,
}


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
    def __init__(self) -> None:
        self.__last_keys_pressed = [] # type: List[int]
        self.__held_keys = tuple(False for _ in range(c.PG_GET_PRESSED_LENGTH)) # type: Sequence[bool]
        self.__mouse_pos = (0, 0)
        self.__last_mouse_click = (0, 0)
        self.__last_mouse_drop = (0, 0)

        # Interface to the keybinds object through this class.
        self.__KB = keys.Keybinds()
        self.__keybinds = self.__KB.keybinds


    def __set_last_keys_pressed(self, key: Optional[int]) -> None:
        """Add key that generates a KEYDOWN event in one frame.
        Because many different keys can be pressed in a short amount
        of time. Make this a list of the last keys pressed
        """
        if key is None:
            self.__last_keys_pressed = []
        else:
            self.__last_keys_pressed.append(key)


    def __set_held_keys(self, keys: Sequence[bool]) -> None:
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
            self.__last_mouse_drop = (0, 0)
        else:
            self.__last_mouse_drop = point


    def update(self, event: Optional[pygame.event.Event]) -> None:
        if event.type == pygame.KEYDOWN:
            self.__set_last_keys_pressed(event.key)
            self.__set_held_keys(pygame.key.get_pressed())
        elif event.type == pygame.KEYUP:
            self.__set_held_keys(pygame.key.get_pressed())
        elif event.type == pygame.MOUSEMOTION:
            point = pygame.mouse.get_pos()
            self.__set_mouse_pos(point)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            point = pygame.mouse.get_pos()
            self.__set_last_mouse_click(point)
        elif event.type == pygame.MOUSEBUTTONUP:
            point = pygame.mouse.get_pos()
            self.__set_last_mouse_drop(point)
        elif event.type == pygame.VIDEORESIZE:
            w, h = event.size
            setup.screen_size.update(w, h)


    def last_keys_pressed(self) -> Optional[List[int]]:
        return self.__last_keys_pressed


    def held_keys(self) -> Optional[Sequence[bool]]:
        return self.__held_keys


    def mouse_pos(self) -> Optional[Tuple[int, int]]:
        return self.__mouse_pos


    def last_mouse_click(self) -> Optional[Tuple[int, int]]:
        return self.__last_mouse_click


    def last_mouse_drop(self) -> Optional[Tuple[int, int]]:
        return self.__last_mouse_drop


    def pressed(self, action: str) -> bool:
        """Convenience function for testing last pressed keybind"""
        keys = tuple(self.__keybinds[action]) # type cast needed for mypy
        for key in keys:
            if key in self.__last_keys_pressed:
                return True

        return False


    def held(self, action: str) -> bool:
        """Convenience function for testing held keybinds."""
        keys = self.__keybinds[action]
        for key in keys:
            if self.__held_keys[key]:
                return True

        return False


    def reset(self) -> None:
        """This should be called once per frame to reset
        keys that need to be read Once Per Frame.
        """
        self.__set_last_keys_pressed(None)
        self.__set_last_mouse_click(None)
        self.__set_last_mouse_drop(None)


    def cleanup(self) -> None:
        self.__KB.dump()
