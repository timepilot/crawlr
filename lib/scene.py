import pygame
from pygame.locals import *
from constants import *
from map import Map
from player import Player

class Scene(object):
    """A scene in the game that loads and manages a level."""

    def __init__(self, window):
        self.window = window
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        level = 1
        self.map = Map(level)
        self.layers = pygame.sprite.LayeredDirty()
        self.player = Player(window, self.map)

        # Characters to be drawn.
        self.characters = pygame.sprite.Group([self.player])

        # All sprites to be drawn.
        self.all_sprites = pygame.sprite.Group([self.characters])

        # All objects to be drawn in order.
        self.layers.add(self.map.mapLayer['terrain'])
        self.layers.add(self.characters)
        self.layers.add(self.map.mapLayer['foreground'])

        # Scroll the map to the player's starting location.
        self.scroll()

    def draw(self):
        """Draws the sprites to the scene and updates the window."""

        self.layers.update()
        rects = self.layers.draw(self.window)
        pygame.display.update(rects)

    def scroll(self):
        """Scroll the map to keep the player visible."""

        b_x, b_y = self.player.rect.center
        self.camera.center = (b_x, b_y)
        b_x, b_y = self.camera.topleft
        camera_w, camera_h = (self.camera.width, self.camera.height)
        map_w, map_h = (self.map.get_size())
        if b_x < 0:
            b_x = 0
        if b_x > map_w - camera_w:
            b_x = map_w - camera_w
        if b_y < 0:
            b_y = 0
        if b_y > map_h - camera_h:
            b_y = map_h - camera_h
        if map_h < camera_h:
            b_y = (map_h - camera_h) / 2
        if map_w < camera_w:
            b_x - (map_w - canera_h) / 2
        self.camera.topleft = [ -b_x, -b_y ]
        self.map.move_map([ self.camera[0], self.camera[1] ])
        self.player.rect.move_ip([ self.camera[0], self.camera[1] ])
        self.player.scroll_pos = [ self.camera[0], self.camera[1] ]
