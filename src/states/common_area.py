from .. components import enemy
from .. tools import State


class CommonArea(State):
    def __init__(self):
        super().__init__()

    def startup(self):
        print("Creating enemies in common area startup")
        self.setup_enemies()

    def setup_enemies(self):
        enemy1 = enemy.Enemy(100, 100)
        print("Created an enemy: {}".format(enemy1))

    def update(self, surface, keys):
        self.surface = surface
        self.keys = keys

        print("Common area state updated.")


