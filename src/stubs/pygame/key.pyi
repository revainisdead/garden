from typing import Sequence


def get_focused() -> bool: ...
def get_pressed() -> Sequence[bool]: ...
def get_mods() -> int: ...
def set_mods(int) -> None: ...
def set_repeat() -> None: ...
def get_repeat() -> Tuple[int, int]: ...
def name() -> str: ...


# vim: set filetype=python :
