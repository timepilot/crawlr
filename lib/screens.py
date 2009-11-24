from os import environ
import pygame
from pygame.locals import *
from constants import *
from data import *
from dice import Die
from interface import *
from map import Map
from characters import Player
from battle import Battle

class Screen(object):
    """The base screen class that other screens inherit from."""

    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        pygame.mouse.set_visible(False)
        if FULL_SCREEN:
            fullscreen = FULLSCREEN
        else:
            fullscreen = False
        self.window = pygame.display.set_mode(WINDOW_SIZE, fullscreen,
            COLOR_DEPTH)


class LoadScreen(Screen):
    """The loading screen displayed when changing states."""

    def __init__(self):
        Screen.__init__(self)
        self.layers = pygame.sprite.LayeredDirty()
        self.add()

    def add(self):
        self.loading = Text("menu", 24, (255,0,0), "Loading...")
        text = pygame.sprite.Group([self.loading])
        all_sprites = pygame.sprite.OrderedUpdates([
            text])
        for sprite in all_sprites:
            self.layers.add(sprite)

    def draw(self):
        self.loading.rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2 ]
        rects = self.layers.draw(self.window)
        self.layers.update(rects)


class TitleScreen(Screen):
    """The title screen is the first screen displayed."""

    def __init__(self):
        Screen.__init__(self)
        self.layers = pygame.sprite.LayeredDirty()
        self.add()

    def add(self):
        self.title = Text("menu", 24, (255,0,0), "Title Screen Goes Here")
        self.help = Text("menu", 16, (255,255,255),
            "Press 'n' to start a new game.")
        text = pygame.sprite.Group([self.title, self.help])
        all_sprites = pygame.sprite.OrderedUpdates([
            text])
        for sprite in all_sprites:
            self.layers.add(sprite)

    def draw(self):
        self.title.rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-20 ]
        self.help.rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2+20 ]
        rects = self.layers.draw(self.window)
        self.layers.update(rects)


class WorldScreen(Screen):
    """The main game screen with a world to wander around."""

    def __init__(self, level):
        Screen.__init__(self)
        self.camera = pygame.Rect((0,0), CAMERA_SIZE)
        self.dialog = Dialog()
        self.map = Map(level)
        self.player = Player(self)
        self.layers = pygame.sprite.LayeredDirty()
        self.add()
        self.map.scroll(self.camera, self.player)

    def add(self):
        """Add sprites to the screen in the correct order."""

        characters = pygame.sprite.Group([
            self.player])
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

    def toggle_dialog(self):
        """Toggles the status menu dialog."""

        if self.dialog.toggle:
            self.dialog.toggle = False
        else:
            self.dialog.toggle = True

    def start_battle(self):
        """Starts a battle screen."""

        if Die(PLAYER_ENCOUNTER_ROLL).roll() == 1:
            pygame.time.set_timer(BATTLE_EVENT, 1000)

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
        self.layers = pygame.sprite.LayeredDirty()
        self.add()

    def add(self):
        self.title = Text("menu", 24, (255,0,0), "Battle Screen Goes Here")
        self.help = Text("menu", 16, (255,255,255),
            "Press 'Esc' to go back to the game.")
        text = pygame.sprite.Group([self.title, self.help])
        all_sprites = pygame.sprite.OrderedUpdates([
            text])
        for sprite in all_sprites:
            self.layers.add(sprite)

    def draw(self):
        self.title.rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2-20 ]
        self.help.rect.center = [ WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2+20 ]
        rects = self.layers.draw(self.window)
        self.layers.update(rects)
