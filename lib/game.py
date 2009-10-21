from os import environ
from sys import exit
import pygame
from pygame.locals import *
from constants import *
from scene import Scene

class Game(object):
    """Creates the game and manages the main loop."""

    def __init__(self):
        """Create a new game window."""

        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.running = True
        self.fullscreen = False
        self.window = pygame.display.set_mode(WINDOW_SIZE, self.fullscreen,
            COLOR_DEPTH)
        pygame.display.set_caption(GAME_NAME)
        pygame.mouse.set_visible(False)

    def run(self):
        """Runs the main game loop."""

        # Create the main game objects.
        self.clock = pygame.time.Clock()
        self.scene = Scene(self.window, 1)

        # For each frame, check for input and redraw accordingly.
        while self.running:
            self.clock.tick(FRAME_RATE)
            self.check_events()
            self.scene.draw()
            self.show_debug()

    def check_events(self):
        """Check for user input in the game."""

        self.move_keys = self.scene.player.move_keys
        for event in pygame.event.get():
            if event.type == QUIT: self.exit
            elif event.type == KEYDOWN:
                key_name = pygame.key.name
                key = event.key
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_f: pygame.display.toggle_fullscreen()
                elif event.key == K_n: self.scene.reload(self)
                elif event.key == K_d: self.show_dialog()
                elif event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(True, key_name, key)
            elif event.type == KEYUP:
                key_name = pygame.key.name
                key = event.key
                if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    self.player_input(False, key_name, key)

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

    def toggle_dialog(self):
        """Toggles the status menu dialog."""

        # TODO: Create dialog object
        #if self.scene.dialog.toggle:
        #    self.scene.dialog.toggle = False
        #else:
        #    self.scene.dialog.toggle = True
        pass

    def show_debug(self):
        """Print debugging info to console."""

        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (int(self.clock.get_fps()), FRAME_RATE)
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

    def exit(self):
        """Exits the game."""

        self.running = False
