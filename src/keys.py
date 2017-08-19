from typing import Optional, Dict, Set, Tuple

import json
import os

import pygame


class Keybinds:
    """
    Default keybinds must be in the format:
        <action>: Tuple[<key>, Optional[<key>]] # XXX not enforced yet.

    So that in the options menu, the player can change which key is
    associated with that action. The rest of the game will only know
    of the action occuring. They must supply the action as strings
    to Input.
    """
    def __init__(self) -> None:
        self.__default_keybinds = {
            "move_up": (pygame.K_w,),
            "move_down": (pygame.K_s,),
            "move_left": (pygame.K_a,),
            "move_right": (pygame.K_d,),
            "escape": (pygame.K_ESCAPE,),
            "enter": (pygame.K_RETURN,),
            "camera_up": (pygame.K_UP,),
            "camera_down": (pygame.K_DOWN,),
            "camera_left": (pygame.K_LEFT,),
            "camera_right": (pygame.K_RIGHT,),
            "arrow_up": (pygame.K_UP,),
            "arrow_down": (pygame.K_DOWN,),
            "arrow_left": (pygame.K_LEFT,),
            "arrow_right": (pygame.K_RIGHT,),
            "cut": (pygame.K_1,),
            "tree": (pygame.K_2,),
            "search": (pygame.K_3,),
            "flip": (pygame.K_4,),
            "five": (pygame.K_5,),
            "six": (pygame.K_6,),
            "seven": (pygame.K_7,),
            "eight": (pygame.K_8,),
            "toggle_panel" : (pygame.K_TAB,),
        } # type: Dict[str, Tuple[int, ...]]

        conf_name = "keys_config.json"
        self.__conf_dir_path = os.path.join("conf")
        self.__conf_file_path = os.path.join("conf", conf_name)
        self.keybinds = self.__initial_conf_load()

        if self.keybinds is None:
            # For use in game.
            self.keybinds = self.__default_keybinds

        self.__used_keys = self.gather_used_keys()
        self.__dump_flag = False


    def gather_used_keys(self) -> Set[int]:
        used_keys = set() # type: Set[int]

        # Note: values is implicitly converts the tuples to lists.
        for keys in tuple(self.keybinds.values()):
            for key in keys:
                used_keys.add(key)

        return used_keys


    def change_key(self, action: str, new_key: Tuple[int, ...]) -> bool:
        """
        Change one key at a time. Recreate the tuple if key can be changed.
        Returns whether the change was successful.
        """
        if new_key in self.__used_keys:
            return False
        else:
            # XXX Mypy does not yet allowed concatention of set length
            # tuples, and it certainly does not allow concatention of
            # varaible length tuples, ignore the type for the addition.
            current_binds = self.keybinds[action]
            new_binds = current_binds + (new_key,) # type: ignore
            self.keybinds[action] = new_binds # Save new binds

            self.__dump_flag = True
            return True


    def does_new_key_exist(self, key: int) -> bool:
        return key in self.__used_keys


    def __initial_conf_load(self) -> Optional[Dict[str, Tuple[int, ...]]]:
        """ Load keys_config if exists and if not, dump default keybinds. """
        binds_temp = None
        if os.path.exists(self.__conf_file_path):
            with open(self.__conf_file_path, "r") as f:
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
            if not os.path.exists(self.__conf_dir_path):
                os.makedirs(self.__conf_dir_path)
            self.reset_to_defaults()

        return binds_temp


    def __write_config(self, data) -> None:
        with open(self.__conf_file_path, "w") as f:
            binds_temp = data
            f.write(json.dumps(binds_temp))


    def __write_current_keybinds(self) -> None:
        self.__write_config(self.keybinds)


    def reset_to_defaults(self) -> None:
        """ Convert keybinds file back to defaults"""
        self.__write_config(self.__default_keybinds)


    def dump(self) -> None:
        if self.__dump_flag:
            self.__write_current_keybinds()
