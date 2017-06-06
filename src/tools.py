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
        image.fill(color + (0,), None, pg.BLEND_RGBA_ADD)
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


def fix_bounds(rect: pg.Rect, highest_x: int, highest_y: int, x_vel: int, y_vel: int, lowest_x: int=0, lowest_y: int=0) -> Tuple[int, int]:
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

    RETURN NEW X AND Y POSITION INSTEAD OF CHANGING IT, LET THE SPRITE
    CHANGE THE MOVEMENT ITSELF.
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

    # New if statement because x and y both need to be checked each frame.
    if new_y < lowest_y:
        hit_wall = True
        new_y = lowest_y
    elif new_y + rect.h > highest_y:
        # Remember: y is inverted... The highest point is on the bottom.
        hit_wall = True
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
    """
    hit_wall = False
    if x_vel > 0:
        rect.right = highest_x
        hit_wall = True
    elif x_vel < 0:
        rect.left = lowest_x
        hit_wall = True
    if y_vel > 0:
        rect.bottom = highest_y
        hit_wall = True
    elif y_vel < 0:
        rect.top = lowest_y
        hit_wall = True
    """
    return hit_wall


def test_collide(sprite: pg.sprite.Sprite, x_vel: int, y_vel: int, collidable_group: pg.sprite.Group) -> bool:
    """Test for the rect's collision into collidables and fix bounds."""

    """
    new_x = rect.x + x_vel
    new_y = rect.y + y_vel
    hit_wall = False
    for collidable in collidables:
        # The lowest x is the left side of the collidable rect. And so on.
        # Picture a sprite moving against a rock, should side of the rock
        # is it colliding with?
        if new_x < collidable.rect.right:
            hit_wall = True
            new_x = collidable.rect.right
        elif new_x + rect.w > collidable.rect.left:
            hit_wall = True
            new_x = rect.x

        if new_y < collidable.rect.bottom:
            hit_wall = True
            new_y = collidable.rect.bottom
        elif new_y + rect.h > collidable.rect.top:
            hit_wall = True
            new_y = rect.y + (collidable.rect.top - rect.bottom)
            #new_y = rect.y

    rect.x = new_x
    rect.y = new_y
    """
    hit_wall = False
    # Rewrite collidables to only contain sprites that are collided with.
    #for collider in [collider for collider in collidables if collider.rect.colliderect(rect)]
    collider = pg.sprite.spritecollideany(sprite, collidable_group)
    if collider is not None:
        # Quadrants. Reverse engineer direction based on velocities.
        #  -x, -y  |  x, -y
        # ------------------
        #  -x,  y  |  x,  y

        #  1  |  2
        # ---------
        #  3  |  4
        neg_x, pos_x = x_vel < 0, x_vel > 0
        neg_y, pos_y = y_vel < 0, y_vel > 0
        """
        quad1 = neg_x and neg_y
        quad2 = pos_x and neg_y
        quad3 = neg_x and pos_y
        quad4 = pos_y and pos_y

        # X compare.
        neg_x_compare = rect.left < collider.rect.right
        neg_x_fix = collider.rect.right
        pos_x_compare = rect.right > collider.rect.left
        pos_x_fix = collider.rect.left
        # Y compare.
        neg_y_compare = rect.top < collider.rect.bottom
        neg_y_fix = collider.rect.bottom
        pos_y_compare = rect.bottom > collider.rect.top
        pos_y_fix = collider.rect.top

        if quad1:
            if neg_x_compare and (neg_y_compare or pos_y_compare):
                rect.left = neg_x_fix
            elif neg_y_compare and (neg_x_compare or pos_x_compare):
                rect.top = neg_y_fix
        elif quad2:
            if pos_x_compare and (neg_y_compare or pos_y_compare):
                rect.right = pos_x_fix
            elif neg_y_compare and (neg_x_compare or pos_x_compare):
                rect.top = neg_y_fix
        elif quad3:
            if neg_x_compare and (neg_y_compare or pos_y_compare):
                rect.left = neg_x_fix
            elif pos_y_compare and (neg_x_compare or pos_x_compare):
                rect.bottom = pos_y_fix
        elif quad4:
            if pos_x_compare and (neg_y_compare or pos_y_compare):
                rect.right = pos_x_fix
            elif pos_y_compare and (neg_x_compare or pos_x_compare):
                rect.bottom = pos_y_fix
        """
        #else:


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


