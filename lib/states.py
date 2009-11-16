import pygame
from pygame.locals import *
from constants import *
from scene import Scene

class BaseState(object):

    def __init__(self, window):
        self.running = True
        self.window = window
        self.clock = pygame.time.Clock()

    def show_debug(self):
        """Print debugging info to console."""

        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (int(self.clock.get_fps()), FRAME_RATE)

    def exit(self):
        self.running = False


class GameState(BaseState):

    def __init__(self, window):
        BaseState.__init__(self, window)

    def run(self):
        self.scene = Scene(self.window, 1)
        while self.running:
            self.clock.tick(FRAME_RATE)
            self.check_events()
            self.scene.draw()
            self.show_debug()

    def check_events(self):
        """Check for user input in the game."""

        self.move_keys = self.scene.player.move_keys
        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_f: pygame.display.toggle_fullscreen()
                elif event.key == K_n: self.scene.reload(self)
                elif event.key == K_d: self.scene.toggle_dialog()
                elif event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(True, pygame.key.name, event.key)
            elif event.type == KEYUP:
                if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(False, pygame.key.name, event.key)

    def player_input(self, moving, name, key):
        """Controls key input to the player character."""

        if moving:
            self.move_keys.append(name(key))
            self.scene.player.direction = self.move_keys[-1]
            self.scene.player.stop = False
        else:
            if len(self.move_keys) > 0:
                keyid = self.move_keys.index(name(key))
                del self.move_keys[keyid]
                if len(self.move_keys) != 0:
                    self.scene.player.direction = (self.move_keys[-1])
                else: self.scene.player.stop = True

    def show_debug(self):
        BaseState.show_debug(self)
        if SHOW_RECTS:
            self.scene.map.layers['terrain'].image.fill(
                (0,0,0), self.scene.player.collide_rect)
            for rect in (self.scene.map.nowalk):
                self.scene.map.layers['terrain'].image.fill(
                    (255,255,255), rect)
        if SHOW_TERRAIN:
            print "Current terrain: " + (
                self.scene.player.current_terrain)
        if SHOW_REGION:
            print "Current region: " + (
                self.scene.player.current_region)
