from typing import Optional, Union, Tuple


class Rect:
    def __init__(self,
            left: Union[int, Tuple[int, int]],
            top: Union[int, Tuple[int, int]],
            width: Optional[int],
            height: Optional[int]) -> None:
        self.x = None # type: int
        self.y = None # type: int
        self.center = None # type: Tuple[int, int]
        self.centerx = None # type: int
        self.centery = None # type: int
        self.left = None # type: int
        self.right = None # type: int
        self.top = None # type: int
        self.bottom = None # type: int
        self.w = self.width = None # type: int
        self.h = self.height = None # type: int


# vim: set filetype=python :
