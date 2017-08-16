from typing import Tuple

from . surface import Surface


def scale(Surface, new_size: Tuple[int, int], dest_surf: Surface=None) -> Surface: ...
def flip(Surface, xbool: bool, ybool: bool) -> Surface: ...
def rotate(Surface, angle: int) -> Surface: ...

# vim: set filetype=python :
