import os

import pygame as pg

from . import tools
from . import constants as c


pg.init()
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

GFX = tools.load_gfx(os.path.join("data", "graphics"))
FONTS = tools.load_fonts(os.path.join("data", "fonts"))
