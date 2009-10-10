class BaseCharacter:
    """The base class from which all other game characters derive."""

    def __init__(self, name, hp, hp_max, mp, mp_max, attack, defense, spells,
            items):
        self.name = name
        self.hp = hp
        self.hp_max = hp_max
        self.mp = mp
        self.mp_map = mp_max
        self.attack = attack
        self.defense = defense
        self.spells = spells
        self.items = items


class PlayerCharacter(BaseCharacter):
    """The hero of the game."""

    def __init__(self, name="Hero", hp=10, hp_max=10, mp=0, mp_max=0,
        attack=1, defense=1, spells=[], items=[]):
        BaseCharacter.__init__(self, name, hp, hp_max, mp, mp_max, attack,
            defense, spells, items)
        self.exp = 0
        self.exp_max = 1000
        self.equipment = {
            'ArmorBody': '', 'ArmorHead': '', 'ArmorHands': '',
            'ArmorFeet': '', 'ArmorShield': '', 'RingLeft': '',
            'RingRight': '', 'BraceletLeft': '', 'BraceletRight': '',
            'Necklace': '', 'WeaponLeft': '', 'WeaponRight': '',
            'Items': items }
