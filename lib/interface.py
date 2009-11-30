import pygame
from data import *
from config import *
from constants import *

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
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.bottom = WINDOW_SIZE[1] - 32
        self.toggle = False

    def update(self):
        self.draw()

    def draw(self):
        self.images = [
            load_tile("interface", "window_n"),
            load_tile("interface", "window_ne"),
            load_tile("interface", "window_e"),
            load_tile("interface", "window_se"),
            load_tile("interface", "window_s"),
            load_tile("interface", "window_sw"),
            load_tile("interface", "window_w"),
            load_tile("interface", "window_nw") ]

        # Draw window corners
        self.image.blit(self.images[1], (DIALOG_SIZE[0]-32,0))
        self.image.blit(self.images[3], (DIALOG_SIZE[0]-32, DIALOG_SIZE[1]-32))
        self.image.blit(self.images[5], (0,DIALOG_SIZE[1]-32))
        self.image.blit(self.images[7], (0,0))

        # Draw window sides
        start = 16
        tiles_x = DIALOG_SIZE[0]/32
        tiles_y = DIALOG_SIZE[1]/32
        for tile in (range(0, tiles_x)):
            self.image.blit(self.images[0], (tile * 32 + start, 0))
            self.image.blit(self.images[4], (tile * 32 + start,
                DIALOG_SIZE[1] - 32))
        for tile in (range(0, tiles_y-1)):
            self.image.blit(self.images[2], (DIALOG_SIZE[0] - 32,
                tile * 32 + start))
            self.image.blit(self.images[6], (0, tile * 32 + start))
