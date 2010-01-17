from constants import *
from sprite import PlayerSprite

class BaseCharacter(object):
    """The base class from which all other game characters derive."""

    def __init__(self, name, hp, hp_max, mp, mp_max, attack, defense,
            spells=[], items=[], exp=0, exp_max=0, gold=0):
        self.name = name
        self.hp = hp
        self.hp_max = hp_max
        self.mp = mp
        self.mp_max = mp_max
        self.attack = attack
        self.defense = defense
        self.spells = spells
        self.items = items
        self.exp = exp
        self.exp_max = exp_max
        self.gold = gold
        self.equipment = {
            'ArmorBody':        '',
            'ArmorHead':        '',
            'ArmorHands':       '',
            'ArmorFeet':        '',
            'ArmorShield':      '',
            'RingLeft':         '',
            'RingRight':        '',
            'BraceletLeft':     '',
            'BraceletRight':    '',
            'Necklace':         '',
            'WeaponLeft':       '',
            'WeaponRight':      '',
            'Items':            [] }


class CharHero(PlayerSprite, BaseCharacter):
    """The hero of the game."""

    def __init__(self, screen, name="hero"):
        PlayerSprite.__init__(self, screen, name)
        BaseCharacter.__init__(self, name, hp=10, hp_max=10, mp=0, mp_max=0,
            attack=1, defense=1, exp_max=1000)


class CharTest(PlayerSprite, BaseCharacter):
    """An extra character for testing."""

    def __init__(self, screen, name="test"):
        PlayerSprite.__init__(self, screen, name)
        BaseCharacter.__init__(self, name, hp=20, hp_max=20, mp=0, mp_max=0,
            attack=1, defense=1, exp_max=1000)
