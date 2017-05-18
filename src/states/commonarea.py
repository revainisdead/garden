import pygame as pg

from .. import constants as c
from .. import setup

from .. components import player, enemy
from .. tools import State


class CommonArea(State):
    def __init__(self):
        super().__init__()
        # XXX Implement only startup when the state is switched to.
        # Currently startup is called in parent class

        self.setup_background()
        self.setup_enemies()
        self.setup_player()


    def startup(self):
        pass


    def setup_background(self):
        """Draw background"""
        self.background = setup.GFX["level_1"]
        self.background_rect = self.background.get_rect()

        # This area will be the entire background
        width = self.background_rect.width
        height = self.background_rect.height
        self.entire_area = pg.Surface((width, height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        self.viewport = setup.SCREEN.get_rect(bottom=self.entire_area_rect.bottom)


    def setup_enemies(self):
        enemy1 = enemy.Enemy(100, 100)
        enemy2 = enemy.Enemy(130, 130)

        self.enemy_group = pg.sprite.Group(enemy1, enemy2)


    def setup_player(self):
        self.player = player.Player(50, 50)

        self.player_group = pg.sprite.Group(self.player)


    def update(self, surface, keys):
        """Update the state every frame"""
        self.surface = surface

        self.handle_update(keys)
        self.blit_images(surface)


    def handle_update(self, keys):
        if keys[c.binds["up"]]:
            print("Up pressed.")
        if keys[c.binds["down"]]:
            print("Down pressed.")
        if keys[c.binds["right"]]:
            print("Right pressed.")
        if keys[c.binds["left"]]:
            print("Left pressed.")
        if keys[c.binds["escape"]]:
            self.state_done = True


    def blit_images(self, surface):
        self.entire_area.blit(self.background, self.viewport, self.viewport)
        self.player_group.draw(self.entire_area)
        self.enemy_group.draw(self.entire_area)

        surface.blit(self.entire_area, (0, 0), self.viewport)
