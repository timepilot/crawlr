import pygame
from data import *
from config import *

class Text(pygame.sprite.DirtySprite):
    """A sprite for text loaded from a font."""

    def __init__(self, font_name, font_size, font_color, font_text):
        pygame.sprite.DirtySprite.__init__(self)
        font_name = load_font(font_name, font_size)
        self.image = font_name.render(font_text, True, font_color)
        self.rect = self.image.get_rect()

    def update(self, rects):
        pygame.display.update(rects)


class Dialog(pygame.sprite.DirtySprite):
    """The dialog window used for story and character dialog."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = load_image('interface', 'dialog')
        self.rect = pygame.Rect((0, WINDOW_SIZE[1]), self.image.get_size())
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.bottom = WINDOW_SIZE[1] - 32
        self.toggle = False
        self.draw()

    def draw(self):
        print 1
