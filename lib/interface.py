import pygame
from data import *
from config import *
from constants import *
from sprite import *

class Text(pygame.sprite.DirtySprite):
    """A sprite for text loaded from a font."""

    def __init__(self, font_name, font_size, font_color, font_text):
        pygame.sprite.DirtySprite.__init__(self)
        self.font = load_font(font_name, font_size)
        self.image = self.font.render(font_text, True, font_color)
        self.rect = self.image.get_rect()

    def update(self, rects):
        pygame.display.update(rects)

class TextBox(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((DIALOG_SIZE[0], 20000), SRCALPHA, 32)
        self.rect = self.image.get_rect()

class Dialog(pygame.sprite.DirtySprite):
    """The dialog window used for story and character dialog."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.bottom = WINDOW_SIZE[1] - 32
        self.toggle = False
        self.images = [
            load_tile("interface", "window_n"),
            load_tile("interface", "window_ne"),
            load_tile("interface", "window_e"),
            load_tile("interface", "window_se"),
            load_tile("interface", "window_s"),
            load_tile("interface", "window_sw"),
            load_tile("interface", "window_w"),
            load_tile("interface", "window_nw"),
            load_tile("interface", "window_bg") ]
        self.text = Text("menu", 16, (224,224,224), None)
        self.font = self.text.font
        self.scroll_pos = 0
        self.tiles_x = DIALOG_SIZE[0]/16
        self.tiles_y = DIALOG_SIZE[1]/16
        self.max_x = DIALOG_SIZE[0]-32
        self.max_y = DIALOG_SIZE[1]-32
        self.draw()

    def draw(self):
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.textbox = TextBox()
        self.draw_background()
        self.draw_text()
        self.draw_frame()

    def draw_background(self):
        """ Draw the dialog window background."""

        for row in range(0, self.tiles_y-1):
            for tile in range(0, self.tiles_x):
                offset = (tile * 16 + 8, row * 16 + 8)
                self.image.blit(self.images[8], offset)

    def draw_text(self):
        """Draw the dialog text."""

        text_all = "This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text. This is some example text."
        words = text_all.rstrip().split(" ")
        line = ""
        num_lines = 0
        lines = []
        color = (224,224,224)
        for word in words:
            line = line + " " + word
            if line[0] == " ":
                line = line[1:]
            if self.font.size(line)[0] > self.max_x - 8:
                line = line.rstrip(word)
                lines.append(self.font.render(line, 1, color))
                line = word
                num_lines = num_lines + 1
        if line != "":
            lines.append(self.font.render(line, 1, color))
            line = ""
            num_lines = num_lines + 1
        for num in range(num_lines):
            self.textbox.image.blit(lines[num],
                (20, num * self.font.get_height() + 10))
        self.image.blit(self.textbox.image, (0, self.scroll_pos))

    def draw_frame(self):
        """Draw a frame around the dialog window."""

        for row in (range(0, self.tiles_y/2-1)):
            for tile in range(0, self.tiles_x/2):
                offset = (tile * 32 + 16, row * 32 + 16)
                self.image.blit(self.images[0], (offset[0], 0))
                self.image.blit(self.images[4], (offset[0], self.max_y))
                self.image.blit(self.images[2], (self.max_x, offset[1]))
                self.image.blit(self.images[6], (0, offset[1]))
        self.image.blit(self.images[1], (self.max_x, 0))
        self.image.blit(self.images[3], (self.max_x, self.max_y))
        self.image.blit(self.images[5], (0, self.max_y))
        self.image.blit(self.images[7], (0, 0))

    def update(self):
        self.draw()

    def scroll(self):
        self.dirty = 1
        self.scroll_pos-=self.font.get_height()
