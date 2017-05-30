from typing import List, Tuple

import os

from PIL import Image
import pygame as pg

from . import constants as c
from . components import util


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


def colorize(images: List[pg.Surface], color: Tuple[int, int, int]) -> List[pg.Surface]:
    colored = []
    for image in images:
        image = image.copy()
        #image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
        image.fill(color[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
        colored.append(image)

    return colored


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
                if name == "tree_shadow":
                    print("unconverted tree shadow alpha: {}".format(img.get_alpha()))
                #img = img.convert_alpha()
                img.convert_alpha()

                # Debug.
                if name == "tree_shadow":
                    print("converted tree shadow alpha: {}".format(img.get_alpha()))
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


def fix_bounds(rect: pg.Rect, highest_x: int, highest_y: int, x_vel: int, y_vel: int, lowest_x: int=0, lowest_y: int=0) -> None:
    """Universal utility to fix x and y values based on bounds

    Non-default args:
    :param rect: Rectangle that gets its x and y modified.
    :param highest_x: Highest X allowed
    :param highest_y: Highest Y allowed
    :param x_vel: X movement speed
    :param y_vel: Y movement speed

    Default args:
    :param lowest_x=0: Lowest X allowed
    :param lowest_y=0: Lowest Y allowed
    """
    new_x = rect.x + x_vel
    new_y = rect.y + y_vel
    hit_wall = False
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
    return hit_wall


def test_collide(rect: pg.Rect, x_vel: int, y_vel: int, collidables: List[util.Collidable]) -> bool:
    """Test for the rect's collision into collidables and fix bounds."""
    # Rewrite collidables to only contain rects that are collided with.
    collidables = [collider for collider in collidables if collider.rect.colliderect(rect)]

    hit_wall = False
    for collider in collidables:
        if collider.rect.colliderect(rect):
            if x_vel > 0:
                rect.right = collider.rect.left
                hit_wall = True
            elif x_vel < 0:
                rect.left = collider.rect.right
                hit_wall = True
            if y_vel > 0:
                rect.bottom = collider.rect.top
                hit_wall = True
            elif y_vel < 0:
                rect.top = collider.rect.bottom
                hit_wall = True

    return hit_wall
