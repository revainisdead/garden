from typing import Any, Dict, Tuple

import time
import random

import pygame

from .. import binds
from .. import constants as c
from .. import control
from .. import setup
from .. import tools

from .. components import non_player_controlled, player, scenery, tilemap, user_interface, util


class CommonArea(control.State):
    def __init__(self) -> None:
        super().__init__()

        self.biome = setup.map_size.get_biome()
        self.tilemap = self.setup_map(self.biome)

        # There will be no stairs up on map initializing.
        self.stairs_up_group = pygame.sprite.Group()

        # Save a copy of the first tilemap, so that we can re-create it later.
        self.farmland = self.tilemap


    def startup(self, game_info: Dict[str, Any]) -> None:
        self.game_info = game_info
        self.state = c.StateName.COMMONAREA

        self.stairs_down_copy = []
        self.stairs_down_group = self.setup_stairs_down()

        self.setup_player()
        self.npc_group = self.setup_npcs()

        self.setup_camera()
        self.setup_hud()


    def setup_map(self, biome: c.Biome) -> tilemap.Map:
        temp_map = tilemap.Map(setup.map_size.get_grid_width(), setup.map_size.get_grid_height(), setup.map_size.get_width(), setup.map_size.get_height(), biome)
        self.collidable_group = temp_map.create_collidables()
        self.tilemap_rect = temp_map.map_surface.get_rect()
        self.entire_area = pygame.Surface((self.tilemap_rect.width, self.tilemap_rect.height)).convert()
        self.entire_area_rect = self.entire_area.get_rect()
        return temp_map


    def setup_camera(self) -> None:
        # Start the camera on top of the player.
        self.camera = pygame.Rect((self.player.rect.x, self.player.rect.y), (setup.screen_size.get_width(), setup.screen_size.get_height()))
        self.camera.centerx = self.player.rect.centerx
        self.camera.centery = self.player.rect.centery

        self.direction = c.Direction.NONE
        self.camera_speed = c.speeds["camera"]
        self.set_camera_velocity()

        # Call move_camera once in setup to force the camera to center
        # on the player.
        self.move_camera()


    def setup_npcs(self) -> pygame.sprite.Group:
        temp_group = pygame.sprite.Group()

        random_npcs_limit = random.randint(c.MIN_NPC_AMOUNT, c.MAX_NPC_AMOUNT)
        for _ in range(random_npcs_limit):
            x, y = self.tilemap.find_random_open_location()
            temp_group.add(non_player_controlled.Npc(x, y))

        return temp_group


    def setup_player(self) -> None:
        # But should the player's location be random? Maybe, go find your farm!
        x, y = self.tilemap.find_random_open_location()
        self.player = player.Player(x, y)
        self.player_group = pygame.sprite.Group(self.player)


    def setup_stash(self) -> None:
        #x, y = self.tilemap.find_random_open_location()
        pass


    def setup_stairs_down(self) -> pygame.sprite.Group:
        temp_group = pygame.sprite.Group()

        random_limit = random.randint(c.MIN_STAIRS_AMOUNT, c.MAX_STAIRS_AMOUNT)
        for _ in range(random_limit):
            x, y = self.tilemap.find_random_open_location()
            # Stairs should draw over bushes, so don't worry about the fact
            # that an "open location" only means no collidables.
            temp_group.add(scenery.Stairs(x, y, "stairs_down"))

            # XXX Collidables for stairs should probably be handled by tilemap.
            self.collidable_group.add(util.Collidable(x, y))

        return temp_group


    def setup_stairs_up(self) -> None:
        """Need 1 stairs up when entering a cave.

        I could put it next to the player but how would I know
        if it's an open location. Just put it in a random open
        location as usual.
        """
        x, y = self.tilemap.find_random_open_location()
        self.stairs_up_group.add(scenery.Stairs(x, y, "stairs_up"))

        # XXX Collidables for stairs should probably be handled by tilemap.
        self.collidable_group.add(util.Collidable(x, y))


    def setup_hud(self) -> None:
        self.hud = user_interface.Hud()


    def update(self, surface: pygame.Surface, current_time: int) -> None:
        """Update the state every frame"""
        # Let this state control the map size update.
        setup.map_size.update(self.biome)

        # XXX Create function/class to handle game info.
        self.game_info["current_time"] = current_time

        self.update_sizes()
        self.update_map()
        self.update_sprites()
        self.handle_states()
        self.blit_images(surface)

        # Draw the hud to the screen over everything else.
        # Similar to Game UI but the hud needs access to game_info.
        self.hud.update(surface, self.game_info, self.player, self.tilemap_rect.bottom)


    def handle_states(self) -> None:
        if binds.INPUT.pressed("escape"):
            self.quit = True
        else:
            self.move_camera()


    def update_sizes(self) -> None:
        if setup.screen_size.changed():
            # Start new camera at the same position as before.
            self.camera = pygame.Rect((self.camera.x, self.camera.y), (setup.screen_size.get_width(), setup.screen_size.get_height()))


    def update_map(self) -> None:
        if setup.map_size.changed():
            self.tilemap = self.setup_map(self.biome)
            self.npc_group = self.setup_npcs()
            self.setup_player()

            # What about going back up to farmland. I want to create
            # the same map as before, and have the same stairs...
            # So I need to save the old map, and un-kill all the stairs.
            for stairs in self.stairs_down_group:
                self.stairs_down_copy.append(stairs)
                stairs.kill()

            self.setup_stairs_up()


    def update_sprites(self) -> None:
        self.player_group.update(self.game_info["current_time"], self.collidable_group)
        self.npc_group.update(self.game_info["current_time"], self.collidable_group)
        self.stairs_down_group.update(self.player.rect)

        # XXX separate into: def handle_biome(self)
        for stairs_down in self.stairs_down_group:
            # Check stairs state change.
            if stairs_down.hit:
                self.biome = c.Biome.CAVE

        # If in cave, check for a hit on stairs up.
        if self.biome == c.Biome.CAVE:
            self.stairs_up_group.update(self.player.rect)
            for stairs_up in self.stairs_up_group:
                if stairs_up.hit:
                    # XXX This won't entirely work. I need to re-create everything in setup_map when I change the map BACK to farmland as well.
                    #self.tilemap = self.farmland
                    # For now just re-setup map, it won't be the same map, but at least it will work. It should be the same map later. I should:
                    #   - Set up 1 farmland and save it's info, including rect.
                    #   - Set up 1 cave map for every stairs down and save it.
                    #   - The random part should be only once. Maybe?
                    #   - I want the farm to save it's state. Including it's look! The look of the farmland could be saved in game info, and caves could be their own state. Like even the worker's location I want to be exactly the same when the player leaves the cave. As for the amount of stuff gathered while the player was gone, that can be calculating, including the amount of growth plants have had.
                    self.tilemap = self.setup_map(c.Biome.FARMLAND)

                    if not self.stairs_down_group:
                        self.stairs_down_group = self.setup_stairs_down() # or just try over-writing the stairs_down group that is empty with new stairs!

                    # And kill stairs up.
                    for stairs in self.stairs_up_group:
                        stairs.kill()
        else:
            # If the biome is not cave. Restore old stairs.
            # XXX This places them in the same old location. Which is good
            # for re-loading an old map, but right now it's going to create
            # a new map.
            #for stairs in self.stairs_down_copy:
            #self.stairs_down_group.add(stairs)
            pass


    def move_camera(self) -> None:
        self.direction = self.player.direction
        self.set_camera_velocity()

        new_x, new_y = tools.fix_edge_bounds(rect=self.camera, highest_x=self.tilemap_rect.right, highest_y=self.tilemap_rect.bottom, x_vel=self.camera_x_vel, y_vel=self.camera_y_vel)

        check_gt_x = lambda x: x if x > self.camera.centerx else self.camera.centerx
        check_lt_x = lambda x: x if x < self.camera.centerx else self.camera.centerx
        check_gt_y = lambda y: y if y > self.camera.centery else self.camera.centery
        check_lt_y = lambda y: y if y < self.camera.centery else self.camera.centery

        if self.camera.x != new_x:
            if self.direction == c.Direction.LEFT:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHT:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.LEFTUP:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHTUP:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.LEFTDOWN:
                self.camera.centerx = check_lt_x(self.player.rect.centerx)
            elif self.direction == c.Direction.RIGHTDOWN:
                self.camera.centerx = check_gt_x(self.player.rect.centerx)

        if self.camera.x < 0:
            self.camera.x = 0
        elif self.camera.x + self.camera.w > self.tilemap_rect.right:
            self.camera.x = new_x

        if self.camera.y < 0:
            self.camera.y = 0
        elif self.camera.y + self.camera.h > self.tilemap_rect.bottom:
            self.camera.y = new_y

        new_x, new_y = tools.fix_edge_bounds(rect=self.camera, highest_x=self.tilemap_rect.right, highest_y=self.tilemap_rect.bottom, x_vel=self.camera_x_vel, y_vel=self.camera_y_vel)

        if self.camera.y != new_y:
            if self.direction == c.Direction.UP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.DOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)
            elif self.direction == c.Direction.LEFTUP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.RIGHTUP:
                self.camera.centery = check_lt_y(self.player.rect.centery)
            elif self.direction == c.Direction.LEFTDOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)
            elif self.direction == c.Direction.RIGHTDOWN:
                self.camera.centery = check_gt_y(self.player.rect.centery)


        if self.camera.x < 0:
            self.camera.x = 0
        elif self.camera.x + self.camera.w > self.tilemap_rect.right:
            self.camera.x = new_x

        if self.camera.y < 0:
            self.camera.y = 0
        elif self.camera.y + self.camera.h > self.tilemap_rect.bottom:
            self.camera.y = new_y

        # Debug.
        #print("camera.y: {}".format(self.camera.y))
        #print("new_y:    {}".format(new_y))
        #self.camera.centerx = self.player.rect.centerx
        #self.camera.centery = self.player.rect.centery


    def set_camera_velocity(self) -> None:
        self.camera_x_vel = 0
        self.camera_y_vel = 0

        if self.direction == c.Direction.LEFT:
            self.camera_x_vel = -self.camera_speed
        elif self.direction == c.Direction.RIGHT:
            self.camera_x_vel = self.camera_speed
        elif self.direction == c.Direction.UP:
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.DOWN:
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.LEFTUP:
            self.camera_x_vel = -self.camera_speed
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.LEFTDOWN:
            self.camera_x_vel = -self.camera_speed
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.RIGHTUP:
            self.camera_x_vel = self.camera_speed
            self.camera_y_vel = -self.camera_speed
        elif self.direction == c.Direction.RIGHTDOWN:
            self.camera_x_vel = self.camera_speed
            self.camera_y_vel = self.camera_speed
        elif self.direction == c.Direction.NONE:
            self.camera_x_vel = 0
            self.camera_y_vel = 0


    def blit_images(self, surface: pygame.Surface) -> None:
        # This is responsible for showing only a certain area
        # of the tilemap surface, the area shown is the area of the camera.
        self.entire_area.blit(self.tilemap.map_surface, self.camera, self.camera)

        self.tilemap.update(self.entire_area, self.camera)

        self.stairs_down_group.draw(self.entire_area)
        self.stairs_up_group.draw(self.entire_area)
        self.npc_group.draw(self.entire_area)
        # Draw player over npc's, to make player feel more important...
        self.player_group.draw(self.entire_area)
        self.tilemap.tree_top_group.draw(self.entire_area)

        # Finally, draw everything to the screen surface.
        surface.blit(self.entire_area, (0, 0), self.camera)
