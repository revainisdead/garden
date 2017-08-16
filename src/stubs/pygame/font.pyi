from typing import Tuple

from . surface import Surface


class Font:
    def __init__(self,
            path: str,
            size: int) -> None: ...
    def render(self,
            text: str,
            antialias: bool,
            color: Tuple[int, ...],
            text_background_color: Tuple[int, ...]=None) -> Surface: ...


# vim: set filetype=python :
