from characters import *

class PartyManager(object):
    """A manager that can add and remove characters to/from the party."""

    def __init__(self, screen):
        self.screen = screen
        self.all_chars = {
            'hero':     CharHero(screen),
            'test':     CharTest(screen) }
        self.chars = {
            'hero': self.all_chars['hero'] }
        self.hero = self.chars['hero']

    def add(self, char):
        """Add a new party character to the party."""

        if not self.all_chars[char] in self.screen.party_sprites:
            self.chars[char] = self.all_chars[char]
            self.chars[char].__init__(self.screen)
            self.screen.party_sprites.add(self.chars[char])
            self.screen.add_all_sprites()

    def remove(self, char):
        """Remove a character from the party."""

        if self.all_chars[char] in self.screen.party_sprites:
            self.chars[char].kill()
            del self.chars[char]
