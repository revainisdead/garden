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
        # Define
        slots = [size][size] # type: List[List[Slot]]





class EquippedItems(_SlotMesh):
    def __init__(self) -> None:
        super.__init__(*args, **kwargs)


class Backpack(_SlotMesh):
    def __init__(self) -> None:
        super.__init__(*args, **kwargs)
