from constants import *
from sprite import *
from character import *

class Monster(MonsterSprite, NonPlayerCharacter):

    def __init__(self, window, map):
        MonsterSprite.__init__(self, window, map)
        NonPlayerCharacter.__init__(self, "NPC")
