from typing import Optional, Dict

import json
import os

import pygame as pygame


class Keybinds:
    def __init__(self) -> None:
        self.__default_keybinds = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "escape": pygame.K_ESCAPE,
            "enter": pygame.K_RETURN,
            "arrow_up": pygame.K_UP,
            "arrow_down": pygame.K_DOWN,
            "one": pygame.K_1,
            "two": pygame.K_2,
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
                binds_temp = data
        else:
            self.reset_to_defaults()

        return binds_temp


    def reset_to_defaults(self) -> None:
        """ Convert keybinds file back to defaults"""
        with open(self.__conf_path, "w") as f:
            binds_temp = self.__default_keybinds
            f.write(json.dumps(binds_temp))
