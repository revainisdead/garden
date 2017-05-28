import enum

import pygame as pg


# Frames per second.
FPS = 20


# Debug flags.
DEBUG_MAP = False # XXX Doesn't work properly with new camera changes.
DEBUG_CAMERA = True
DEBUG_ENEMY = False


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
    NONE = 8


# XXX Unused
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


# Sizes.
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
NPC_MULT = 0.25


# Speeds.
speeds = {
    "player": 10,
    "enemy": 2 if not DEBUG_ENEMY else 30,
    "projectile": 10,
    "npc_roaming": 1.5,
    "npc_running": 5,
    "camera": 10 if not DEBUG_CAMERA else 100,
}

# Density.
BUSH_DENSITY = 10

# Offsets.
TREE_SHADOW_OFFSET = 9
