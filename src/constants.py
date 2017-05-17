import enum

import pygame as pg


class States(enum.Enum):
    COMMONAREA = 0


binds = {
    "up": pg.K_w,
    "down": pg.K_s,
    "left": pg.K_a,
    "right": pg.K_d,
}

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# R, G, B
RED =       (255, 0, 0)
GREEN=      (0, 255, 0)
BLUE =      (0, 0, 255)
YELLOW =    (0, 255, 255)


