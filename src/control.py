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
from . import setup
from . components import user_interface, util


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
        previous, self.state_name = self.state_name, self.state.next
        # Get game_info before setting new state
        game_info = self.state.dump_game_info()
        self.state = self.state_dict[self.state_name]

        # Startup state when switching to it
        self.state.startup(game_info)
        print("Main state switched to: {}".format(self.state_name))

        self.state.previous = previous


class State:
    def __init__(self) -> None:
        # Quit everything
        self.quit = False

        # Quit this state
        self.state_done = False

        self.next = None # type: c.StateName
        self.previous = None # type: c.StateName

        # XXX Make game info it's own object.
        self.game_info = {} # type: Dict[str, Any]


    def dump_game_info(self) -> Dict[str, Any]:
        return self.game_info


    def startup(self, game_info: Dict[str, Any]) -> None:
        raise NotImplementedError


    def update(self, surface: pygame.Surface, dt: int) -> None:
        raise NotImplementedError
