from . import constants as c
from . import setup
from . import tools

from . states import commonarea
from . states import mainmenu


def main():
    state_dict = {
        c.MainState.MAINMENU: mainmenu.MainMenu(),
        c.MainState.COMMONAREA: commonarea.CommonArea(),
    }

    control = tools.Control("Garden")
    control.setup_states(state_dict, c.MainState.MAINMENU)
    control.game_loop()




if __name__ == "__main__":
    main()
