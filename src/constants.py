import enum

import pygame as pg


CAPTION = "Garden"

# Frames per second.
FPS = 20
PG_GET_PRESSED_LENGTH = 323


# Debug flags.
DEBUG_MAP = False   # XXX Doesn't work properly with new camera changes.
DEBUG_CAMERA = True # XXX IF NOT CAMERA_ON_HERO, use debug_camera speed.
DEBUG_ENEMY = False
DEBUG_PLAYER = False
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


class Biome(enum.Enum):
    FARMLAND = 0
    ISLAND = 1
    CAVE = 2
    HOUSE = 3


# Extract colors using: labs.tineye.com/color/
# (TIP: Uncheck "Exclude background color from extracted colors")
# Convert hex color to r,g,b using: www.rapidtables.com/convert/color/
# Sprites: getspritexy.com, spritecow.com
#                R, G, B
BLACK =         (0, 0, 0)
GRAY =          (100, 100, 100)
WHITE =         (255, 255, 255)
UGLY_PURPLE =   (255, 0, 255)

SELECTED_GRAY = (244, 244, 244)
RESTING_GRAY =  (90, 90, 90)

# Colorkey for pressed icons.
ICON_GRAY =     (136, 136, 136)

# Soothing colors for UI buttons.
FOREST_GREEN =  (83, 150, 78)
DARK_PALE =     (170, 155, 82)


# Multipliers.
BACKGROUND_MULT = 0.397
ENEMY_MULT = 1.5
PROJECTILE_MULT = 1.25
NPC_MULT = 0.25

MENU_MULT = 1.15
BUTTON_MULT = 0.10 # 0.16 makes the button the size of a tile
PRESSED_BUTTON_MULT = 0.097

map_mult = {
    Biome.FARMLAND: 4,
    Biome.ISLAND: 2,
    Biome.CAVE: 2,
    Biome.HOUSE: 0.5,
}


# Sizes.
TILE_SIZE = 64
ORIGINAL_ICON_SIZE = 400
BUTTON_SIZE = ORIGINAL_ICON_SIZE * BUTTON_MULT # 400 is actual the w/h of the button icon PNGs.

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

#***
# Base map size off of resolution, fix it to the nearest TILE_SIZE.
#***
#MAP_WIDTH = SCREEN_WIDTH*4
#MAP_HEIGHT = SCREEN_HEIGHT*4
MAP_WIDTH = round(SCREEN_WIDTH * map_mult[Biome.FARMLAND] / TILE_SIZE) * TILE_SIZE
MAP_HEIGHT = round(SCREEN_HEIGHT * map_mult[Biome.FARMLAND] / TILE_SIZE) * TILE_SIZE
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)
GRID_WIDTH = int(round(MAP_WIDTH / TILE_SIZE))
GRID_HEIGHT = int(round(MAP_HEIGHT / TILE_SIZE))

CORNER_SIZE = 15

FONT_SIZE = 22

# Full size(1) for tile_size = 64
# Half size(0.5)  for tile_size = 32
TILE_MULT = TILE_SIZE / 64


# Speeds.
speeds = {
    "player": 5 if not DEBUG_PLAYER else 15,
    "enemy": 2 if not DEBUG_ENEMY else 30,
    "projectile": 10,
    "npc_roaming": 3 if not DEBUG_NPC else 10,
    "npc_running": 5,
    "camera": 6 if not DEBUG_CAMERA else 100,
}

# XXX mirror movement speeds dict with proportional animation speeds.
#animation_speeds {
#    "player": ?,
#    "npc_roaming": ?,
#}


# Running: also change animation speed.
# And change sprite state.


# Density.
#BUSH_DENSITY = 10
#FENCE_DENSITY = 40
#TREE_DENSITY = 8
BUSH_DENSITY = 9
FENCE_DENSITY = 60
TREE_DENSITY = 6


MIN_FENCE_LENGTH = 2
MAX_FENCE_LENGTH = 5

MIN_NPC_AMOUNT = 3
MAX_NPC_AMOUNT = 8


# Offsets.
TREE_SHADOW_OFFSET = 9
BUTTON_OFFSET = 60
MENU_SELECTION_OFFSET = 73
#PRESSED_BUTTON_OFFSET = ORIGINAL_ICON_SIZE * 0.02


# Height on screen
UI_BUTTON_Y = SCREEN_HEIGHT * 5/6
MENU_Y = int(SCREEN_HEIGHT / 3.5)