def test_diagonal_collide(rect: pg.Rect, x_vel: int, y_vel: int, collidables: List[util.Collidable]) -> bool:
    """
    The only way to test diagonal collision is to change velocity values,
    not to change the sides of the rects based on velocity.
    A diagonal test should return corrected velocity values.

    - This is only preferred for diagonal movement, it's okay to correct
    up, down, left, right movement because it can only have one velocity value
    greater than or less than 0 at a time, whereas diagonal movement has
    values other than 0 for x velocity and y velocity both.

    - Another reason we don't use this for npc roaming is because we only
    care about returning hit_wall for AI, if a player hits a wall it
    doesn't matter, but if a AI hits a wall we want it to go somewhere else.

    :returns: x_vel, y_vel
    """
    # Rewrite collidables to only contain rects that are collided with.
    #collidables = [collider for collider in collidables if collider.rect.colliderect(rect)]
    hit_left_wall, hit_right_wall, hit_top_wall, hit_bottom_wall = (False, False, False, False)

    hit_wall = False
    neg_x, pos_x = x_vel < 0, x_vel > 0
    neg_y, pos_y = y_vel < 0, y_vel > 0
    for collider in [collider for collider in collidables if collider.rect.colliderect(rect)]:
        """
        if x_vel > 0:
            # If vel would put it over the bound, stop moving it.
            # But if it is over already the bound, correct it.
            if rect.right > collider.rect.left:
                x_vel = 0
            elif rect.right > collider.rect.left:
                rect.right = collider.rect.left
        elif x_vel < 0:
            if rect.left + x_vel < collider.rect.right:
                x_vel = 0
            elif rect.left > collider.rect.right:
                rect.left = collider.rect.right

        if y_vel > 0:
            if rect.bottom + y_vel > collider.rect.top:
                y_vel = 0
            elif rect.bottom > collider.rect.top:
                rect.bottom = collider.rect.top
        elif y_vel < 0:
            if rect.top + y_vel < collider.rect.bottom:
                y_vel = 0
            elif rect.top > collider.rect.bottom:
                rect.top = collider.rect.bottom
    return x_vel, y_vel

        if pos_x:
            if rect.right > collider.rect.left:
                rect.right = collider.rect.left
                hit_wall = True
        elif neg_x:
            if rect.left < collider.rect.right:
                rect.left = collider.rect.right
                hit_wall = True
        elif pos_y:
            if rect.bottom > collider.rect.top:
                rect.bottom = collider.rect.top
                hit_wall = True
        elif neg_y:
            if rect.top < collider.rect.bottom:
                rect.top = collider.rect.bottom
                hit_wall = True

    return hit_wall
        """
        # Figure out which wall was collided with.
        #if rect.right > collider.rect.left:
            #hit_left_wall = True
        #if rect.left < collider.rect.right:
            #hit_right_wall = True
        #if rect.bottom > collider.rect.top:
            #hit_top_wall = True
        #if rect.top < collider.rect.bottom:
            #hit_bottom_wall = True
        #print(rect.right + x_vel)
        #print(collider.rect.left)
        #print(collider.rect.left + x_vel)
        if rect.right > collider.rect.left and rect.right < collider.rect.left + x_vel:
            hit_left_wall = True
        if rect.left < collider.rect.right and rect.left > collider.rect.right + x_vel:
            hit_right_wall = True

        if rect.bottom > collider.rect.top and rect.bottom < collider.rect.top:
            hit_top_wall = True
        if rect.top < collider.rect.bottom and rect.top > collider.rect.bottom:
            hit_bottom_wall = True


        if hit_left_wall or hit_right_wall:
            # Do x check.
            if pos_x:
                if rect.right > collider.rect.left:
                    rect.right = collider.rect.left
            elif neg_x:
                if rect.left < collider.rect.right:
                    rect.left = collider.rect.right

        elif hit_top_wall or hit_bottom_wall:
            if pos_y:
                if rect.bottom > collider.rect.top:
                    rect.bottom = collider.rect.top
            elif neg_y:
                if rect.top < collider.rect.bottom:
                    rect.top = collider.rect.bottom

        test = any([hit_left_wall, hit_right_wall, hit_top_wall, hit_bottom_wall])
        if test: print(test)


# To allow diagonal movement, the *side* that is being collided with
# *must* be known, therefore collidrect cannot be used, or else it will
# detect *all* collisions, but we only want the position to be reset
# on that side IF and only IF it collided with that side.
