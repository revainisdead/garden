from typing import Optional, Dict, Set, Tuple

import json
import os

import pygame


class Keybinds:
    """
    Default keybinds must be in the format:
        <action>: <key>

    So that in the options menu, the player can change which key is
    associated with that action. The rest of the game will only know
    of the action occuring. They must supply the action as strings
    to the Input read-only singleton.
    """
    def __init__(self) -> None:
        self.__default_keybinds = {
            "move_up": (pygame.K_w,
            "move_down": pygame.K_s,
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "escape": pygame.K_ESCAPE, # Reserved: no action
            "enter": pygame.K_RETURN, # Reserved: no action
            "camera_up": pygame.K_UP,
            "camera_down": pygame.K_DOWN,
            "camera_left": pygame.K_LEFT,
            "camera_right": pygame.K_RIGHT,
            "arrow_up": pygame.K_UP, # Reserved: no action
            "arrow__down": pygame.K_DOWN, # Reserved: no action
            "arrow__left": pygame.K_LEFT, # Reserved: no action
            "arrow_right": pygame.K_RIGHT, # Reserved: no action
            "cut": pygame.K_1,
            "tree": pygame.K_2,
            "search": pygame.K_3,
            "flip": pygame.K_4,
            "five": pygame.K_5, # undef
            "six": pygame.K_6, # undef
            "seven": pygame.K_7, # undef
            "eight": pygame.K_8, # undef
        } # type: Dict[str, Tuple[int, ...]]

        conf_name = "keys_config.json"
        self.__conf_path = os.path.join("conf", conf_name)
        self.keybinds = self.__initial_conf_load()

        if self.keybinds is None:
            # For use in game.
            self.keybinds = self.__default_keybinds

        self.__used_keys = self.gather_used_keys()


    def gather_used_keys(self) -> Set[int]:
        used_keys = [] # type Set[int]

        for keys in self.keybinds.values():
            for key in keys:
                self.used_keys.append(key)

        return used_keys


    def change_key(action: str, new_key: Tuple[int, ...]) -> bool:
        """ Returns whether the change was successful. """
        if key in self.__used_keys:
            return False
        else:
            self.keybinds[action] = new_keys
            return True


    def does_new_key_exist(self, key: int) -> bool:
        return key in self.__used_keys


    def __initial_conf_load(self) -> Optional[Dict[str, int]]:
        """ Load keys_config if exists and if not, dump default keybinds. """
        binds_temp = None
        if os.path.exists(self.__conf_path):
            with open(self.__conf_path, "r") as f:
                data = json.loads(f.read()) # Load string and save into dict.
                binds_temp = data

                if binds_temp:
                    # If file exists, check if the length of the default keybinds
                    # has increased by comparing the keybinds from the file,
                    # so that we can rewrite it.
                    if len(self.__default_keybinds) > len(binds_temp):
                        # Warning: this resets all the users keybinds
                        # to the default. Will be important later to
                        # only set to default any new keys added.
                        self.reset_to_defaults()

                        # Also need to reset binds_temp to None, so that the
                        # run-time keybinds gets reset to the default values as well.
                        binds_temp = None

        else:
            self.reset_to_defaults()

        return binds_temp


    def reset_to_defaults(self) -> None:
        """ Convert keybinds file back to defaults"""
        with open(self.__conf_path, "w") as f:
            binds_temp = self.__default_keybinds
            f.write(json.dumps(binds_temp))
