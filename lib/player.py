from constants import *
from sprite import PlayerSprite
from character import PlayerCharacter

class Player(PlayerSprite, PlayerCharacter):
    """The main player character."""

    def __init__(self, window, map):
        PlayerSprite.__init__(self, window, map)
        PlayerCharacter.__init__(self, 'Hero')
