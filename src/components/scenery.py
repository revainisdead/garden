import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup


class Bush(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeShadow(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["tree_shadow"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeBottom(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]


        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TreeTop(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_name) -> None:
        super().__init__()
        sprite = setup.GFX[sprite_name]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # If treetop is harvested, kill it's shadow
        # If treetop is harvested, how to know whether to draw it? Need public method to see if it needs to be drawn


    def update(self) -> None:
        self.handle_state()


    def handle_state(self) -> None:
        if self.state == c.CropState.HARVESTED:
            # Track time and regrow
            pass
        else:
            pass


class FenceLink(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["fence_link"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class FenceEnd(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        sprite = setup.GFX["fence_end"]

        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
