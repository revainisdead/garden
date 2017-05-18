import enum

import pygame as pg


class States(enum.Enum):
    MAINMENU = 0
    COMMONAREA = 1


binds = {
    "up": pg.K_w,
    "down": pg.K_s,
    "left": pg.K_a,
    "right": pg.K_d,
    "escape": pg.K_ESCAPE,
    "enter": pg.K_RETURN,
}


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


# R, G, B
RED =       (255, 0, 0)
GREEN =     (0, 255, 0)
BLUE =      (0, 0, 255)
YELLOW =    (0, 255, 255)
PURPLE =    (255, 0, 255)
GRAY =      (100, 100, 100)
BLACK =     (0, 0, 0)
WHITE =     (255, 255, 255)
