from typing import List, Tuple

from typing import Tuple


class Slot:
    def __init__(self) -> None:
        # stores rect
        # stores surface
        # stores image
        # move to new slot by moving rect
        #
        self.taken = False


class _SlotMesh:
    def __init__(self, size: Tuple[int, int]) -> None:
        # Anything else I could use besides a 2d list? Identifiable by pos only
        # Makes groking really difficult, and arbitrary access
        self.__slots = [[Slot() for y in range(size[0])] for x in range(size[1])] # type: List[List[Slot]]


class EquippedItems(_SlotMesh):
    def __init__(self, *args, **kwargs) -> None:
        super.__init__(*args, **kwargs)


class Backpack(_SlotMesh):
    def __init__(self, *args, **kwargs) -> None:
        super.__init__(*args, **kwargs)
