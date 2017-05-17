import os

import pygame as pg
from PIL import Image


class InvalidFont(Exception): pass
class InvalidGFX(Exception): pass


class Control:
    def __init__(self, caption):
        self.quit = False

        self.screen = pg.display.get_surface()

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
        # Allow quitting the main game loop from the state object
        if self.state.quit:
            self.quit = True
        elif self.state.state_done:
            self.flip_state()


        # Implement flipping (aka going to the next) states.
        #   * Initial screen
        #   * Loading screen
        #   * Level 1
        #   * Level 2
        #   * ...
        #   * Game over

        self.state.update(self.screen, self.keys)


    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

        print("Initial state in control object: {}".format(self.state_name))


    def flip_state(self):
        # Simultaneous state flip to next
        previous = self.state_name = self.state_name, self.state.next

        # Startup state when switching to it
        self.state.startup()

        self.state.previous = previous



class State:
    def __init__(self):
        # Quit everything
        self.quit = False

        # Quit this state
        self.state_done = False

        # Until states flow into each other, run statup manually
        self.startup()

        # State machine???
        self.next = None
        self.previous = None


    def startup(self):
        raise NotImplementedError


    def update(self, surface, keys):
        raise NotImplementedError


def strip_png(img):
    r, g, b, a = img.split()
    img = Image.merge("RGB", (r, g, b))
    return img


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


def load_gfx(path, accept=(".bmp")):
    colorkey = (255, 0, 255)
    graphics = {}

    # Convert images in directory first, then load them.
    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        name, ext = os.path.splitext(pic_path)
        if ext.lower() not in accept:
            convert_png(pic_path)

    for pic in os.listdir(path):
        pic_path = os.path.join(path, pic)
        name, ext = os.path.splitext(pic)

        if ext.lower() in accept:
            img = pg.image.load(pic_path)

            if img.get_alpha():
                img = img.convert_alpha()
            else:
                print("Setting color key for {}: {}".format(ext, [key for key in colorkey]))
                img = img.convert()
                img.set_colorkey(colorkey)

            graphics[name] = img

        else:
            raise InvalidGFX("Got unexpected gfx format. {}".format(ext))

    # sanity check
    if not graphics:
        print("No graphics loaded.")

    return graphics


def load_fonts(path, accept=(".ttf")):
    fonts = {}

    for font in os.listdir(path):
        name, ext = os.path.splitext(font)

        if ext.lower() in accept:
            fonts[name] = os.path.join(path, font)
        else:
            raise InvalidFont("Received invalid font. {}".format(font))

    return fonts


def load_music(path, accept=(".wav", ".mp3", ".ogg", ".mdi")): pass
def load_sfx(path, accept=(".wav", ".mpe", ".ogg", ".mdi")): pass
