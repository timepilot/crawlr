from characters import CharHero, CharTest

class CharacterManager(object):

    def __init__(self, screen):
        self.party = {
            'hero':     CharHero(screen),
            'test':     CharTest(screen) }
