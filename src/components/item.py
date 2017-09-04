"""
Item workflow.

"""
from typing import Dict, Tuple

import pygame

import enum
import random
import uuid

from . import errors
from . import helpers

from .. import constants as c
from .. import setup
from .. import tools


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


# All stats can be ON all items.
# It's only on application do they
# matter if it's for worker for player or etc.
class Stat(enum.Enum):
    WRK_MV_SPEED = 0
    PLY_MV_SPEED = 1
    WRK_GATHER_SPEED = 2
    PLY_GATHER_SPEED = 3
    NODE_RESPAWN_RATE = 4
    WATER_WALKING = 5
    CHOP = 6
    ITEM_DROP_RATE = 7
    RARE_ITEM_CHANCE = 8

stat_readable_names = {
    Stat.WRK_MV_SPEED: "Worker move speed",
    Stat.PLY_MV_SPEED: "Player move speed",
    Stat.WRK_GATHER_SPEED: "Worker gather speed",
    Stat.PLY_GATHER_SPEED: "Player gather speed",
    Stat.NODE_RESPAWN_RATE: "Node respawn rate",
    Stat.WATER_WALKING: "Skill: Water walking",
    Stat.CHOP: "Skill: Chop tree",
    Stat.ITEM_DROP_RATE: "Item drop rate",
    Stat.RARE_ITEM_CHANCE: "Rare item chance",
}


