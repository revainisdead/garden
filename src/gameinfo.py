from typing import Any


class CustomDict(dict):
    """
    Wrapper around dict that allows accessing the object's attributes
    by dot access as opposed to strings as keys.

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


class GameInfo(CustomDict): pass
