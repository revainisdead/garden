from typing import List, Tuple

from typing import Tuple

import pygame

from .. import binds
from .. import constants as c
from .. import setup


class Slot:
    def __init__(self) -> None:
        # stores rect
        # stores surface
        # stores image
        # move to new slot by moving rect
        self.taken = False
        self.item = None # type: Optional[Item]
        self.hide = False # dragging, don't dra

        #self.rect = self.item.rect


    def update(self, action: str) -> None:
        # ONLY UPDATE IF SLOTMESH SAYS IT NEEDS TO CHANGE
        pass


    def drop(self, item: _Item) -> None:
        self.taken = True

        if item:
            self.item = item


    def pickup(self) -> None: pass
    def drag(self) -> None: self.hide = True



class _SlotMesh:
    def __init__(self, size: Tuple[int, int]) -> None:
        # Anything else I could use besides a 2d list? Identifiable by pos only
        # Makes groking really difficult, and arbitrary access
        self.__slots = [[Slot() for y in range(size[0])] for x in range(size[1])] # type: List[List[Slot]]

        self.__open = True


    def update(self, inp: binds.Input) -> None:
        self.handle_state(inp)


    def handle_state(self, inp: binds.Input) -> None:
        slot_changed = False

        self.dragging 

        lmc = inp.last_mouse_click()
        lmd = inp.last_mouse_drop()
        mp = inp.mouse_pos()

        if lmc:
            s = check_slots(lmc)
            if s:
                s.pickup()

        if lmd:
            s = check_slots(lmd)
            if s:
                s.drop()

        if mp:
            s = check_slots(mp)
            if s:
                s.drag()


    def switch(self) -> None:
        self.__open = not self.__open


    def check_slots(self, pos: Tuple[int, int]) -> Optional[Slot]:
        """ Returns a slot if one contains that position.
        That was this function can be used for mousedown
        (pickup) and mouseup (dropping)"""
        x, y = *pos
        for s in self.__slots:
            if s.collidepoint(pos):
                s.dragging = True



class EquippedItems(_SlotMesh):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Backpack(_SlotMesh):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Workers(_SlotMesh):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class SidePanel:
    """
    Make a solid panel, so that slots can be transparent.
    Indicating an empty slot, and since the background of
    that is this panel, which is solid, it will look nice.
    """
    def __init__(self, width: int) -> None:
        self.width = width
        self.setup_panel()
        self.color = c.PANEL_GRAY

    def setup_panel(self) -> None:
        screenw = setup.screen_size.get_width()
        screenh = setup.screen_size.get_height()
        self.rect = pygame.Rect((screenw - self.width, 0), (self.width, screenh))

    def update(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
        if setup.screen_size.changed():
            self.setup_panel()


class Inventory:
    def __init__(self) -> None:
        self.backpack = Backpack((6, 5))
        self.equipped = EquippedItems((6, 3))
        self.workers = Workers((6, 1))

        self.__panel = SidePanel(c.SIDE_PANEL_WIDTH)
        self.__open = True


    def switch(self) -> None:
        self.__open = not self.__open
        self.backpack.switch()
        self.equipped.switch()
        self.workers.switch()


    # Wherever update is called from can access game_info,
    # pass the keybinds object in game_info in.
    def update(self, surface: pygame.Surface, inp: binds.Input) -> None:
        self.handle_state(inp)

        if self.__open:
            self.__panel.update(surface)


    def handle_state(self, inp: binds.Input) -> None:
        if inp.pressed("toggle_panel"):
            self.switch()
