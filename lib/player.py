from constants import *
from sprite import PlayerSprite

class Player(PlayerSprite):
    """The main player character."""

    def __init__(self, window, map):
        PlayerSprite.__init__(self, window, map)
        self.name = "Player Name"
