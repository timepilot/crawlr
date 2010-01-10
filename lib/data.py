from os import path
from configobj import ConfigObj
import pygame
from pygame.locals import *

DATA_PY = path.abspath(path.dirname(__file__))
DATA_DIR = path.normpath(path.join(DATA_PY, '..', 'data'))

class LoadSprite(object):
    """Load a sprite from a spritesheet."""

    def __init__(self, type, subtype, filename):
        self.sheet = load_image(type, subtype, filename)

    def image(self, rect, colorkey=None, alpha=False):
        rect = Rect(rect)
        if alpha:
            image = pygame.Surface(rect.size).convert_alpha()
        else:
            image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    def images(self, rects, colorkey=None):
        imgs = []
        for rect in rects:
            imgs.append(self.image(rect, colorkey))
        return imgs

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
