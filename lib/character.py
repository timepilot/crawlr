class BaseCharacter(object):
    """The base class from which all other game characters derive."""

    def __init__(self, name, hp, hp_max, mp, mp_max, attack, defense, spells,
            items, exp, gold):
        self.name = name
        self.hp = hp
        self.hp_max = hp_max
        self.mp = mp
        self.mp_map = mp_max
        self.attack = attack
        self.defense = defense
        self.spells = spells
        self.items = items
        self.exp = exp
        self.gold = gold


class PlayerCharacter(BaseCharacter):
    """The hero of the game."""

    def __init__(self, name="Hero", hp=10, hp_max=10, mp=0, mp_max=0,
            attack=1, defense=1, spells=[], items=[], exp=0, gold=0):
        BaseCharacter.__init__(self, name, hp, hp_max, mp, mp_max, attack,
            defense, spells, items, exp, gold)
        self.exp_max = 1000
        self.equipment = {
            'ArmorBody': '', 'ArmorHead': '', 'ArmorHands': '',
            'ArmorFeet': '', 'ArmorShield': '', 'RingLeft': '',
            'RingRight': '', 'BraceletLeft': '', 'BraceletRight': '',
            'Necklace': '', 'WeaponLeft': '', 'WeaponRight': '',
            'Items': items }


class NonPlayerCharacter(BaseCharacter):
    """A computer-controlled character."""

    def __init__(self, name="NPC", hp=1, hp_max=1, mp=0, mp_max=0, attack=1,
            defense=1, spells=[], items=[], exp=0, gold=0, frequency=0, size=2,
            movement=1, num_attacks=1, damage=1, morale=5):
        BaseCharacter.__init__(self, name, hp, hp_max, mp, mp_max, attack,
            defense, spells, items, exp, gold)
        self.frequency = frequency
        self.size = size
        self.movement = movement
        self.num_attacks = num_attacks
        self.damage = damage
        self.morale = morale
