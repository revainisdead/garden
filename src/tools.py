from typing import List, Tuple

import os

from PIL import Image
import pygame

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


def colorize(images: List[pygame.Surface], color: Tuple[int, ...]) -> List[pygame.Surface]:
    colored = []
    for image in images:
        image = image.copy()
        #image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        image.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)
        colored.append(image)
    return colored


def colorize_quality(images: List[pygame.Surface], color: Tuple[int, ...]) -> List[pygame.Surface]:
    colored = []
    for image in images:
        image = image.copy()
        #image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        image.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)
        colored.append(image)
    return colored


def recursive_load_gfx(path, accept=(".png", ".bmp", ".svg")):
    """
    Load graphics files.
    This operates on a one folder at a time basis.

    Note: An empty string doesn't count as invalid,
    since that represents a folder name.
    """
    colorkey = c.UGLY_PURPLE
    graphics = {}

    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        name, ext = os.path.splitext(pic)

        if ext.lower() in accept:
            img = pygame.image.load(pic_path)

            if img.get_alpha():
                #img = img.convert_alpha()
                img.convert_alpha()
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


# Load all the fonts for all the sizes that I want to use.
def load_fonts(path, accept=(".ttf")):
    fonts = {}

    for pair in c.FONT_SIZE_DICT.items():
        font_size_name = pair[0] # Ex. menu, game, etc.
        font_size = pair[1]
        for font in os.listdir(path):
            name, ext = os.path.splitext(font)
            if ext.lower() in accept:
                # Add the intended size use to the name.
                name = "{}_{}".format(font_size_name, name)
                fonts[name] = pygame.font.Font(os.path.join(path, font), font_size)
            else:
                print("Received invalid font. {}".format(font))

    return fonts


def load_sfx(path, accept=(".wav", ".mpe", ".ogg", ".mdi")):
    sounds = {}
    for sound in os.listdir(path):
        name, ext = os.path.splitext(sound)

        if ext.lower() in accept:
            sounds[name] = pygame.mixer.Sound(os.path.join(path, sound))
        else:
            print("Received invalid sound effect. {}".format(sound))

    return sounds


def load_music(path, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    pass


def fix_edge_bounds(rect: pygame.Rect, highest_x: int, highest_y: int, x_vel: int, y_vel: int) -> Tuple[int, int]:
    """Universal utility to correct x and y values based on fixed bounds.

    Useful for checking if something has gone past the highest possible
    x or y (a.k.a. end of the map).

    :param rect: Rectangle that gets its x and y modified.
    :param highest_x: Highest X allowed
    :param highest_y: Highest Y allowed
    :param x_vel: X movement speed
    :param y_vel: Y movement speed

    :returns: One corrected x and one corrected y value.
    """
    lowest_x = 0
    lowest_y = 0

    new_x = rect.x + x_vel
    new_y = rect.y + y_vel
    if new_x < lowest_x:
        new_x = lowest_x
    elif new_x + rect.w > highest_x:
        # Apply y fix to x for fixing the camera on top of player.
        new_x = rect.x + (highest_x - rect.right)

    # New if statement because x and y both need to be checked each frame.
    if new_y < lowest_y:
        new_y = lowest_y
    elif new_y + rect.h > highest_y:
        # Remember: y is inverted... The highest point is on the bottom.
        # Interesting bug was here. When the camera is about the move off
        # the map, the camera speed will be added to new_y and if the camera
        # displacement would have moved the camera off the screen, it will
        # prevent it from moving to the end. So add whatever is left between
        # the camera and the end of the map, even if it was less than the
        # speed, to see the entire area. Somehow though this bug didn't
        # apply to the horizontal movement.
        new_y = rect.y + (highest_y - rect.bottom)

    #rect.x = new_x
    #rect.y = new_y
    return new_x, new_y


def test_collide(sprite: pygame.sprite.Sprite, x_vel: int, y_vel: int, collidable_group: pygame.sprite.Group) -> bool:
    """
    Test for the rect's collision into collidables and fix bounds.
    Only use for horizontal and vertical movement, not diagonal.

    Like for AI roaming, worker roaming, etc.
    """
    hit_wall = False
    neg_x, pos_x = x_vel < 0, x_vel > 0
    neg_y, pos_y = y_vel < 0, y_vel > 0
    collider = pygame.sprite.spritecollideany(sprite, collidable_group)

    if collider is not None:
        if pos_x:
            if sprite.rect.right > collider.rect.left:
                sprite.rect.right = collider.rect.left
                hit_wall = True
        elif neg_x:
            if sprite.rect.left < collider.rect.right:
                sprite.rect.left = collider.rect.right
                hit_wall = True
        elif pos_y:
            if sprite.rect.bottom > collider.rect.top:
                sprite.rect.bottom = collider.rect.top
                hit_wall = True
        elif neg_y:
            if sprite.rect.top < collider.rect.bottom:
                sprite.rect.top = collider.rect.bottom
                hit_wall = True

    return hit_wall
