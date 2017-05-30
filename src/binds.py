import pygame as pg


# XXX Load keys from json file
# Allow json file to be manipulated from main menu
# To allow changing of keybinds
# Note: Don't implement until decided what the keys actually do by
# default because the strings will name them: move_left, move_right, etc.
#
# Need to have a list of all available keybinds: shift, letters, numbers, etc.
keybinds = {
    "up": pg.K_w,
    "down": pg.K_s,
    "left": pg.K_a,
    "right": pg.K_d,
    "escape": pg.K_ESCAPE,
    "enter": pg.K_RETURN,
    "arrow_up": pg.K_UP,
    "arrow_down": pg.K_DOWN,
}


class Input:
    # A class that handles all input and keybinds.
    #   - Other objects like states and the player, camera, etc.
    #     should interface with this one, so that that input is streamline
    #     and not affecting everything in muliple places.
    def __init__(self):
        pass
