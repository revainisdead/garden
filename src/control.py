# Module Import Order:
# typing
# python
# third-party
# local relative import (.)
#   - same folder
#   - deeper folder
# parent relative import (..)
#   - same folder
#   - deeper folder
#
# Rule: unqualified imports before qualified
#   Ex. from module import class
#       import module
from typing import Any, Optional, Callable, Dict

import time

import pygame

from . import binds
from . import constants as c
from . import keys
from . import setup
from . components import user_interface, util


class GameInfo(dict):
    """
    Wrapper around dict that allow dot access for game info type safety.

    Usage:
        >>> game_info = GameInfo(title="test", players=5)
        >>> game_info.title
        test
        >>> game_info.players
        5
        >>> game_info.keys()
        dict_keys(['title', 'players'])
        >>> game_info.values()
        dict_values(['test', 5])
        >>> json.dumps(g__e_info)
        '{"title": "test", "players": 5}'
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    def __getitem__(self, *args, **kwargs):
        """ Overwrite the ability to access members using square brackets. """
        raise KeyError

    def __getattr__(self, key: str) -> Any:
        return self.get(key)

    def __setattr__(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)


class Control:
    def __init__(self, caption: str) -> None:
        self.quit = False
        self.dt = 0.0
        self.fps = c.FPS
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.screen_surface = pygame.display.get_surface()

        self.state = None # type: State
        self.state_name = None # type: c.StateName
        self.state_dict = {} # type: Dict[c.StateName, State]


    def game_loop(self) -> None:
        while not self.quit:
            self.update()
            pygame.display.update()
            self.dt = self.clock.tick(self.fps)

        # When the game loop exits, let game info clean itself up.
        return self.state.cleanup()


    def event_loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            else:
                binds.INPUT.update(event)


    def update(self) -> None:
        """Connects to the main game loop.
        Do any updates needed.
        """
        self.event_loop()

        self.dt = pygame.time.get_ticks()
        if self.state.quit:
            self.quit = True
        elif self.state.state_done:
            self.flip_state()

        self.state.update(self.screen_surface, self.dt)

        # In Game User Interface.
        self.game_ui.update(self.screen_surface, self.dt, self.state_name)

        binds.INPUT.reset()


    def setup_states(self, state_dict, start_state) -> None:
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        print("Initial state in control object: {}".format(self.state_name))


    def setup_game_ui(self) -> None:
        self.game_ui = user_interface.GameUI()


    def flip_state(self) -> None:
        previous = self.state_name
        self.state_name = self.state.next

        # Get game_info and cleanup before setting new state
        game_info = self.state.dump_game_info()
        self.state.cleanup()

        self.state = self.state_dict[self.state_name]

        # Startup state when switching to it with the dumped game info.
        self.state.startup(game_info)
        print("State switched to: {}".format(self.state_name))

        self.state.previous = previous


class State:
    def __init__(self) -> None:
        # Quit everything
        self.quit = False

        # Quit this state
        self.state_done = False

        self.next = None # type: c.StateName
        self.previous = None # type: c.StateName

        # These are things that every state needs.
        self.game_info = GameInfo(
            input = binds.Input()
        )


    def dump_game_info(self) -> GameInfo:
        return self.game_info


    def cleanup(self) -> None:
        """
        This must be called to give the objects in the game info
        a chance to cleanup, let the game info object handle that.
        """
        for k, v in self.game_info.items():
            if isinstance(v, object):
                # Mypy doesn't  like this call because I'm assuming object
                # has a cleanup method. It isn't guarenteed to, but I can
                # enforce that. Ignore the type.
                v.cleanup() # type: ignore


    def startup(self, game_info: GameInfo) -> None:
        raise NotImplementedError


    def update(self, surface: pygame.Surface, dt: int) -> None:
        raise NotImplementedError
