import pygame as pg

from .. import constants as c


class Collidable(pg.sprite.Sprite):
    """Create a collidable rect
    This sprite itself has nothing about it that prevents movement through it.
    But if the Collidable rect exists ensure that is can't be moved through.
    """
    def __init__(self, x: int, y: int, width: int=c.TILE_SIZE, height: int=c.TILE_SIZE) -> None:
        super().__init__()

        self.image = pg.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Tooltip(pg.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        sprite = setup.GFX["tooltip_bubble"]

        self.name = sprite_name
        self.image = helpers.get_image(0, 0, c.TILE_SIZE, c.TILE_SIZE, sprite, mult=c.TILE_MULT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def render_text(self) -> None:
        pass


    def scale_to_text_size(self) -> None:
        pass
