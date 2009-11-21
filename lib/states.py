import sys
import pygame
from pygame.locals import *
from constants import *
from screens import GameScreen

class BaseState(object):

    def __init__(self, window):
        self.window = window
        self.state = self
        self.clock = pygame.time.Clock()

    def show_debug(self):
        """Print debugging info to console."""

        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (int(self.clock.get_fps()), FRAME_RATE)

    def run(self):
        while True:
            self.clock.tick(FRAME_RATE)
            self.state.check_events()
            self.state.draw()

    def switch(self, state):
        self.state = None
        self.state = state
        self.run()

    def exit(self):
        pygame.quit()
        sys.exit(0)


class TitleScreenState(BaseState):

    def __init__(self, window):
        BaseState.__init__(self, window)

    def draw(self):
        self.window.fill((0,0,0))
        pygame.display.update()

    def check_events(self):
        """
        Title screen events:
        Esc:    exit game
        F:      toggle fullscreen
        N:      new game
        """

        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_f: pygame.display.toggle_fullscreen()
                elif event.key == K_n:
                    self.switch(GameScreenState(self.window))


class GameScreenState(BaseState):

    def __init__(self, window):
        BaseState.__init__(self, window)
        self.screen = GameScreen(self.window, 1)

    def draw(self):
        self.screen.draw()
        self.show_debug()

    def check_events(self):
        """
        Check for user input in the game.
        Esc:    exit to title screen
        F:      toggle fullscreen
        D:      toggle display
        Arrows: move player
        """

        self.move_keys = self.screen.player.move_keys
        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_f: pygame.display.toggle_fullscreen()
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

    def show_debug(self):
        BaseState.show_debug(self)
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
        self.switch(TitleScreenState(self.window))
