from os import environ
from sys import exit
import pygame
from pygame.locals import *
from config import *
from scene import Scene

class Game(object):
    """Creates the game and manages the main loop."""

    def __init__(self):
        self.create()
        self.run()

    def create(self):
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

        self.clock = pygame.time.Clock()
        self.scene = Scene(self.window, 1)

        while self.running:
            self.clock.tick(FRAME_RATE)
            self.check_events()
            self.draw()

    def check_events(self):
        """Check for user input in the game."""

        move_keys = self.scene.player.move_keys

        for event in pygame.event.get():

            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                key_name = pygame.key.name
                key = event.key

                if event.key == K_ESCAPE:
                    self.running = False

                # Switch to fullscreen mode when 'F' key is pressed.
                elif event.key == K_f:
                    pygame.display.toggle_fullscreen()

                # Reload the scene when 'N' key is pressed.
                elif event.key == K_n:
                    for sprite in self.scene.all_sprites:
                        sprite.kill()
                        sprite = None
                    self.run()

                # Toggle dialog window when 'D' key is pressed.
                elif event.key == K_d:
                    if self.scene.dialog.toggle:
                        self.scene.dialog.toggle = False
                    else:
                        self.scene.dialog.toggle = True

                # Move the player when arrow keys are pressed.
                elif event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    move_keys.append(key_name(key))
                    self.scene.player.direction = move_keys[-1]
                    self.scene.player.stop = False

            elif event.type == KEYUP:
                key_name = pygame.key.name
                key = event.key

                # Stop moving the player when arrow keys are released.
                if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
                    if len(move_keys) > 0:
                        keyid = move_keys.index(key_name(key))
                        del move_keys[keyid]
                        if len(move_keys) != 0:
                            self.scene.player.direction = (move_keys[-1])
                        else:
                            self.scene.player.stop = True

    def draw(self):
        """Render graphics to the screen."""

        self.scene.draw()
        self.show_debug()

    def show_debug(self):
        """Print debugging info to console."""

        # Print framerate.
        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (int(self.clock.get_fps()), FRAME_RATE)

        # Show collisions.
        if SHOW_RECTS:
            self.scene.map.layers['terrain'].image.fill(
                (0,0,0), self.scene.player.collide_rect)
            for rect in (self.scene.map.nowalk):
                self.scene.map.layers['terrain'].image.fill(
                    (255,255,255), rect)

        # Print current terrain type.
        if SHOW_TERRAIN:
            print "Current terrain: " + (
                self.scene.player.current_terrain)

        # Print current region.
        if SHOW_REGION:
            print "Current region: " + (
                self.scene.player.current_region)

    def exit(self):
        """Exits the game."""

        pygame.quit()
