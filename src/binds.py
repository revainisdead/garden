import pygame as pg


# XXX Load keys from json file
# Allow json file to be manipulated from main menu
# To allow changing of keybinds
# Note: Don't implement until decided what the keys actually do by
# default because the strings will name them: move_left, move_right, etc.
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
