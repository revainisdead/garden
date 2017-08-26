from . import constants as c
from . import control
from . import setup

from . states import commonarea
from . states import mainmenu

import sys
import traceback


def main():
    setup.start()

    states = {
        c.StateName.MAINMENU: mainmenu.MainMenu(),
        c.StateName.COMMONAREA: commonarea.CommonArea(),
    }

    game = control.Control(c.CAPTION)
    game.setup_states(states, c.StateName.MAINMENU)
    game.setup_game_ui()

    # Never let exceptions crash the game loop.
    try:
        game.game_loop()
    except:
        traceback.print_exc()

    # The game loop has quit and we still have control of the program here.
    # Do any clean up necessary before exit.
    sys.exit()


if __name__ == "__main__":
    main()
