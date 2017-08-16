from typing import Tuple


class Event:
    def __init__(self) -> None:
        self.type = None # type: int
        self.key = None # type: int
        self.size = None # type: Tuple[int, int]


# vim: set filetype=python :
