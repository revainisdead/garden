from typing import Any, Tuple

from . rect import Rect


HWSURFACE = None # type: Any
SRCALPHA = None # type: Any


class Surface:
    def __init__(self,
            area: Tuple[int, int]) -> None: ...

    def blit(self, surf: "Surface", rect1: Rect, rect2: Rect) -> None: ...

# vim: set filetype=python :
