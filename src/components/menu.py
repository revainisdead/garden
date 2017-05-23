import pygame as pg

from .. import constants as c
from .. import setup


labels = {
    "play": "play",
    "load_game": "load game",
    "quit": "quit",
}


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()

        self.sprite = setup.GFX["green_button01"]
        self.sprite_selected = setup.GFX["green_button00"]

        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()

        # To center the menu item, take half of the width away from x.
        self.rect.x = x - self.rect.width/2
        self.rect.y = y

        self.name = name
        self.selected = False


    def load_sprites_from_sheet(self):
        frames = []
        frames.append(self.get_image(0, 0, 190, 49, self.sprite))
        frames.append(self.get_image(0, 0, 190, 49, self.sprite_selected))
        return frames


    def get_image(self, x, y, width, height, sprite):
        """Extracts from sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(sprite, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)

        size_delta = (int(rect.width*c.UI_MULT), int(rect.height*c.UI_MULT))
        image = pg.transform.scale(image, size_delta)
        return image


    def update(self, selection):
        self.handle_state(selection)


    def handle_state(self, selection):
        if selection == self.name:
            self.selected = True
            frame_index = 1
            self.image = self.frames[frame_index]
        else:
            self.selected = False
            frame_index = 0
            self.image = self.frames[frame_index]

    def render_name(self, surface):
        font = setup.FONTS["kenvector_future_thin"]
        if self.selected:
            text = font.render(labels[self.name], True, c.WHITE)
        else:
            text = font.render(labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(c.SCREEN_WIDTH/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)
