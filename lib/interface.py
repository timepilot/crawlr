import pygame
from data import *
from config import *
from constants import *

class Font(pygame.sprite.DirtySprite):
    """A sprite for text loaded from a font."""

    def __init__(self, font_name, font_size, font_color, font_text):
        pygame.sprite.DirtySprite.__init__(self)
        self.font = load_font(font_name, font_size)
        self.image = self.font.render(font_text, True, font_color)
        self.rect = self.image.get_rect()

    def update(self, rects):
        pygame.display.update(rects)


class Dialog(object):
    """The base class for all dialog window objects."""

    def __init__(self):
        self.window = DialogWindow()
        self.text = DialogText("hugrhgshrilghrei gih h urhg uhrseg hureghuh e shuerhguerg erhgeruhg ershg uershg erushguresglhehgersluhglhreg  g erg er gher hgregh reghr g  gher ughre g regh reusglhghrseug hersul gre g slg hers uglh rlguhs glrehglesr gheru sg  sg srg sre g erughure ghreushg sr g serg re ger gser g rrs ghrelukghlshgrlse g sg serg  seg s rgs g es glse gs ger g ers glh srelg lsre glsre gl  sg rslg sre  hglserg se rg  srg g er slg g s rg selr ghslerhgeslr g   gl g hsl gl sg sl gherg h gslgslgsglhh gs g s g srelghrehgeurhghreg lr lg re lg lre hlgkjrel lgkr lr   hrejgh jjjergh e h h  erhgjjskelhgks erhgjk h  erskhg sg")
        self.toggle = False
        self.sprites = [
            self.window,
            self.text ]

    def scroll(self, dir):
        """Scroll the dialog text."""

        rect = self.text.rect
        height = self.text.font.get_height()
        if (dir == "up") and (rect.top < DIALOG_TOP):
            self.text.scroll([0, height])
        elif (dir =="down") and (rect.bottom > DIALOG_BOTTOM - height):
            self.text.scroll([0, -height])


class DialogWindow(pygame.sprite.DirtySprite):
    """The dialog window used for story and character dialog."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0] / 2, 0 ]
        self.rect.bottom = DIALOG_BOTTOM
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
        self.draw_background()
        self.draw_frame()

    def draw_background(self):
        """ Draw the dialog window background."""

        for row in range(0, DIALOG_TILES[1] - 1):
            for tile in range(0, DIALOG_TILES[0]):
                offset = (tile * 16 + 8, row * 16 + 8)
                self.image.blit(self.images[8], offset)

    def draw_frame(self):
        """Draw a frame around the dialog window."""

        for row in (range(0, DIALOG_TILES[1] / 2 - 1)):
            for tile in range(0, DIALOG_TILES[0] / 2):
                offset = (tile * 32 + 16, row * 32 + 16)
                self.image.blit(self.images[0], (offset[0], 0))
                self.image.blit(self.images[4],
                    (offset[0], DIALOG_MAX_SIZE[1]))
                self.image.blit(self.images[2],
                    (DIALOG_MAX_SIZE[0], offset[1]))
                self.image.blit(self.images[6], (0, offset[1]))
        self.image.blit(self.images[1],
            (DIALOG_MAX_SIZE[0], 0))
        self.image.blit(self.images[3],
            (DIALOG_MAX_SIZE[0], DIALOG_MAX_SIZE[1]))
        self.image.blit(self.images[5],
            (0, DIALOG_MAX_SIZE[1]))
        self.image.blit(self.images[7], (0, 0))


class DialogText(pygame.sprite.DirtySprite):
    """The moving text in the dialog window."""

    def __init__(self, text):
        pygame.sprite.DirtySprite.__init__(self)
        self.text = text
        self.font_sprite = Font("menu", 16, DIALOG_TEXT_COLOR, None)
        self.font = self.font_sprite.font
        self.image = pygame.Surface(
            (DIALOG_SIZE[0], DIALOG_TEXT_HEIGHT), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.top = DIALOG_TOP
        self.num_lines = 0
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
                self.num_lines = self.num_lines + 1
        if line != "":
            lines.append(self.font.render(line, 1, DIALOG_TEXT_COLOR))
            line = ""
            self.num_lines = self.num_lines + 1
        for num in range(self.num_lines):
            self.rect.height = num * height + 32
            self.image.blit(lines[num], (20, num * height + 16))

    def scroll(self, offset):
        """Scroll the dialog text."""

        self.dirty = 1
        self.rect.move_ip(offset)
