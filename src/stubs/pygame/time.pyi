""" When int is returned, it's returning milliseconds. """


def get_tickets() -> int: ...
def delay(int) -> int: ...
def wait(int) -> int: ...


class Clock:
    def __init__(self) -> None: ...
    def tick(self, framerate: int=0) -> int: ...
    def tick_busy_loop(self, framerate: int=0) -> int: ...
    def get_time(self) -> int: ...
    def get_rawtime(self) -> int: ...
    def get_fps(self) -> float: ...


# vim: set filetype=python :
