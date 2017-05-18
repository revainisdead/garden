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

        # The first state should call startup itself
        self.startup()


    def startup(self):
        self.setup_background()
        self.setup_enemies()
        self.setup_player()

        self.state = c.MainState.COMMONAREA


    def setup_background(self):
        """Draw background"""
        self.background = setup.GFX["tile_map_silver"]
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

        self.handle_states(keys)
        self.blit_images(surface)


    def handle_states(self, keys):
        # Handle OTHER states (not level states)
        # Like running, paused, dead

        # if self.time_state == c.TimeState.RUNNING:
        self.update_sprites(keys)

    def update_sprites(self, keys):
        self.enemy_group.update()
        self.player_group.update(keys)



    def blit_images(self, surface):
        self.entire_area.blit(self.background, self.viewport, self.viewport)
        self.player_group.draw(self.entire_area)
        self.enemy_group.draw(self.entire_area)

        surface.blit(self.entire_area, (0, 0), self.viewport)
