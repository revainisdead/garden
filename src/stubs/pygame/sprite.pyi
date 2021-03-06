from typing import Any, Optional, Iterator, Iterable

from . rect import Rect


def spritecollideany(sprite: Sprite, group: Group, collided: Any=None) -> Optional[Sprite]: ...


class Sprite:
    def __init__(self, *groups: Group) -> None:
        self.rect = None # type: Rect

    def get_rect(self) -> Rect: ...
    def add(self, *groups: Group) -> None: ...
    def kill(self) -> None: ...


class Group(Iterable[Sprite]):
    def __init__(self, *sprites) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __next__(self) -> Sprite: ...
    def __len__(self) -> int: ...
    def __contains__(self, s: object) -> bool: ...
    def add(self, *sprites: Sprite) -> None: ...
    def update(self, *args) -> None: ...
    def draw(self, Surface) -> None: ...


# vim: set filetype=python :
