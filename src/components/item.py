"""
Item workflow.

"""
from typing import Dict

import pygame

import enum
import random
import uuid

from . import helpers

from .. import constants as c
from .. import setup


# XXX: Colorize items randomly, or based on quality?
# options
# - keep the outer black, change the white to a random color
# - change both the outer and inner to a random color
# - make the icon a color representing quality:
#       - make the inner the color
#       - and the outer the same color but some shades darker.
#       - looks embossed and clearly communicates rarity.


# XXX: Starting items:
#       boots: water walking
#       axe: cut trees


class Stat(enum.Enum):
    WRK_MV_SPEED = 0
    PLY_MV_SPEED = 1
    WRK_GATHER_SPEED = 2
    PLY_GATHER_SPEED = 3
    NODE_RESPAWN_RATE = 4
    WATER_WALKING = 5
    CHOP = 6


class ItemType(enum.Enum):
    WORKER = 0
    EQ_ITEM = 1


class Qlty(enum.Enum):
    Enslaving = 0
    Sacrificial = 1
    Arduous = 2
    Artistic = 3
    Organic = 4
    Collective = 5
    Synergistic = 6
    Burning = 7
    Bountiful = 8
    Godly = 9


qualities = [
    "Enslaving",
    "Sacrificial",
    "Arduous",
    "Artistic",
    "Organic",
    "Collective",
    "Synergistic",
    "Burning",
    "Bountiful",
    "Godly",
]

# Maps 1 to 1 to ```class Quality```
quality_color = [
    c.BLACK,
] # List[Tuple[int, int, int]]


# Stat: Tuple[Low_range, High_range]
stat_ranges = {
    Qlty(0): (1, 2),
    Qlty(1): (1, 2),
    Qlty(2): (1, 2),
} # type: Dict[str, Tuple[int, int]]


# Noun: List[Stats]
# Notes:
#     - This is all the stats this item can have.
#       There will still be only a random number of
#       the stats on the finished item.
#     - Use mostly gender bias names, and later can check
#       specifically for man, woman, etc.
#     - Can move these around feely, as long as the length
#       of the dict doesn't change. If it does at the icon
#       name to item_icon.
item_map = {
    "Man": [Stat.WRK_MV_SPEED],
    "Woman": [Stat.WRK_MV_SPEED],
    "Vindicator": [Stat.WRK_MV_SPEED, Stat.PLY_MV_SPEED],

    "Weeds": [Stat.NODE_RESPAWN_RATE],
    "Gem": [Stat.WRK_MV_SPEED],
    "Moon boots": [Stat.WATER_WALKING]
} # type: Dict[str, List[Stat]]


# Also need to map the item names to their icons.
item_icon = {
    "Man": "team_icon",
    "Woman": "team_icon",
    "Vindicator": "team_icon",
    "Team": "team_icon",

    "Gravekeeper": "gem_icon",
    "Weeds": "gem_icon",
    "Gem": "gem_icon",
    "Moon boots": "moonboots_icon",
} # type: Dict[str, str]


class Item(pygame.sprite.Sprite):
    """
    Item's have:
        Static:
            Name, "<adjective> <noun>"
            Range of stats

        Random
            Number of stats
            Type of stat
            Stat values

    - Name noun associated with certain icon
    - Name adjective associated with quality
    """
    def __init__(self, x: int, y: int, item_name: str) -> None:
        super().__init__()
        sprite = setup.GFX[item_icon[item_name]]

        self.image = helpers.get_image(0, 0, 32, 32, sprite, mult=c.BUTTON_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.__quality = self.__get_rand_quality()
        self.__item_name = self.__get_rand_item()
        self.__item_qualities = item_map[self.__item_name]
        self.__stats = self.__gen_stats()

        self.__name = str(self.__quality + self.__item_name)

        # Id should be unique and is used to identify this specific item.
        #self.__id = uuid.uuid()
        # Necessary? or just hash the quality and the stats together

        # Workers need "people icons" and items "item icons".
        self.type = ItemType.EQ_ITEM

        # Could hold data and access attributes through it
        # Or add attributes directly onto this item


    def __get_rand_item(self) -> str:
        x = random.randint(0, len(item_map.keys()) - 1)
        return list(item_map.keys())[x]


    def __get_rand_quality(self) -> str:
        x = random.randint(0, len(qualities) - 1)
        return qualities[x]


    def __gen_stats(self) -> Dict[Stat, float]:
        return {
            Stat.CHOP: 1,
        }


    #def __setattr__
    #def __getattr__



# learn factory first.
# drop_item() -> Item() # generate random item
#

