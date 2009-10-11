from sprite import *
from character import *

class Player(PlayerSprite, PlayerCharacter):
    """The main player character."""

    def __init__(self, scene):
        PlayerSprite.__init__(self, scene)
        PlayerCharacter.__init__(self, 'Hero')
