import enum

import pygame as pg


# Debug flags.
DEBUG_MAP = False # XXX Doesn't work properly with new camera changes.
DEBUG_CAMERA = True


class MainState(enum.Enum):
    MAINMENU = 0
    COMMONAREA = 1


class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    LEFTUP = 4
    LEFTDOWN = 5
    RIGHTUP = 6
    RIGHTDOWN = 7


class TimeState(enum.Enum):
    RUNNING = 0
    PAUSED = 1


# Extract colors using: labs.tineye.com/color/
# (TIP: Uncheck "Exclude background color from extracted colors")
# Convert hex color to r,g,b using: www.rapidtables.com/convert/color/
# Sprites: getspritexy.com, spritecow.com
#            R, G, B
RED =       (255, 0, 0)
GREEN =     (0, 255, 0)
BLUE =      (0, 0, 255)
YELLOW =    (0, 255, 255)
PURPLE =    (255, 0, 255)
GRAY =      (100, 100, 100)
BLACK =     (0, 0, 0)
WHITE =     (255, 255, 255)
SAPPHIRE =  (5, 35, 94)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_WIDTH = SCREEN_WIDTH*4
MAP_HEIGHT = SCREEN_HEIGHT*4
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)
TILE_SIZE = 64

FONT_SIZE = 22

# Multipliers.
BACKGROUND_MULT = 2.5
ENEMY_MULT = 1.5
PROJECTILE_MULT = 1.25
UI_MULT = 1.15
TILE_MULT = 1

# Speeds
speeds = {
    "player": 10,
    "enemy": 30,
    "camera": 100 if DEBUG_CAMERA else 10,
}
