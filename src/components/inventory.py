from typing import Optional, List, Tuple

import pygame

from . import item

from .. import binds
from .. import constants as c
from .. import setup


class SlotTaken(Exception): pass
class AllSlotsTaken(Exception): pass


class Slot:
    def __init__(self, pos: Tuple[int, int]) -> None:
        self.taken = False
        self.item = None # type: Optional[item.Item]
        self.pos = pos
        self.last_item = None # type: item.Item

        # Get a rect to draw the slot background.
        self.bg_rect = self.create_bg(pos)


    def create_bg(self, pos: Tuple[int, int]) -> pygame.rect.Rect:
        return pygame.rect.Rect(pos, (c.SLOT_SIZE, c.SLOT_SIZE))


    def update(self, screen: pygame.surface.Surface) -> None:
        if self.item:
            pass
        else:
            pygame.draw.rect(screen, c.BLACK, self.bg_rect)


    def get_rect(self) -> Optional[pygame.rect.Rect]:
        try:
            return self.item.rect
        except AttributeError:
            return None


    def reset(self) -> None:
        if self.last_item:
            self.item = self.last_item

            # Also must re-position self.item, since the last time we
            # saw last_item it was being dragged around.
            self.item.rect.x, self.item.rect.y = self.pos

            self.last_item = None
            self.taken = True


    def drop(self, item: item.Item) -> None:
        """
        If spot is taken, this will throw ```SlotTaken```
        """
        if self.taken:
            raise SlotTaken

        if item:
            self.item = item
            self.item.rect.x, self.item.rect.y = self.pos

            # If a set item is set, the last item must be reset as well.
            self.last_item = None
            self.taken = True


    def pickup(self, pos) -> None:
        r = self.get_rect()
        if r:
            # Save a copy of the current item
            self.last_item = self.item

            # Remove current item from slot.
            self.item = None
            self.taken = False

            # Move center of item to mouse pos
            r.centerx, r.centery = pos


    def drag(self, pos: Tuple[int, int]) -> None:
        # If slot taken, it needs to stop dragging.
        #if self.last_item and not self.taken:
        if self.last_item:
            r = self.last_item.rect
            r.x, r.y = pos


class SlotMesh:
    """
    Abstraction that holds all slots and grids of slots.
    """
    def __init__(self, pos: Tuple[int, int]) -> None:
        self.x, self.y = pos
        self.__last_h = 0

        self.__slots = [[]] # type: List[List[Slot]]
        self.flat_slots = [] # type List[Slot]

        self.__hide = False
        self.__drag_slot = None # type: Optional[Slot]


    def __create_slots(self, pos: Tuple[int, int], size: Tuple[int, int]) -> List[Slot]:
        """
        Set up slots and their positions.

        2D List comprehension example.
        ```self.__slots = [[Slot() for y in range(size[1])] for x in range(size[0])]```

        1D List comprehension example for flattening.
        ```self.flat_slots = [s for sublist in self.__slots for s in sublist]```
        """
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


    def append_grid(self, size: Tuple[int, int]) -> None:
        # Move down the grid based on the size of the last grid.
        tmp_slots = self.__create_slots((self.x, self.y), size)
        for slot_list in tmp_slots:
            self.__slots.append(slot_list)

            # Append new slot_lists to flat_slots
            for s in slot_list:
                self.flat_slots.append(s)

        # Reset last height to the current height at the end of the function.
        self.__last_h = size[1]
        self.y += c.MESH_Y_OFFSET + self.__last_h*c.SLOT_SIZE


    def update(self, screen: pygame.surface.Surface, inp: binds.Input) -> None:
        self.handle_state(inp)
        self.update_slots(screen)


    def handle_state(self, inp: binds.Input) -> None:
        lmc = inp.last_mouse_click()
        lmd = inp.last_mouse_drop()
        mp = inp.mouse_pos()

        if lmc:
            s = self.check_slots(lmc)
            if s:
                self.__drag_slot = s
                s.pickup(lmc)

        if lmd:
            s = self.check_slots(lmd)
            if s:
                if self.__drag_slot:
                    try:
                        # Drop the old item from the drag slot into the new slot s.
                        s.drop(self.__drag_slot.last_item)
                    except SlotTaken:
                        self.__drag_slot.reset()
            else:
                # Slot was not dropped on an existing slot.
                if self.__drag_slot:
                    self.__drag_slot.reset()

            # Always ensure the drag slot is reset to None on mouse up.
            self.__drag_slot = None

        # For dragging, ensure the drag slot exists.
        if mp and self.__drag_slot:
            self.__drag_slot.drag(mp)


    def switch(self) -> None:
        self.__hide = not self.__hide


    def check_slots(self, pos: Tuple[int, int]) -> Optional[Slot]:
        """ Returns a slot if one contains that position.
        This function can be used for mousedown
        (pickup) and mouseup (dropping)"""
        for slot_list in self.__slots:
            for s in slot_list:
                bg_r = s.bg_rect
                if bg_r.collidepoint(pos):
                        return s
        return None


    def update_slots(self, screen: pygame.surface.Surface) -> None:
        for slot_list in self.__slots:
            for s in slot_list:
                s.update(screen)


    def refill_slot(self, item: item.Item, s_index: int) -> None:
        """ Fill the slot that is at the given index with the item. """
        i = -1   # Count index because it's a 2D list.
        for slot_list in self.__slots:
            for s in slot_list:
                i += 1
                if i == s_index:
                    s.drop(item)
                    return


    def fill_next_slot(self, item: item.Item) -> None:
        """ Fill next open slot. """
        for slot_list in self.__slots:
            for s in slot_list:
                if not s.taken:
                    s.drop(item)
                    return
        raise AllSlotsTaken


