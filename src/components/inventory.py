from typing import Optional, List, Tuple

from typing import Tuple

import pygame

from . import item

from .. import binds
from .. import constants as c
from .. import setup


class SlotTaken(Exception): pass


class Slot:
    def __init__(self) -> None:
        # stores rect
        # stores surface
        # stores image
        # move to new slot by moving rect
        self.taken = False
        self.item = None # type: Optional[item.Item]
        # XXX surface should be in item because that's where the sprite
        # will be stored
        # Needed the interface to slot so that the item in this particular
        # slot can change easily


        # we need the surface here so we can get the rect and pos
        #self.surface = pygame.Surface((c.SLOT_SIZE, c.SLOT_SIZE)).convert()
        #self.rect = self.surface.get_rect()

        # when dragging, don't hide, need to draw it on mouse
        #self.hide = False # dragging, don't draw
        #self.rect = self.item.rect


    def update(self, action: str) -> None:
        # ONLY UPDATE IF SLOTMESH SAYS IT NEEDS TO CHANGE
        pass


    def drop(self, item: item.Item, pos: Tuple[int, int]) -> None:
        """
        If spot is taken, this will throw ```SlotTaken```
        """
        if self.taken:
            raise SlotTaken
        else:
            self.taken = True
            self.item.rect.x, self.item.rect.y = pos

        self.item = item


    def pickup(self) -> None:
        """ Pickup is not equivalent to drag.

        This is because when it is picked up, we need to get the location,
        in case it's dropped on a taken slot or dropped where there is no
        slot, then we can reset the position.
        """
        self.__last_pos = (self.rect.x, self.rect.y)


    def drag(self, pos: Tuple[int, int]) -> None:
        self.rect.x, self.rect.y = pos


class _SlotMesh:
    def __init__(self, size: Tuple[int, int]) -> None:
        # Anything else I could use besides a 2d list? Identifiable by pos only
        # Makes groking really difficult, and arbitrary access
        self.__slots = [[Slot() for y in range(size[1])] for x in range(size[0])] # type: List[List[Slot]]

        self.__hide = False
        self.__drag_slot = None # type: Optional[Slot]


    def update(self, inp: binds.Input) -> bool:
        return self.handle_state(inp)


    def handle_state(self, inp: binds.Input) -> bool:
        slot_changed = False

        lmc = inp.last_mouse_click()
        lmd = inp.last_mouse_drop()
        mp = inp.mouse_pos()

        if lmc:
            s = self.check_slots(lmc)
            if s:
                slot_changed = True
                s = self.__drag_slot
                s.pickup()

        if lmd:
            s = self.check_slots(lmd)
            if s:
                slot_changed = True
                try:
                    s.drop()
                except SlotTaken:
                    self.__drag_slot = None
            else:
                # Slot was not dropped on an existing slot.
                self.__drag_slot.reset()
                self.__drag_slot = None

        # For dragging, ensure there is a dragging slot at the moment.
        if mp and self.__drag_slot:
            s = self.check_slots(mp)
            if s:
                slot_changed = True
                s.drag(mp)

        return slot_changed


    def switch(self) -> None:
        self.__hide = not self.__hide


    def check_slots(self, pos: Tuple[int, int]) -> Optional[Slot]:
        """ Returns a slot if one contains that position.
        That was this function can be used for mousedown
        (pickup) and mouseup (dropping)"""
        x, y = pos
        for slot_list in self.__slots:
            for s in slot_list:
                if s.rect.collidepoint(pos):
                    return s

        return None



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

        self.__items = self.__create_items()


    # XXX: Later the items will be created on a random chance
    #      when gathering nodes.
    def __create_items(self) -> List[item.Item]:
        items = [] # type: List[Item]
        for name in item.item_map.keys():
            print(name)
            items.append(item.Item(100, 100, name))
        return items


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
            bp_change = self.backpack.update(inp)
            eq_change = self.equipped.update(inp)
            wrk_change = self.workers.update(inp)


    def handle_state(self, inp: binds.Input) -> None:
        if inp.pressed("toggle_panel"):
            self.switch()
