from typing import Any, Tuple


class Image:
    def __init__(self) -> None: ...


def merge(mode: str, bands: Tuple[int, ...]) -> Image: ...
def open(fp: str, mode: str="r") -> Image: ...

# vim: set filetype=python :
