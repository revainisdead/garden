from typing import Any


from . rect import Rect
from . surface import Surface, SRCALPHA
from . import display
from . import event
from . import font
from . import key
from . import mixer
from . import mouse
from . import sprite
from . import time
from . import transform


K_w = \
K_a = \
K_s = \
K_d = \
K_1 = \
K_2 = \
K_3 = \
K_4 = \
K_5 = \
K_6 = \
K_7 = \
K_8 = \
K_RETURN = \
K_ESCAPE = \
K_UP = \
K_DOWN = \
K_LEFT = \
K_RIGHT = \
KEYUP = \
KEYDOWN = \
MOUSEMOTION = \
MOUSEBUTTONDOWN = \
MOUSEBUTTONUP = \
VIDEORESIZE = \
FULLSCREEN = \
DOUBLEBUF = \
HWSURFACE = \
OPENGL = \
RESIZABLE = \
NOFRAME = \
QUIT = \
BLEND_RGBA_ADD = None # type: int

KMOD_NONE = KMOD_LSHIFT = KMOD_RSHIFT = KMOD_SHIFT = KMOD_CAPS = \
KMOD_LCTRL = KMOD_RCTRL = KMOD_CTRL = KMOD_LALT = KMOD_RALT = \
KMOD_ALT = KMOD_LMETA = KMOD_RMETA = KMOD_META = KMOD_NUM = KMOD_MODE = None # type: int


def init() -> None: ...


# vim: set filetype=python :
