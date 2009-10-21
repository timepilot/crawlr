import pygame
from data import *
from config import *

class Dialog(pygame.sprite.DirtySprite):
    """
    The dialog window used for story and character dialog.
    """

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = load_image('interface', 'dialog')
        self.rect = pygame.Rect((0, WINDOW_SIZE[1]),
            self.image.get_size())
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.bottom = WINDOW_SIZE[1] - 32
        self.toggle = False

    def update(self):
        self.dirty = 1
