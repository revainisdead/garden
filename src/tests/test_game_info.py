from typing import Any

from .. import gameinfo

import contextlib
import unittest


class TestGameInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.game_info = gameinfo.GameInfo(test="cat", test_two="dog")

    def tearDown(self) -> None:
        del self.game_info["test"]
        del self.game_info["test_two"]

        del self.game_info


    def test_attr_set_and_get(self) -> None:
        """ Dot access """
        assert(self.game_info.test == "cat")
        assert(self.game_info.test_two == "dog")

        self.game_info.new_attr = 42
        assert(self.game_info.new_attr == 42)


    def test_getitem(self) -> None:
        """ Bracket access, not allowed.

        Note: KeyError should always be raised.
              If it is not, then it succeeded,
              which is considered a failure.
        """
        try:
            t1 = self.game_info["test"] != "cat"
            t2 = self.game_info["test_two"] != "dog"
        except KeyError:
            pass
        else:
            raise Exception("GameInfo should not allow __getitem__ access.")
