import pygame
from characters import *

class PartyManager(object):
    """A manager that can add and remove characters to/from the party."""

    def __init__(self, screen):
        self.screen = screen
        self.hero = CharHero(screen)
        self.all_chars = {
            'hero':     self.hero,
            'test':     CharTest(screen, self.hero) }
        self.chars = {}
        self.sprites = pygame.sprite.Group()

    def add(self, char):
        """Add a new party character to the party."""

        if not self.all_chars[char] in self.sprites:
            self.chars[char] = self.all_chars[char]
            if not char is "hero":
                self.chars[char].__init__(self.screen, self.hero)
            else:
                self.chars[char].__init__(self.screen)
            self.sprites.add(self.chars[char])
            self.screen.add_sprites()

    def remove(self, char):
        """Remove a character from the party."""

        if self.all_chars[char] in self.sprites:
            self.chars[char].kill()
            del self.chars[char]
