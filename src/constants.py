import enum

import pygame


CAPTION = "Garden"

# Frames per second.
FPS = 40
PG_GET_PRESSED_LENGTH = 323
CAMERA_BIGGER_SIZE = 100 # Represents increasing each side by this amount.


# Debug flags.
DEBUG_MAP = False
DEBUG_CAMERA = False
DEBUG_ENEMY = False
DEBUG_PLAYER = False
DEBUG_NPC = False


def flip_player_camera_combo(flip: bool) -> None:
    global DEBUG_CAMERA
    global DEBUG_PLAYER
    DEBUG_CAMERA = flip
    DEBUG_PLAYER = flip
flip_player_camera_combo(False)


class StateName(enum.Enum):
    MAINMENU = 0
    COMMONAREA = 1
    INGAMEMENU = 2


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
    GROWING = 1
    GROWN = 2


# XXX Unused
class TimeState(enum.Enum):
    RUNNING = 0
    PAUSED = 1


class Biome(enum.Enum):
    FARMLAND = 0
    CAVE = 1
    HOUSE = 2
    ISLAND = 3


class Switch(enum.Enum):
    ON = 0
    OFF = 1


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
PANEL_GRAY =    (186, 186, 186)
# Colorkey for pressed icons.
ICON_GRAY =     (136, 136, 136)

# Soothing colors for UI buttons.
FOREST_GREEN =  (83, 150, 78)
DARK_PALE =     (170, 155, 82)
AUTUMN =        (255, 167, 73)
NICE_VIOLET =   (229, 162, 219)

# Quality colors
DIRTY_GRAY =    (128, 130, 132)
MAROON =        (130, 0, 0)
BROWN =         (96, 37, 3)
BLUE =          (30, 17, 145)
BACTERIA =      (56, 142, 17)
TEAL =          (39, 178, 146)
ORANGE =        (186, 58, 0)
MAGENTA =       (158, 0, 150)
LIME_GREEN =    (87, 155, 20)
DARK_YELLOW =   (188, 188, 0)


# Multipliers.
DEFAULT_BACKGROUND_X_MULT = 0.26042 # Resolution w / background w
DEFAULT_BACKGROUND_Y_MULT = 0.39063 # Resolution h / background h
ENEMY_MULT = 1.5
PROJECTILE_MULT = 1.25
NPC_MULT = 0.25

MENU_MULT = 1.15
BUTTON_MULT = 0.10  # 0.16 makes the button the size of a tile
ITEM_MULT = 0.09     # 0.08 is 32x32, but items are 36x36, 0.09 is perfect.
PRESSED_BUTTON_MULT = 0.097
TOOLTIP_MULT = 1

map_mult = {
    Biome.FARMLAND: 5,
    Biome.ISLAND: 2,
    Biome.CAVE: 2,
    Biome.HOUSE: 0.5,
}


# Sizes.
TILE_SIZE = 64
ORIGINAL_ICON_SIZE = 400
BUTTON_SIZE = ORIGINAL_ICON_SIZE * BUTTON_MULT # 400 is actual the w/h of the button icon PNGs.
SLOT_SIZE = 36

#DEFAULT_SCREEN_WIDTH = 800
#DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
DEFAULT_SCREEN_SIZE = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

CORNER_SIZE = 15

FONT_SIZE_DICT = {
    "menu": 22,
    "game": 14,
}

# Full size(1) for tile_size = 64
# Half size(0.5)  for tile_size = 32
TILE_MULT = TILE_SIZE / 64


speeds = {
    "player": 3 if not DEBUG_PLAYER else 20,
    "enemy": 2 if not DEBUG_ENEMY else 30,
    "projectile": 10,
    "npc_roaming": 2 if not DEBUG_NPC else 10,
    "npc_running": 3,
    "camera": 3 if not DEBUG_CAMERA else 20,
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
FENCE_DENSITY = 50
TREE_DENSITY = 11

MIN_FENCE_LENGTH = 2
MAX_FENCE_LENGTH = 5

MIN_NPC_AMOUNT = 5
MAX_NPC_AMOUNT = 9
MIN_STAIRS_AMOUNT = 5
MAX_STAIRS_AMOUNT = 8


# Offsets.
TREE_SHADOW_OFFSET = 9
BUTTON_OFFSET = 60
MENU_SELECTION_OFFSET = 73
#PRESSED_BUTTON_OFFSET = ORIGINAL_ICON_SIZE * 0.02


# Starting heights based off the default screen size.
IMMUTABLE_BUTTON_X = 100
IMMUTABLE_BUTTON_Y_OFFSET = 100
STARTING_MENU_Y = int(DEFAULT_SCREEN_HEIGHT / 3.5)
MENU_WIDTH = 218 # Size of the menu item sprites after transformation.
IMMUTABLE_HUD_X_OFFSET = 70
IMMUTABLE_HUD_Y = 20

SIDE_PANEL_WIDTH = 290
SLOT_OFFSET = 6
MESH_X_OFFSET = 271 # 290 - ((290 - ((6 * c.SLOT_SIZE) + (6 * SLOT_OFFSET))) / 2) = 271
MESH_Y_OFFSET = 100
NUM_SLOTS_WIDE = 6


# Scalers.
# I know that for the 800 by 600 resolution the background
# multiplier of 0.397 fits well so that mimick that scale
# determine a value to multiply the sum of the width and height
# to get a reasonable background multiplier.
BACKGROUND_X_SCALER = DEFAULT_BACKGROUND_X_MULT / DEFAULT_SCREEN_WIDTH
BACKGROUND_Y_SCALER = DEFAULT_BACKGROUND_Y_MULT / DEFAULT_SCREEN_HEIGHT
