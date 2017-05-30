import pygame as pg

from . import helpers

from .. import constants as c
from .. import setup


menu_labels = {
    "play": "play",
    "load_game": "load game",
    "quit": "quit",
}


button_names = [
    "wood_axe_icon",
]


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()

        self.sprite = setup.GFX[name]
        #self.sprite_pressed = setup.GFX["wood_axe_icon"]
        #self.pressed = False

        #self.font = setup.FONTS["kenvector_future_thin"]

        self.frames = self.load_sprites_from_sheet()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.name = name


    def load_sprites_from_sheet(self):
        frames = []
        frames.append(helpers.get_image(0, 0, 400, 400, self.sprite, mult=c.BUTTON_UI_MULT))
        #frames.append(helpers.get_image(0, 0, 400, 400, self.sprite_pressed, mult=c.BUTTON_UI_MULT))
        return frames


    def update(self, selection):
        self.handle_state()


    def handle_state(self):
        pass


    def render_name(self, surface):
        if self.pressed:
            text = self.font.render(menu_labels[self.name], True, c.WHITE)
        else:
            text = self.font.render(menu_labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(c.SCREEN_WIDTH/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


class MenuSelection(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()

        self.sprite = setup.GFX["green_button01"]
        self.sprite_selected = setup.GFX["green_button00"]

        self.font = setup.FONTS["kenvector_future_thin"]

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
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite, mult=c.MENU_MULT))
        frames.append(helpers.get_image(0, 0, 190, 49, self.sprite_selected, mult=c.MENU_MULT))
        return frames


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
        if self.selected:
            text = self.font.render(menu_labels[self.name], True, c.WHITE)
        else:
            text = self.font.render(menu_labels[self.name], True, c.BLACK)

        text_rect = text.get_rect(center=(c.SCREEN_WIDTH/2, self.rect.y + self.rect.height/2))
        surface.blit(text, text_rect)


class GameUI:
    def __init__(self):
        self.setup_buttons()


    def setup_buttons(self) -> None:
        # XXX UI button area?
        # Don't set area and don't name it button1, loop over to create buttons?
        # And loop over a list of button sprite names
        button1 = Button(200, 500, button_names[0])

        self.button_group = pg.sprite.Group(button1)


    def update(self, screen: pg.Surface) -> None:
        # XXX Access Input
        self.handle_state()

        self.blit_images(screen)


    def handle_state(self) -> None:
        pass


    def blit_images(self, screen: pg.Surface) -> None:
        # Draw sprites onto the screen
        self.button_group.draw(screen)
