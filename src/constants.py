import enum

import pygame as pg


CAPTION = "Garden"

# Frames per second.
FPS = 40


# Debug flags.
DEBUG_MAP = False # XXX Doesn't work properly with new camera changes.
DEBUG_CAMERA = False # XXX IF NOT CAMERA_ON_HERO, use debug_camera speed.
DEBUG_ENEMY = False
DEBUG_NPC = False


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


class CropState(enum.Enum):
    HARVESTED = 0
    GROWN = 1


# XXX Unused
class TimeState(enum.Enum):
    RUNNING = 0
    PAUSED = 1


# Extract colors using: labs.tineye.com/color/
# (TIP: Uncheck "Exclude background color from extracted colors")
# Convert hex color to r,g,b using: www.rapidtables.com/convert/color/
# Sprites: getspritexy.com, spritecow.com
#            R, G, B
RED =           (255, 0, 0)
GREEN =         (0, 255, 0)
BLUE =          (0, 0, 255)
YELLOW =        (0, 255, 255)
PURPLE =        (255, 0, 255)
GRAY =          (100, 100, 100)
BLACK =         (0, 0, 0)
WHITE =         (255, 255, 255)

# Colorkey for pressed icons.
ICON_GRAY =     (136, 136, 136)

# Soothing colors for UI buttons.
PALE =          (251, 255, 193) # Too close to white for an icon.
SOFT_GREEN =    (176, 255, 112)
#LIGHT_YELLOW =  (242, 244, 117)
LIGHT_YELLOW =  (232, 234, 119)


# Multipliers.
BACKGROUND_MULT = 2.5
ENEMY_MULT = 1.5
PROJECTILE_MULT = 1.25
NPC_MULT = 0.25

MENU_MULT = 1.15
BUTTON_MULT = 0.10 # 0.16 makes the button the size of a tile
PRESSED_BUTTON_MULT = 0.095


# Sizes.
TILE_SIZE = 64
BUTTON_SIZE = 400 * BUTTON_MULT # 400 is actual the w/h of the button icon PNGs.

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_WIDTH = SCREEN_WIDTH*4
MAP_HEIGHT = SCREEN_HEIGHT*4
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)
GRID_WIDTH = int(MAP_WIDTH / TILE_SIZE)
GRID_HEIGHT = int(MAP_HEIGHT / TILE_SIZE)

CORNER_SIZE = 15

FONT_SIZE = 22

# Full size(1) for tile_size = 64
# Half size(0.5)  for tile_size = 32
TILE_MULT = TILE_SIZE / 64


# Speeds.
speeds = {
    "player": 10,
    "enemy": 2 if not DEBUG_ENEMY else 30,
    "projectile": 10,
    "npc_roaming": 2 if not DEBUG_NPC else 10,
    "npc_running": 5,
    "camera": 5 if not DEBUG_CAMERA else 100,
}
# Running: also change animation speed.
# And change sprite state.


# Density.
BUSH_DENSITY = 10
FENCE_DENSITY = 40
TREE_DENSITY = 8

MIN_FENCE_LENGTH = 2
MAX_FENCE_LENGTH = 5

MIN_NPC_AMOUNT = 3
MAX_NPC_AMOUNT = 8


# Offsets.
TREE_SHADOW_OFFSET = 9
BUTTON_OFFSET = 60
MENU_SELECTION_OFFSET = 80
