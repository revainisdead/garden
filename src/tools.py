from typing import Tuple

import os
import time

import pygame as pg
from PIL import Image

from . import constants as c


per_pixel_alpha_names = [
    "tree_shadow",
]


class Control:
    def __init__(self, caption):
        self.quit = False

        self.screen = pg.display.get_surface()

        self.current_time = 0
        self.fps = c.FPS
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
        # Get game_info before setting new state
        game_info = self.state.dump_game_info()
        self.state = self.state_dict[self.state_name]

        # Startup state when switching to it
        self.state.startup(game_info)
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
        self.game_info = {}


    def dump_game_info(self):
        return self.game_info


    def startup(self):
        raise NotImplementedError


    def update(self):
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


# XXX Unused
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

            #if name in per_pixel_alpha_names:
            if img.get_alpha():
                if name == "tree_shadow":
                    print("unconverted tree shadow alpha: {}".format(img.get_alpha()))
                if name == "small_orange_treebottom":
                    print("unconverted tree bottom alpha: {}".format(img.get_alpha()))
                #img = img.convert_alpha()
                img.convert_alpha()

                # Debug.
                if name == "tree_shadow":
                    print("converted tree shadow alpha: {}".format(img.get_alpha()))
                if name == "small_orange_treebottom":
                    print("converted tree bottom alpha: {}".format(img.get_alpha()))
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



def fix_bounds(rect: pg.Rect, highest_x: int, highest_y: int, x_vel: int, y_vel: int, lowest_x: int=0, lowest_y: int=0) -> Tuple[pg.Rect, bool]:
    """Universal utility to fix x and y values based on bounds

    Non-default args:
    :param highest_x: Highest X allowed
    :param highest_y: Highest Y allowed
    :param x_vel: X movement speed
    :param y_vel: Y movement speed
    :param rect: Rectangle to check bounds for

    Default args:
    :param lowest_x=0: Lowest X allowed
    :param lowest_y=0: Lowest Y allowed

    Returns Tuple of:
    :returns rect: Rectangle with corrected x, y values
    :returns hit_wall: Whether the end of the map was hit
    """
    hit_wall = False

    new_x = rect.x + x_vel
    new_y = rect.y + y_vel
    if new_x < lowest_x:
        hit_wall = True
        new_x = lowest_x
    elif new_x + rect.w > highest_x:
        hit_wall = True
        new_x = rect.x

    if new_y < lowest_y:
        hit_wall = True
        new_y = lowest_y
    elif new_y + rect.h > highest_y:
        # Remember: y is inverted... The highest point is on the bottom.
        hit_wall = True
        new_y = rect.y

    rect.x = new_x
    rect.y = new_y
    return rect, hit_wall
