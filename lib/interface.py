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


class DialogWindow(pygame.sprite.DirtySprite):
    """The window used for story and dialog."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 0 ]
        self.rect.top = DIALOG_TOP
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
        self.text = DialogText("ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few ewfh fwe hfo ewhfowehfoiwe hfoe fh owef howe fhew ofh owehfo wefh owei foiw efohiwefhoiwehfoiwe hf owefh weoif hoiwe fhwe ihf weof howe ifh weofh weohf woe fowe hf weoifhowei hfoewh f owefh woe ifho wehf oweih fowei fhwe hf weof we fhowe hfoweifhowe fh weohf owef oweihf oiwe fo wehfowe fhowe hf woe fhowefhowe hfh wefwe fe wo fhwe hf wef we fhwe h fhwoefh wehf we of hwehf w eofhowe fh owehfowei hf ohwefoi weof owe fo woef h wehf hwef ewh fhw eofh we fo wefh owefew f ewfhweo hf weh foweh foe whof ewhfh ew fowe hf oew fh oew hho few")
        self.toggle = False
        self.text_layer = pygame.sprite.LayeredDirty([self.text])

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
        self.draw_background()
        self.draw_text()
        self.draw_frame()


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
            self.image.blit(lines[num], (20, num * height + 10))

    def update(self):
        """Redraw the dialog text."""

        self.dirty = 1

    def scroll(self, dir):
        """Scroll the dialog text."""

        offset = self.font.get_height()
        if (dir == "up") and (self.rect.top < 0):
            self.rect.move_ip([0, offset])
        if (dir == "down") and (self.rect.bottom > DIALOG_SIZE[1]):
            self.rect.move_ip([0, -offset])
        print self.rect.bottom
