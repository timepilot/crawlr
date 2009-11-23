import sys
import pygame
from pygame.locals import *
from constants import *
from screens import *

class BaseState(object):
    """The base state that all other states subclass."""

    def __init__(self, window=None):
        self.window = window
        self.state = self
        self.clock = pygame.time.Clock()

    def run(self):
        """The main game loop that listens for events and draws the screen."""

        while True:
            self.limit_fps()
            self.state.show_debug(self.framerate)
            self.state.check_events()
            self.state.draw()

    def limit_fps(self):
        self.clock.tick(FRAME_RATE)
        self.framerate = int(self.clock.get_fps())

    def show_debug(self, fps):
        """Print debugging info to console."""

        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (fps, FRAME_RATE)

    def switch(self, state):
        self.state = state
        self.run()

    def exit(self):
        pygame.quit()
        sys.exit(0)


class InitState(Screen, BaseState):
    """State used to initialize the game and switch to the
    title screen state."""

    def __init__(self):
        Screen.__init__(self)
        BaseState.__init__(self, self.window)
        self.switch(TitleState())


class TitleState(BaseState):
    """State that controls the title screen."""

    def __init__(self):
        BaseState.__init__(self)
        self.screen = TitleScreen()

    def draw(self):
        self.screen.draw()

    def check_events(self):
        """
        Title screen events:
        Esc:    exit game
        N:      new game
        """

        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_n:
                    self.switch(WorldState())


class WorldState(BaseState):
    """State to control the world map screen."""

    def __init__(self):
        BaseState.__init__(self)
        self.screen = WorldScreen(1)

    def draw(self):
        """Draw the world screen graphics."""
        self.screen.draw()

    def check_events(self):
        """
        Check for user input on the world screen.
        Esc:    exit to title screen
        D:      toggle display
        Arrows: move player
        """

        self.move_keys = self.screen.player.move_keys
        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_d: self.screen.toggle_dialog()
                elif event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(True, pygame.key.name, event.key)
            elif event.type == KEYUP:
                if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(False, pygame.key.name, event.key)

    def player_input(self, moving, name, key):
        """Controls key input to the player character."""

        if moving:
            self.move_keys.append(name(key))
            self.screen.player.direction = self.move_keys[-1]
            self.screen.player.stop = False
        else:
            if len(self.move_keys) > 0:
                keyid = self.move_keys.index(name(key))
                del self.move_keys[keyid]
                if len(self.move_keys) != 0:
                    self.screen.player.direction = (self.move_keys[-1])
                else: self.screen.player.stop = True

    def show_debug(self, fps):
        BaseState.show_debug(self, fps)
        if SHOW_RECTS:
            self.screen.map.layers['terrain'].image.fill(
                (0,0,0), self.screen.player.collide_rect)
            for rect in (self.screen.map.nowalk):
                self.screen.map.layers['terrain'].image.fill(
                    (255,255,255), rect)
        if SHOW_TERRAIN:
            print "Current terrain: " + (
                self.screen.player.current_terrain)
        if SHOW_REGION:
            print "Current region: " + (
                self.screen.player.current_region)

    def exit(self):
        """Quit the main game screen returning to the title screen."""

        self.screen.destroy();
        self.switch(TitleState())
