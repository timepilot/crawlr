from characters import CharHero, CharTest

class CharacterManager(object):

    def __init__(self, screen):
        self.screen = screen
        self.party = {
            'hero':     CharHero(screen),
            'test':     CharTest(screen) }

    def party_add(self, char):
        """Add a new party character to the player's party."""

        if not self.party[char] in self.screen.party_sprites:
            self.screen.party_sprites.add(self.party[char])
            self.screen.add_all_sprites()

    def party_remove(self, char):
        """Remove a character from the player's party."""

        if self.party[char] in self.screen.party_sprites:
            self.party[char].kill()
