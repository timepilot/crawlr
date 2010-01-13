import pygame
from data import *
from config import *
from constants import *
from random import choice

class Font(pygame.sprite.DirtySprite):
    """A sprite for text loaded from a font."""

    def __init__(self, font_name, font_size, font_color, font_text):
        pygame.sprite.DirtySprite.__init__(self)
        self.font = load_font(font_name, font_size)
        self.image = self.font.render(font_text, True, font_color)
        self.rect = self.image.get_rect()

    def update(self, rects):
        pygame.display.update(rects)


class StatsWindow(pygame.sprite.DirtySprite):
    """The area in the top left of the screen that displays party members and
        their statistics."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((128,256), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.left = 32
        self.rect.top = 32
        self.image1 = load_image("gui", "dialog", "dialog_n")

    def draw(self):
        #self.image.blit(self.image1, (0,0))
        pass

    def update(self):
        self.draw()


class DialogWindow(pygame.sprite.DirtySprite):
    """The window used for story and dialog."""

    def __init__(self, text):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.top = DIALOG_TOP
        self.images = [
            load_image("gui", "dialog", "dialog_n"),
            load_image("gui", "dialog", "dialog_ne"),
            load_image("gui", "dialog", "dialog_e"),
            load_image("gui", "dialog", "dialog_se"),
            load_image("gui", "dialog", "dialog_s"),
            load_image("gui", "dialog", "dialog_sw"),
            load_image("gui", "dialog", "dialog_w"),
            load_image("gui", "dialog", "dialog_nw"),
            load_image("gui", "dialog", "dialog_bg") ]
        self.text = DialogText(text)
        self.toggle = False
        self.text_layer = pygame.sprite.LayeredDirty([self.text])
        self.draw()

    def draw(self):
        self.draw_background()
        self.draw_text()
        self.draw_frame()

    def draw_background(self):
        """Draw the dialog window's translucent background."""

        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        for row in range(0, DIALOG_TILES[1] - 1):
            for tile in range(0, DIALOG_TILES[0]):
                offset = (tile * 16 + 8, row * 16 + 8)
                self.image.blit(self.images[8], offset)

    def draw_text(self):
        """Draw the text layer onto the window's background."""

        self.text_layer.update()
        self.text_layer.draw(self.image)

    def draw_frame(self):
        """Draw the dialog window's frame."""

        blit = self.image.blit
        for row in (range(0, DIALOG_TILES[1] / 2 - 1)):
            for tile in range(0, DIALOG_TILES[0] / 2):
                offset = (tile * 32 + 16, row * 32 + 16)
                blit(self.images[0], (offset[0], 0))
                blit(self.images[4], (offset[0], DIALOG_MAX_SIZE[1]))
                blit(self.images[2], (DIALOG_MAX_SIZE[0], offset[1]))
                blit(self.images[6], (0, offset[1]))
        blit(self.images[1], (DIALOG_MAX_SIZE[0], 0))
        blit(self.images[3], DIALOG_MAX_SIZE)
        blit(self.images[5], (0, DIALOG_MAX_SIZE[1]))
        blit(self.images[7], (0, 0))

    def update(self):
        """Redraw the dialog window."""

        self.dirty = 1
        if self.text.scrolling:
            self.draw()
            self.text.scrolling = False

    def destroy(self):
        self.text.kill()
        self.kill()
        self.text = None

class DialogText(pygame.sprite.DirtySprite):
    """The moving text in the dialog window."""

    def __init__(self, text):
        pygame.sprite.DirtySprite.__init__(self)
        self.text = text
        self.font_sprite = Font("menu", 16, DIALOG_TEXT_COLOR, None)
        self.font = self.font_sprite.font
        self.image = pygame.Surface(DIALOG_BUFFER_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.num_lines = 0
        self.scrolling = False
        self.draw()

    def draw(self):
        """Draw the dialog text."""

        words = self.text.rstrip().split(" ")
        line = ""
        lines = []
        height = self.font.get_height()
        for word in words:
            line = line + " " + word
            if line[0] == " ":
                line = line[1:]
            if self.font.size(line)[0] > DIALOG_MAX_SIZE[0] - 8:
                line = line.rstrip(word)
                lines.append(self.font.render(line, 1, DIALOG_TEXT_COLOR))
                line = word
                self.num_lines += 1
        if line != "":
            lines.append(self.font.render(line, 1, DIALOG_TEXT_COLOR))
            line = ""
            self.num_lines += 1
        for num in range(self.num_lines):
            self.rect.height = num * height + 32
            self.image.blit(lines[num], (20, num * height + 10))

    def update(self):
        """Redraw the dialog text."""

        self.dirty = 1

    def scroll(self, dir):
        """Scroll the dialog text."""

        self.scrolling = True
        offset = self.font.get_height()
        if (dir == "up") and (self.rect.top < 0):
            self.rect.move_ip([0, offset])
        if (dir == "down") and (self.rect.bottom > DIALOG_SIZE[1]):
            self.rect.move_ip([0, -offset])
