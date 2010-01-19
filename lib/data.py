from os import path
from random import seed, choice
from time import time
import pygame
from configobj import ConfigObj

DATA_PY = path.abspath(path.dirname(__file__))
DATA_DIR = path.normpath(path.join(DATA_PY, '..', 'data'))

class Die(object):
    """Die used to determine outcomes of game events."""

    def __init__(self, sides=6):
        try: self.sides = range(1, sides + 1)
        except TypeError: self.sides = list(sides)

    def roll(self, times=1):
        """Seed randomization with current time and rolls a die the specified
            number of times."""

        t = time()
        seed(t)
        total = 0
        for i in range(1, times + 1):
            roll = choice(self.sides)
            total += roll
        return total

def load_font(name, size):
    """Load a font file from disk."""

    file = path.join(DATA_DIR, 'fonts', name + '.ttf')
    font = pygame.font.Font(file, size)
    return font

def load_image(type, subtype, filename):
    """Load an image file from disk."""

    file = path.join(DATA_DIR, 'images', type, subtype, filename + '.png')
    image = pygame.image.load(file).convert_alpha()
    return image

def load_map(map, mode='rb'):
    """Load a map file from disk."""

    return ConfigObj(open(path.join(DATA_DIR, 'maps', map + '.map'), mode))
