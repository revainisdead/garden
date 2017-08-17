from typing import overload, Optional, Union, Tuple


class Rect:
    x = None # type: int
    y = None # type: int
    center = None # type: Tuple[int, int]
    centerx = None # type: int
    centery = None # type: int
    left = None # type: int
    right = None # type: int
    top = None # type: int
    bottom = None # type: int
    w = width = None # type: int
    h = height = None # type: int

    @overload
    def __init__(self,
            left: int,
            top: int,
            w: int,
            h: int) -> None: ...

    @overload
    def __init__(self,
            left_top: Tuple[int, int],
            w_h: Tuple[int, int]) -> None: ...

    def colliderect(self, Rect) -> bool: ...
    def collidepoint(self, x: Union[int, Tuple[int, int]], y: Optional[int]) -> bool: ...


# vim: set filetype=python :
