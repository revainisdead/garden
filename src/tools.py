import os
import time

import pygame as pg
from PIL import Image

from . import constants as c


class Control:
    def __init__(self, caption):
        self.quit = False

        self.screen = pg.display.get_surface()

        self.current_time = 0
        self.fps = 20
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

        self.keys = pg.key.get_pressed()

        self.state = None
        self.state_name = None
        self.state_dict = {}


    def game_loop(self):
        while not self.quit:
            self.event_loop()

            self.update()
            pg.display.update()

            self.clock.tick(self.fps)


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()


    def update(self):
        """Connects to the main game loop.
        Do any updates needed
        """
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.quit = True
        elif self.state.state_done:
            self.flip_state()

        self.state.update(self.screen, self.keys, self.current_time)


    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

        print("Initial state in control object: {}".format(self.state_name))


    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]

        # Startup state when switching to it
        self.state.startup()
        print("Main state switched to: {}".format(self.state_name))

        self.state.previous = previous


class State:
    def __init__(self):
        # Quit everything
        self.quit = False

        # Quit this state
        self.state_done = False

        self.next = None
        self.previous = None


    def startup(self):
        raise NotImplementedError


    def update(self, surface, keys, current_time):
        raise NotImplementedError


# XXX Unused
def strip_png(img):
    r, g, b, a = img.split()
    img = Image.merge("RGB", (r, g, b))
    return img


# XXX Unused
def convert_png(name_path, convert_to_ext=".bmp"):
    # Name here should include the extension
    original_name = name_path
    if os.path.exists(original_name):
        img = Image.open(original_name)

        name, ext = os.path.splitext(original_name)
        joined = name + convert_to_ext

        img = strip_png(img)

        img.save(joined)
        print(" ** Removing {} **".format(original_name))
        os.unlink(original_name)


def colorize(image, color):
    image = image.copy()
    #image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
    image.fill(color[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
    return image


def recursive_load_gfx(path, accept=(".png", ".bmp", ".svg")):
    """
    Load graphics files.
    This operates on a one folder at a time basis.

    Note: An empty string doesn't count as invalid,
    since that represents a folder name.
    """
    colorkey = c.PURPLE
    graphics = {}

    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        name, ext = os.path.splitext(pic)

        if ext.lower() in accept:
            img = pg.image.load(pic_path)

            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img

        elif not ext:
            pass
        else:
            print("Got unexpected gfx format\n" \
                    "Path: {}\n" \
                    "Name: {}\n" \
                    "Ext: {}\n".format(pic_path, name, ext))

    return graphics


def load_gfx(path):
    """Loads all the files in the graphics folder
    and also one more folder level deep.
    Doesn't recurse files deeper than that."""
    graphics = {}

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        name, ext = os.path.splitext(item)

        # If there is no extension, assume it's a folder.
        if ext == "":
            # WARNING: Update can overwrite existing keys
            graphics.update(recursive_load_gfx(item_path))
        else:
            graphics.update(recursive_load_gfx(path))

    # sanity check
    if not graphics:
        print("No graphics loaded.")

    return graphics


def load_fonts(path, accept=(".ttf")):
    fonts = {}
    for font in os.listdir(path):
        name, ext = os.path.splitext(font)

        if ext.lower() in accept:
            fonts[name] = pg.font.Font(os.path.join(path, font), c.FONT_SIZE)
        else:
            print("Received invalid font. {}".format(font))

    return fonts


def load_sfx(path, accept=(".wav", ".mpe", ".ogg", ".mdi")):
    sounds = {}
    for sound in os.listdir(path):
        name, ext = os.path.splitext(sound)

        if ext.lower() in accept:
            sounds[name] = pg.mixer.Sound(os.path.join(path, sound))
        else:
            print("Received invalid sound effect. {}".format(sound))

    return sounds


def load_music(path, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    pass
