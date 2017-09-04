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
from . import gameinfo
from . import keys
from . import setup
from . components import item, user_interface


class Control:
    def __init__(self, caption: str) -> None:
        self.quit = False
        self.dt = 0.0
        self.fps = c.FPS
        self.c_fps = 0 # Current FPS from pygame's Clock.
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.screen_surface = pygame.display.get_surface()

        self.state = None # type: State
        self.state_name = None # type: c.StateName
        self.states = {} # type: Dict[c.StateName, State]


    def game_loop(self) -> None:
        while not self.quit:
            self.update()
            pygame.display.update()
            self.dt = self.clock.tick(self.fps)
            self.c_fps = self.clock.get_fps()

            # Sync threads with main thread.
            if self.state_name == c.StateName.COMMONAREA:
                while not self.state.game_info.thread_queue.empty():
                    t = self.state.game_info.thread_queue.get()
                    t.join()

        # When the game loop exits, let state clean up game info.
        return self.state.cleanup()


    def event_loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            else:
                self.state.game_info.inp.update(event)


    def update(self) -> None:
        """ Connects to the main game loop. """
        self.event_loop()

        # This is time since start time. Will need this later but not now.
        self.game_time = pygame.time.get_ticks()

        if self.state.quit:
            self.quit = True
        elif self.state.state_done:
            self.flip_state()

        self.state.update(self.screen_surface, self.dt, self.game_time, self.c_fps)

        # In Game User Interface.
        self.game_ui.update(self.screen_surface, self.state_name, self.state.game_info, self.state.game_info.item_gen_proc.drop)

        # End of frame. Do resets.
        self.state.game_info.inp.reset()
        setup.screen_size.reset()


    def setup_states(self, states, start_state) -> None:
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        print("Initial state in control object: {}".format(self.state_name))


    def setup_game_ui(self) -> None:
        self.game_ui = user_interface.GameUI()


    def flip_state(self) -> None:
        previous = self.state_name
        self.state_name = self.state.next

        # Get game_info and cleanup before setting new state
        game_info = self.state.dump_game_info()
        self.state.cleanup()

        self.state = self.states[self.state_name]

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
        self.game_info = gameinfo.GameInfo(
            dt = 0,
            game_time = 0,
            inp = binds.Input(),
            item_gen_proc = item.ItemGenerator(),
        )


    def dump_game_info(self) -> gameinfo.GameInfo:
        return self.game_info


    def call_cleanups(self) -> None:
        """
        If the item in game_info is an object (a.k.a. has the __class__
        attribute) then call its cleanup method.
        """
        for k, v in self.game_info.items():
            if hasattr(v, "__name__"):
                # Mypy doesn't  like this call because I'm assuming object
                # has a cleanup method. It isn't guarenteed to, but I can
                # enforce that it does. Ignore the type.
                v.cleanup() # type: ignore


    def cleanup(self) -> None:
        """
        This must be called to give the objects in the game info
        a chance to cleanup.
        """
        self.call_cleanups()

        # I only need to save the npc locations when
        #self.game_info.npc_group = self.npc_group
        # mainmenu won't have noc_group, not sure what to do.


    def startup(self, game_info: gameinfo.GameInfo) -> None:
        raise NotImplementedError


    def update(self, surface: pygame.Surface, dt: int) -> None:
        raise NotImplementedError
