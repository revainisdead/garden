from . import constants as c
from . import setup
from . import tools

from . states import commonarea


def main():
    state_dict = {
        c.States.COMMONAREA: commonarea.CommonArea(),
    }

    control = tools.Control("Game Caption")

    control.setup_states(state_dict, c.States.COMMONAREA)
    control.game_loop()




if __name__ == "__main__":
    main()
