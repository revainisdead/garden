from typing import Tuple

import os

import pygame as pg

from . import constants as c
from . import tools


GFX =   {}
FONTS = {}
SFX =   {}

screen_size = None

class ScreenSize:
    def __init__(self):
        self.__width, self.__height = c.DEFAULT_SCREEN_SIZE
        self.__changed = False


    def __resize(self, width: int, height: int) -> None:
        if width != self.__width and height != self.__height:
            self.__width = width
            self.__height = height
            self.__changed = True
        else:
            self.__changed = False


    def get_size(self) -> Tuple[int, int]:
        return self.__width, self.__height


    def get_width(self) -> int:
        return self.__width


    def get_height(self) -> int:
        return self.__height


    def changed(self) -> bool:
        """This will spit out true for only one frame when the size changes."""
        return self.__changed


    def update(self, width: float, height: float) -> None:
        self.__resize(int(round(width)), int(round(height)))

        if self.__changed:
            pg.display.set_mode((self.__width, self.__height), pg.RESIZABLE)


def start():
    pg.init()
    pg.font.init()

    # Initialize screen
    _ = pg.display.set_mode(c.DEFAULT_SCREEN_SIZE, pg.RESIZABLE)

    global GFX
    GFX = tools.load_gfx(os.path.join("data", "graphics"))
    global FONTS
    FONTS = tools.load_fonts(os.path.join("data", "fonts"))
    global SFX
    SFX = tools.load_sfx(os.path.join("data", "sounds"))

    global screen_size
    screen_size = ScreenSize()
