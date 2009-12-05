import pygame
from pygame.locals import *
from constants import *
from data import *
from interface import *
from map import Map
from characters import Player
from battle import Battle

class Screen(object):
    """The base screen class that other screens inherit from."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        pygame.mouse.set_visible(False)
        if FULL_SCREEN:
            fullscreen = FULLSCREEN
        else:
            fullscreen = False
        self.window = pygame.display.set_mode(WINDOW_SIZE, fullscreen,
            COLOR_DEPTH)
        self.layers = pygame.sprite.LayeredDirty()

    def add(self, items):
        """Add items to the screen."""

        group = pygame.sprite.Group(items)
        self.all_sprites = pygame.sprite.OrderedUpdates([group])
        for sprite in self.all_sprites:
            self.layers.add(sprite)
        self.align(items)

    def draw(self):
        """Draw items to the screen."""

        rects = self.layers.draw(self.window)
        self.layers.update(rects)

    def destroy(self):
        """Destroy the current screen."""

        for sprite in self.all_sprites:
            sprite.kill()


class LoadScreen(Screen):
    """The loading screen displayed when changing states."""

    def __init__(self):
        Screen.__init__(self)
        text1 = Font("menu", 24, (255,0,0), "Loading...")
        self.add([text1])

    def align(self, items):
        items[0].rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 ]


class TitleScreen(Screen):
    """The title screen is the first screen displayed."""

    def __init__(self):
        Screen.__init__(self)
        text1 = Font("menu", 24, (255,0,0), "Title Screen Goes Here")
        text2 = Font("menu", 16, (255,255,255),
            "Press 'n' to start a new game.")
        self.add([text1, text2])

    def align(self, items):
        items[0].rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-20 ]
        items[1].rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2+20 ]


class WorldScreen(Screen):
    """The main game screen with a world to wander around."""

    def __init__(self, map_num):
        Screen.__init__(self)
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        self.map = Map(map_num)
        self.player = Player(self)
        self.map.scroll(self.camera, self.player)
        self.add()

    def add(self):
        """Add sprites to the screen in the correct order."""

        characters = pygame.sprite.Group([self.player])
        self.all_sprites = pygame.sprite.OrderedUpdates([
            self.map.layers['terrain'],
            characters,
            self.map.layers['foreground'] ])
        for sprite in self.all_sprites:
            self.layers.add(sprite)

    def draw(self):
        """Draws the sprites to the screen and updates the window."""

        self.layers.update()
        rects = self.layers.draw(self.window)
        pygame.display.update(rects)

    def destroy(self):
        """Destroy the current screen."""

        for sprite in self.all_sprites:
            sprite.kill()
        self.map = None
        self.player = None


class BattleScreen(Screen, Battle):
    """The battle screen is where a battle takes place."""

    def __init__(self, prevstate):
        Screen.__init__(self)
        Battle.__init__(self, prevstate)
        text1 = Font("menu", 24, (255,0,0), "Battle Screen Goes Here")
        text2 = Font("menu", 16, (255,255,255),
            "Press 'Esc' to go back to the game.")
        self.add([text1, text2])

    def align(self, items):
        items[0].rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-20 ]
        items[1].rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2+20 ]
