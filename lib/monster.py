from sprite import *
from character import *

class Monster(MonsterSprite, NonPlayerCharacter):

    def __init__(self, scene):
        MonsterSprite.__init__(self, scene)
        NonPlayerCharacter.__init__(self, "NPC")
