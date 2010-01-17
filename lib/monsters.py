from characters import BaseCharacter
from sprite import MonsterSprite

class BaseMonster(MonsterSprite, BaseCharacter):
    """The base class for all other monsters."""

    def __init__(self, screen, name):
        MonsterSprite.__init__(self, screen, name)
        BaseCharacter.__init__(self, name, hp=1, hp_max=1, mp=0, mp_max=0,
            attack=1, defense=1)
        self.max_amount = 1
        self.frequency = 0
        self.size = 2
        self.movement = 1
        self.num_attacks = 1
        self.damage = 1
        self.morale = 5


class Slug(BaseMonster):
    """A giant slug."""

    def __init__(self, screen, name="Slug"):
        BaseMonster.__init__(self, screen, name)
        self.hp = 2
        self.hp_max = 2
        self.gold = 2
        self.max_amount = 3


class PoisonSlug(BaseMonster):
    """A giant slug that has a poisonous attack."""

    def __init__(self, screen, name="PoisonSlug"):
        BaseMonster.__init__(self, screen, name)
        self.hp = 2
        self.hp_max = 2
        self.exp = 10
        self.gold = 2
        self.max_amount = 1


class MagiSlug(BaseMonster):
    """A giant slug that can cast spells."""

    def __init__(self, screen, name="MagiSlug"):
        BaseMonster.__init__(self, screen, name)
        self.hp = 2
        self.hp_max = 2
        self.exp = 20
        self.gold = 2
        self.max_amount = 1


class Hawk(BaseMonster):
    """A flying creature."""

    def __init__(self, screen, name="Hawk"):
        BaseMonster.__init__(self, screen, name)
        self.hp = 2
        self.hp_max = 2
        self.exp = 20
        self.gold = 2
        self.max_amount = 2


MONSTER_DICT = {
    "Slug":         Slug,
    "PoisonSlug":   PoisonSlug,
    "MagiSlug":     MagiSlug,
    "Hawk":         Hawk
    }
