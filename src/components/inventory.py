from typing import Optional, List, Tuple

from typing import Tuple

import pygame

from . import item

from .. import binds
from .. import constants as c
from .. import setup


class SlotTaken(Exception): pass


class Slot:
    def __init__(self, pos: Tuple[int, int]) -> None:
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

        self.__last_pos = None

        # Get a rect to draw the slot background.
        self.bg_rect = self.create_bg(pos)


    def create_bg(self, pos: Tuple[int, int]) -> pygame.rect.Rect:
        return pygame.rect.Rect(pos, (c.SLOT_SIZE, c.SLOT_SIZE))


    def update(self, screen: pygame.surface.Surface) -> None:
        # ONLY UPDATE IF SLOTMESH SAYS IT NEEDS TO CHANGE

        pygame.draw.rect(screen, c.BLACK, self.bg_rect)


    def get_rect(self) -> Optional[pygame.rect.Rect]:
        try:
            return self.item.rect
        except AttributeError:
            return None


    def reset(self) -> None:
        r = self.get_rect()
        if r:
            r.x, r.y = self.__last_pos


    def drop(self, item: item.Item, pos: Tuple[int, int]) -> None:
        """
        If spot is taken, this will throw ```SlotTaken```
        """
        if self.taken:
            raise SlotTaken
        else:
            self.taken = True
            r = self.get_rect()
            if r:
                r.x, r.y = pos

        self.item = item


    def pickup(self, pos) -> None:
        """ Pickup is not equivalent to drag.

        This is because when it is picked up, we need to get the location,
        in case it's dropped on a taken slot or dropped where there is no
        slot, then we can reset the position.
        """
        r = self.get_rect()
        if r:
            # Save the current item position
            self.__last_pos = (r.x, r.y)

            # Move center of item to mouse pos
            r.centerx, r.centery = pos


    def drag(self, pos: Tuple[int, int]) -> None:
        self.rect.x, self.rect.y = pos


class _SlotMesh:
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int]) -> None:
        # Anything else I could use besides a 2d list? Identifiable by pos only
        # Makes groking really difficult, and arbitrary access

        self.__slots = self.__create_slots(pos, size)

        self.__hide = False
        self.__drag_slot = None # type: Optional[Slot]


    def __create_slots(self, pos: Tuple[int, int], size: Tuple[int, int]) -> List[Slot]:
        #self.__slots = [[Slot() for y in range(size[1])] for x in range(size[0])]
        slots = [] # type: List[List[Slot]]

        x_diff = c.SLOT_OFFSET
        y_diff = c.SLOT_OFFSET

        p_x, p_y = pos
        s_x, s_y = size

        # Make a copy of the starting x value
        orig_x = p_x
        for y in range(s_y):
            # Slots is a list of lists, create tmp list.
            tmp = []

            # Reset x to original x and increase y
            p_x = orig_x
            p_y += (y_diff + c.SLOT_SIZE)
            for x in range(s_x):
                tmp.append(Slot((p_x, p_y)))
                p_x += (x_diff + c.SLOT_SIZE)

            slots.append(tmp)
        return slots


    def update(self, screen: pygame.surface.Surface, inp: binds.Input) -> None:
        changed = self.handle_state(inp)
        #if changed:
        self.update_slots(screen)


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
                s.pickup(lmc)

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
                if self.__drag_slot:
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
                r = s.get_rect()
                if r:
                    if r.collidepoint(pos):
                        return s
        return None


    def update_slots(self, screen: pygame.surface.Surface) -> None:
        for slot_list in self.__slots:
            for s in slot_list:
                s.update(screen)



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
        self.__setup_meshes()

        self.__panel = SidePanel(c.SIDE_PANEL_WIDTH)
        self.__open = True

        self.__items = self.__create_items()


    # XXX: Later the items will be created on a random chance
    #      when gathering nodes, and should be placed in the next
    #      available slot.
    def __create_items(self) -> List[item.Item]:
        items = [] # type: List[Item]
        for name in item.item_map.keys():
            print(name)
            items.append(item.Item(100, 100, name))
        return items


    def __setup_meshes(self) -> None:
        # Start y value from 0, x is constant
        screenw = setup.screen_size.get_width()
        x = screenw - c.MESH_X_OFFSET

        y = c.MESH_Y_OFFSET
        self.backpack = Backpack((x, y), (6, 5))
        y += c.MESH_Y_OFFSET + 6*c.SLOT_SIZE # 6: number of backpack x slots
        self.equipped = EquippedItems((x, y), (6, 3))
        y += c.MESH_Y_OFFSET + 3*c.SLOT_SIZE # 3: number of equipped x slots
        self.workers = Workers((x, y), (6, 1))



    def switch(self) -> None:
        self.__open = not self.__open
        self.backpack.switch()
        self.equipped.switch()
        self.workers.switch()


    # Wherever update is called from can access game_info,
    # pass the keybinds object in game_info in.
    def update(self, screen: pygame.Surface, inp: binds.Input) -> None:
        self.handle_state(inp)

        if self.__open:
            self.__panel.update(screen)
            self.backpack.update(screen, inp)
            self.equipped.update(screen, inp)
            self.workers.update(screen, inp)

        if setup.screen_size.changed():
            self.__setup_meshes()


    def handle_state(self, inp: binds.Input) -> None:
        if inp.pressed("toggle_panel"):
            self.switch()
