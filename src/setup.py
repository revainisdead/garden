import os

import pygame as pg

from . import tools
from . import constants as c


pg.init()
pg.display.set_mode(c.SCREEN_SIZE)

GFX = tools.load_gfx(os.path.join("data", "graphics"))
FONTS = tools.load_fonts(os.path.join("data", "fonts"))

