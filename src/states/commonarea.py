import pygame as pg

from .. import binds
from .. import constants as c
from .. import setup

from .. components import player, enemy
from .. tools import State


class CommonArea(State):
    def __init__(self):
        super().__init__()


    def startup(self, game_info):
        self.game_info = game_info

        self.setup_background()
        self.setup_enemies()
        self.setup_player()
        self.glaive_group = pg.sprite.Group()

        self.state = c.MainState.COMMONAREA


    def setup_background(self):
        """Draw background"""
        self.background = setup.GFX["cloud_background"]
        self.background_rect = self.background.get_rect()

        size_delta = (int(self.background_rect.width*c.BACKGROUND_MULT), int(self.background_rect.height*c.BACKGROUND_MULT))
        self.background = pg.transform.scale(self.background, size_delta)

        self.background_rect = self.background.get_rect()
        self.entire_area = pg.Surface((self.background_rect.width, self.background_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()

        self.viewport = setup.SCREEN.get_rect(bottom=self.entire_area_rect.bottom)
        #self.viewport.x = ???


    def setup_enemies(self):
        enemy1 = enemy.Enemy(300, 300)
        enemy2 = enemy.Enemy(350, 350)

        self.enemy_group = pg.sprite.Group(enemy1, enemy2)


    def setup_player(self):
        self.player = player.Player(500, 400)

        self.player_group = pg.sprite.Group(self.player)


    def update(self, surface, keys, current_time):
        """Update the state every frame"""
        self.game_info["current_time"] = current_time

        self.update_sprites(keys)
        self.handle_states(keys)
        self.blit_images(surface)


    def handle_states(self, keys):
        # Handle OTHER states (not level states)
        # Like running, paused, dead

        # if self.time_state == c.TimeState.RUNNING:
        if keys[binds.keybinds["escape"]]:
            self.quit = True


    def update_sprites(self, keys):
        self.enemy_group.update(self.game_info["current_time"], self.glaive_group)
        self.glaive_group.update(self.game_info["current_time"])

        self.player_group.update(keys)


    def blit_images(self, surface):
        self.entire_area.blit(self.background, self.viewport, self.viewport)
        self.player_group.draw(self.entire_area)
        self.enemy_group.draw(self.entire_area)
        self.glaive_group.draw(self.entire_area)

        surface.blit(self.entire_area, (0, 0), self.viewport)