# EQ_ITEM
class ItemType(enum.Enum):
    WORKER = 0
    EQUIPMENT = 1


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
    def __init__(self, pos: Tuple[int, int], values: Dict[str, Any]) -> None:
        super().__init__()

        self.__set_values(values)

        sprite = setup.GFX[self.__icon]

        self.image = helpers.get_image(0, 0, c.ORIGINAL_ICON_SIZE, c.ORIGINAL_ICON_SIZE, sprite, mult=c.ITEM_MULT)
        self.image = tools.colorize_quality([self.image], quality_colors[self.__quality])[0]

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


    def __set_values(values: Dict[str, Any]:
        """ Interfaces directly to ```ItemGenerator.drop``` """
        self.__quality = values["quality"]
        self.__icon = values["icon"]
        self.__name = values["name"]
        self.__full_name = str(self.__quality + " " + self.__name)
        self.__item_type = values["item_type"]
        self.__stats_allowed = values["stats_allowed"]
        self.stats = values["stats"]


        # Workers need "people icons" and items "item icons".
        self.type = ItemType.WORKER

        # Could hold data and access attributes through it
        # Or add attributes directly onto this item


    def __get_rand_item(self) -> str:
        i = random.randint(0, len(self.item_names) - 1)
        return list(self.item_names)[i]


    def __get_rand_quality(self) -> str:
        i = random.randint(0, len(qualities) - 1)
        return qualities[i]


    def __gen_stats(self) -> Dict[Stat, float]:
        stats = {} # type: Dict[Stat

        for stat in self.__stat_names:
            low, high = stat_ranges[stat]
            if low and high < 1:
                # Stat ranges are percentages.
                low = int(low*100)
                high = int(high*100)
                value = random.randint(low, high)/100
            elif low == 0 and high == 1:
                # Stat range is False to True.
                value
            else:
                value = random.randint(low, high + 1)

            stats[stat] = value

        print(stats)
        return stats


    #def __setattr__
    #def __getattr__



# learn factory first.
# drop_item() -> Item() # generate random item
#

class ItemGenerator(threading.Thread):
    """
    - Holds all item templates.
    - Creates new, random items.

    Intended to be stored in the GameInfo object.

    Spawn this daemon and call ```drop``` to receive
    a new item.
    """
    daemon = True

    def __init__(self) -> None:
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
        self.item_map = {
            "Man": [Stat.WRK_MV_SPEED],
            "Woman": [Stat.WRK_MV_SPEED],
        } # type: Dict[str, List[Stat]]

        # Quality scale: Do the stat ranges {this}
        #                many times. 1 - 10.
        # list(qualities.keys())[0-9]
        self.quality_colors = {
            "Enslaving": c.DIRTY_GRAY,
            "Sacrificial": c.MAROON,
            "Arduous": c.BROWN,
            "Artistic": c.BLUE,
            "Organic": c.BACTERIA,
            "Collective": c.TEAL,
            "Synergistic": c.ORANGE,
            "Burning": c.MAGENTA,
            "Bountiful": c.LIME_GREEN,
            "Godly": c.DARK_YELLOW,
        }
        self.qualities = [
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

        # Stat: Tuple[Low_range, High_range]
        self.stat_ranges = {
            Stat(0): (1, 2),
            Stat(1): (1, 2),
            Stat(2): (0.05, 0.07),
            Stat(3): (0.01, 0.02),
            Stat(4): (0.01, 0.02),
            Stat(5): (0, 1),
            Stat(6): (0, 1),
        } # type: Dict[str, Tuple[int, int]]

        self.templates = None # type: List[ItemTemplate]

        # Create all game templates here.
        self.create_templates()

        self.item_names = [] # type: List[str]

        # After all items have been created.
        self.remove_build_data()


    def __new_item(self, props: List[str]) -> None:
        self.item_names.append(props[0])

        self.templates.append(ItemTemplate({
                "name": props[0],
                "stats_allowed": props[1],
                "icon": props[2],
                "item_type": props[3],
            }))


    def create_templates(self) -> None:
        """
        Easy, in-one-spot way of adding new item templates
        to the game.

        There are data structures used to add new items,
        and data structures that get applied to new items
        once they are defined.

        Here we are creating new item types or templates,
        that get random attributes added to it once a new
        item is requested.
        """
        self.__new_item([
                "Man",
                [Stat.WRK_MV_SPEED],
                "team_icon",
                ItemType.WORKER,
            ])
        self.__new_item([
                "Woman",
                [Stat.WRK_MV_SPEED],
                "team_icon",
                ItemType.WORKER,
            ])
        self.__new_item([
                "Vindicator",
                [Stat.WRK_MV_SPEED],
                "skeleton_king_icon",
                ItemType.WORKER,
            ])
        self.__new_item([
                "Weeds",
                [Stat.WRK_MV_SPEED],
                "small_weeds_icon",
                ItemType.EQUIPMENT,
            ])
        self.__new_item([
                "Gem",
                [Stat.WRK_MV_SPEED],
                "gem_icon",
                ItemType.EQUIPMENT,
            ])
        self.__new_item([
                "Moon boots",
                [Stat.WRK_MV_SPEED],
                "moonboots_icon",
                ItemType.EQUIPMENT,
            ])


    def drop(self) -> Item:
        # select random template in self.templates
        template = self.templates[random.randint(0, len(self.templates) - 1)]

        values = self.__gen_stats(template)
        item = Item(values)

        # create temp item
        # generate random stats for item
        # store stats in item
        # return item

        # CHANCE TO DROP
        # Factor in "magic find"
        # "Item drop rate" - Chance to get item?
        # - Chance to get a "more rare" item?
        # - Chance to increase to gotten item's rarity?
        #

        # Can return None
        # Chance to get rare item affected by player's current stats


        # inject random values ->
        # name
        # quality
        # stat values
        # number of stats
        pass


    def __gen_stats(self, template: ItemTemplate) -> None:
        stats = self.__gen_stats()

        values = {
            "quality": self.__get_rand_quality()
            "icon": template["icon"]
            "name": template["name"]
            "item_type": template["item_type"]
            "stats_allowed": template["stats_allowed"]
            "stats": stats,


    def __get_rand_quality(self) -> str:
        i = random.randint(0, len(self.qualities) - 1)
        return self.qualities[i]


    def __get_rand_name(self) -> str:
        i = random.randint(0, len(item_map.keys()) - 1)
        return list(item_map.keys())[i]


    def __gen_stats(self) -> Dict[Stat, float]:
        stats = {} # type: Dict[Stat

        for stat in self.__stat_names:
            low, high = stat_ranges[stat]
            if low and high < 1:
                # Stat ranges are percentages.
                low = int(low*100)
                high = int(high*100)
                value = random.randint(low, high)/100
            elif low == 0 and high == 1:
                # Stat range is False to True.
                value
            else:
                value = random.randint(low, high + 1)

            stats[stat] = value

        print(stats)
        return stats


    def remove_build_data(self) -> None:
        pass


class ItemTemplate:
    """
    Add a varity of items to the game.

    Raises ```InvalidData``` if incorrect data key is provided.
    """
    def __init__(self, data: Dict[str, str]) -> None:
        self.keys = [
            "name",
            "stats_allowed",
            "icon",
            "item_type",
        ]
        self.validate_data(data)


    def validate_data(self, data: Dict[str, str]) -> None:
        for v in list(data.values()):
            if not isinstance(v, str):
                raise errors.InvalidData

        try:
            # Must contain all the required keys.
            self.name = data[self.keys[0]]
            self.stats_allowed = data[self.keys[1]]
            self.icon = data[self.keys[2]]
            self.item_type = data[self.keys[3]]
        except KeyError:
            raise errors.InvalidData
