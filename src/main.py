from . import constants as c
from . import setup
from . import tools

from . states import common_area


def main():
    state_dict = {
        c.States.COMMON_AREA: common_area.CommonArea(),
    }

    control = tools.Control("Game Caption")

    control.setup_states(state_dict, c.States.COMMON_AREA)
    control.game_loop()




if __name__ == "__main__":
    main()
