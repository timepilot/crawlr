from characters import Monster

class Slug(Monster):
    """A giant slug."""

    def __init__(self, screen):
        Monster.__init__(self, screen)
        self.name = "Slug"
        self.hp = 2
        self.hp_max = 2
        self.gold = 2
        self.max_amount = 3


class PoisonSlug(Monster):
    """A giant slug that has a poisonous attack."""

    def __init__(self, screen):
        Monster.__init__(self, screen)
        self.name = "PoisonSlug"
        self.hp = 2
        self.hp_max = 2
        self.exp = 10
        self.gold = 2
        self.max_amount = 1


class MagiSlug(Monster):
    """A giant slug that can cast spells."""

    def __init__(self, screen):
        Monster.__init__(self, screen)
        self.name = "MagiSlug"
        self.hp = 2
        self.hp_max = 2
        self.exp = 20
        self.gold = 2
        self.max_amount = 1


class Hawk(Monster):
    """A flying creature."""

    def __init__(self, screen):
        Monster.__init__(self, screen)
        self.name = "Hawk"
        self.hp = 2
        self.hp_max = 2
        self.exp = 20
        self.gold = 2
        self.max_amount = 2


MONSTER_DICT = {
    1: [ Slug, PoisonSlug, MagiSlug, Hawk ]
    }
