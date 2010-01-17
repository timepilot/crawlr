from characters import *

class PartyManager(object):
    """A manager that can add and remove characters to/from the party."""

    def __init__(self, screen):
        self.screen = screen
        self.list = {
            'hero':     CharHero(screen),
            'test':     CharTest(screen) }

    def add(self, char):
        """Add a new party character to the player's party."""

        if not self.list[char] in self.screen.party_sprites:
            self.screen.party_sprites.add(self.list[char])
            self.screen.add_all_sprites()

    def remove(self, char):
        """Remove a character from the player's party."""

        if self.list[char] in self.screen.party_sprites:
            self.list[char].kill()
