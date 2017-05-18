from . import constants as c
from . import setup
from . import tools

from . states import commonarea
from . states import mainmenu


def main():
    state_dict = {
        c.States.MAINMENU: mainmenu.MainMenu(),
        c.States.COMMONAREA: commonarea.CommonArea(),
    }

    control = tools.Control("Garden")

    control.setup_states(state_dict, c.States.MAINMENU)
    control.game_loop()




if __name__ == "__main__":
    main()
