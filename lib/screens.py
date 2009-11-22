from os import environ
import pygame
from pygame.locals import *
from constants import *
from interface import Dialog
from map import Map
from characters import Player
from battle import Battle

class Screen(object):
    """The base screen class that other screens inherit from."""

    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        fullscreen = False
        pygame.display.set_caption(GAME_NAME)
        pygame.mouse.set_visible(False)
        self.window = pygame.display.set_mode(WINDOW_SIZE, fullscreen,
            COLOR_DEPTH)


class TitleScreen(Screen):
    """The title screen displayed when the game is first run."""

    def __init__(self):
        Screen.__init__(self)

    def draw(self):
        """Draws the title screen and updates the window."""

        self.window.fill((0,0,0))
        pygame.display.update()


class WorldScreen(Screen):
    """The main game screen."""

    def __init__(self, level):
        Screen.__init__(self)
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        self.dialog = Dialog()
        self.map = Map(level)
        self.player = Player(self)
        self.layers = pygame.sprite.LayeredDirty()
        self.add()
        self.scroll()

    def add(self):
        """Add sprites to the screen in the correct order."""

        characters = pygame.sprite.Group([self.player])
        self.all_sprites = pygame.sprite.OrderedUpdates([
            self.map.layers['terrain'],
            characters,
            self.map.layers['foreground']])
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

    def destroy(self):
        """Destroy the current screen."""

        for sprite in self.all_sprites:
            sprite.kill()
        self.map = None
        self.player = None
