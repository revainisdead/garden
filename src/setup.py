import os

import pygame as pg

from . import binds
from . import constants as c
from . import tools


pg.init()
pg.font.init()

if not c.DEBUG_MAP:
    SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
else:
    SCREEN = pg.display.set_mode(c.MAP_SIZE)

SCREEN_RECT = SCREEN.get_rect()

GFX = tools.load_gfx(os.path.join("data", "graphics"))
FONTS = tools.load_fonts(os.path.join("data", "fonts"))
SFX = tools.load_sfx(os.path.join("data", "sounds"))
