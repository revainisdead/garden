import os

import pygame as pg


class Control:
    def __init__(self, caption):
        self.quit = False

        self.screen = pg.display.get_surface()

        self.fps = 20
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

        self.keys = pg.key.get_pressed()

        # State stuff
        self.state = None
        self.state_name = None
        self.state_dict = {}


    def game_loop(self):
        while not self.quit:
            self.event_loop()

            # Drawing updates
            self.update()

            # audio?
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


def __load_stuff(path, accept):
    stuff = {}

    # List of everything in path
    for item in os.listdir(path):
        # Unpack filename and ext
        name, ext = os.path.splitext(item)

        if ext.lower() in accept:
            stuff[name] = os.path.join(path, item)

    return stuff


def load_gfx(path, accept=(".png")):
    colorkey = (255, 0, 255)
    graphics = {}

    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)

        if ext.lower() in accept:
            img = pg.image.load(os.path.join(path, pic))

            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
        else:
            print("Got unexpected graphic format: {}".format(ext))

        graphics[name] = img

    return graphics

def load_fonts(path, accept=(".ttf")):
    return __load_stuff(path, accept)


def load_music(path, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    pass


def load_sfx(path, accept=(".wav", ".mpe", ".ogg", ".mdi")):
    pass
