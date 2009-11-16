from os import environ
from sys import exit
import pygame
from pygame.locals import *
from constants import *
from states import *

class Game(object):
    """Creates the game and manages the main loop."""

    def __init__(self):
        """Create a new game window."""

        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.fullscreen = False
        self.window = pygame.display.set_mode(WINDOW_SIZE, self.fullscreen,
            COLOR_DEPTH)
        pygame.display.set_caption(GAME_NAME)
        pygame.mouse.set_visible(False)

    def run(self):
        state = GameState(self.window)
        state.run()

