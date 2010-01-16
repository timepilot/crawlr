from constants import *
from sprite import *

class BaseCharacter(object):
    """The base class from which all other game characters derive."""

    def __init__(self, name, hp, hp_max, mp, mp_max, attack, defense,
            spells=[], items=[], exp=0, gold=0):
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
        self.gold = gold


class PlayerCharacter(PlayerSprite, BaseCharacter):
    """The main player character."""

    def __init__(self, screen, name, hp=10, hp_max=10, mp=0, mp_max=0,
            attack=1, defense=1):
        PlayerSprite.__init__(self, screen, name)
        BaseCharacter.__init__(self, name, hp, hp_max, mp, mp_max, attack,
            defense)
        self.exp_max = 1000
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


class Monster(MonsterSprite, BaseCharacter):
    """The base class for all other monsters."""

    def __init__(self, screen, name="Monster", hp=1, hp_max=1, mp=0, mp_max=0,
            attack=1, defense=1):
        MonsterSprite.__init__(self, screen)
        BaseCharacter.__init__(self, name, hp, hp_max, mp, mp_max, attack,
            defense)
        self.max_amount = 1
        self.frequency = 0
        self.size = 2
        self.movement = 1
        self.num_attacks = 1
        self.damage = 1
        self.morale = 5
