from os import path
from configobj import ConfigObj
import pygame
from pygame.locals import *

DATA_PY = path.abspath(path.dirname(__file__))
DATA_DIR = path.normpath(path.join(DATA_PY, '..', 'data'))

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