### Slot type ###
# Equipped
# Backpack
# Workers


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
        self.__setup_mesh()

        self.__panel = SidePanel(c.SIDE_PANEL_WIDTH)
        self.__open = True

        self.item_group = pygame.sprite.Group()
        self.__items = self.__create_items()


    # XXX: Later the items will be created on a random chance
    #      when gathering nodes, and should be placed in the next
    #      available slot.
    def __create_items(self) -> List[item.Item]:
        items = [] # type: List[Item]
        flat_s = self.slot_mesh.flat_slots

        for i, name in enumerate(item.item_map.keys()):
            item_tmp = item.Item((flat_s[i].pos), name)
            items.append(item_tmp)

            self.add_item(item_tmp)
            print(item_tmp.name)
        return items


    def __setup_mesh(self) -> None:
        screenw = setup.screen_size.get_width()
        x = screenw - c.MESH_X_OFFSET
        y = c.MESH_Y_OFFSET
        num_x_slots = c.NUM_SLOTS_WIDE
        num_y_slots = 5

        self.slot_mesh = SlotMesh((x, y))
        for i in range(3):
            self.slot_mesh.append_grid((num_x_slots, num_y_slots))
            num_y_slots -= 2


    def add_item(self, item: item.Item) -> None:
        # New items always go into the backpack.
        try:
            self.slot_mesh.fill_next_slot(item)
        except AllSlotsTaken:
            pass
        else:
            self.item_group.add(item)


    def readd_item(self, item: item.Item, s_index: int) -> None:
        try:
            self.slot_mesh.refill_slot(item, s_index)
        except AllSlotsTaken:
            pass
        else:
            self.item_group.add(item)


    def __move_items(self) -> None:
        """ Move all the existing items to the new slot positions. """
        self.item_group = pygame.sprite.Group()
        flat_s = self.slot_mesh.flat_slots

        for i, item in enumerate(self.__items):
        #for i, slot in enumerate(flat_s)
            s = flat_s[i] # works because slots are filled in order, 0-1-2 etc.
            item.rect.x, item.rect.y = s.pos

            # - When the screen is resized, the slots are actually re-created.
            # So we need to add the items back in to the slots.
            # - But we need to add them back into the equivalent slot they were
            # in before.
            self.readd_item(item, i)

        # Let old slots get garbage collected.
        self.slot_mesh.flat_slots = None


    def switch(self) -> None:
        self.__open = not self.__open
        self.slot_mesh.switch()


    def update(self, screen: pygame.Surface, inp: binds.Input) -> None:
        self.handle_state(inp)

        if self.__open:
            self.__panel.update(screen)
            self.slot_mesh.update(screen, inp)
            self.item_group.draw(screen)

        if setup.screen_size.changed():
            self.__setup_mesh()
            self.__move_items()


    def handle_state(self, inp: binds.Input) -> None:
        if inp.pressed("toggle_panel"):
            self.switch()
