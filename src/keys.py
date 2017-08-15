from typing import Optional, Dict

import json
import os

import pygame as pg


class Keybinds:
    def __init__(self) -> None:
        self.__default_keybinds = {
            "up": pg.K_w,
            "down": pg.K_s,
            "left": pg.K_a,
            "right": pg.K_d,
            "escape": pg.K_ESCAPE,
            "enter": pg.K_RETURN,
            "arrow_up": pg.K_UP,
            "arrow_down": pg.K_DOWN,
            "one": pg.K_1,
            "two": pg.K_2,
        }

        conf_name = "keys_config.json"
        self.__conf_path = os.path.join("conf", conf_name)
        self.keybinds = self.__initial_conf_load()

        if self.keybinds is None:
            # For use in game.
            self.keybinds = self.__default_keybinds


    def __initial_conf_load(self) -> Optional[Dict[str, int]]:
        """ Load keys_config if exists and if not, dump default keybinds. """
        binds_temp = None
        if os.path.exists(self.__conf_path):
            with open(self.__conf_path, "r") as f:
                data = json.loads(f.read()) # Load string and save into dict.
                print(data)
                binds_temp = data
        else:
            self.reset_to_defaults()

        return binds_temp


    def reset_to_defaults(self) -> None:
        """ Convert keybinds file back to defaults"""
        with open(self.__conf_path, "w") as f:
            binds_temp = self.__default_keybinds
            f.write(json.dumps(binds_temp))
