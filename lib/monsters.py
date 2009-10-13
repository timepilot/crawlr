from characters import Monster

class Slime(Monster):

    def __init__(self, scene):
        Monster.__init__(self, scene)
        self.hp = 10


class Slime2(Monster):

    def __init__(self, scene):
        Monster.__init__(self, scene)
        self.hp = 20


class Slime3(Monster):

    def __init__(self, scene):
        Monster.__init__(self, scene)
        self.hp = 30


MONSTER_LIST = [ Slime, Slime2, Slime3 ]
