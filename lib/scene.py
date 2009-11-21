import pygame
from pygame.locals import *
from constants import *
from interface import Dialog
from map import Map
from characters import Player
from battle import Battle

class GameScreen(object):
    """The main game screen."""

    def __init__(self, window, level):
        self.window = window
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        self.dialog = Dialog()
        self.map = Map(level)
        self.player = Player(self)
        self.layers = pygame.sprite.LayeredDirty()

        # Add items to the screen.
        self.add()

        # Scroll the map to the player's starting location.
        self.scroll()

    def add(self):
        """Add sprites to the screen in the correct order."""

        # Characters to be drawn.
        characters = pygame.sprite.Group([self.player])

        # All sprites to be drawn in order.
        self.all_sprites = pygame.sprite.OrderedUpdates([
            self.map.layers['terrain'],
            characters,
            self.map.layers['foreground']])

        # Add all of the sprites to the screen.
        for sprite in self.all_sprites:
            self.layers.add(sprite)

    def draw(self):
        """Draws the sprites to the screen and updates the window."""

        if self.dialog.toggle:
            self.layers.add(self.dialog)
        else:
            self.dialog.kill()
            self.dialog.toggle = False

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
            b_x - (map_w - camera_w) / 2
        self.camera.topleft = [ -b_x, -b_y ]
        self.map.move_map([ self.camera[0], self.camera[1] ])
        self.player.rect.move_ip([ self.camera[0], self.camera[1] ])
        self.player.scroll_pos = [ self.camera[0], self.camera[1] ]

    def toggle_dialog(self):
        """Toggles the status menu dialog."""

        if self.dialog.toggle:
            self.dialog.toggle = False
        else:
            self.dialog.toggle = True

    def start_battle(self):
        """Starts a battle screen."""

        self.battle = Battle(self)
        self.battle.create_monsters()

    def reload(self, game):
        """Reloads the current screen."""

        self.destroy()
        game.run()

    def destroy(self):
        """Destroy the current screen."""

        for sprite in self.all_sprites:
            sprite.kill()
        self.map = None
        self.player = None
