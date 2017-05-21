import enum

import pygame as pg


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


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


#            R, G, B
# Extract colors using: labs.tineye.com/color/
# (TIP: Uncheck "Exclude background color from extracted colors")
# Convert hex color to r,g,b using: www.rapidtables.com/convert/color/
# Sprites: getspritexy.com, spritecow.com
RED =       (255, 0, 0)
GREEN =     (0, 255, 0)
BLUE =      (0, 0, 255)
YELLOW =    (0, 255, 255)
PURPLE =    (255, 0, 255)
GRAY =      (100, 100, 100)
BLACK =     (0, 0, 0)
WHITE =     (255, 255, 255)
SAPPHIRE =  (5, 35, 94)
