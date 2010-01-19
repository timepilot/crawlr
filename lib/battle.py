from random import choice
from constants import *
from data import *
from monsters import *

class Battle(object):
    """A battle has started."""

    def __init__(self, screen):
        self.screen = screen
        self.map = screen.map
        self.region = screen.party.chars['hero'].current_region
        self.map_monsters = self.map.region_monsters[self.region]
        self.battle_monsters = []
        self.create_monsters()
        self.show_debug()

    def create_monsters(self):
        """Randomly create the monsters for the battle."""

        # Create a list of monster instances for the current region.
        temp_monsters = []
        for monster in self.map_monsters:
            temp_monsters.append(MONSTER_DICT[monster](self))

        # Randomly select 1-4 regional monsters.
        num = Die(MONSTERS_MAX_AMOUNT).roll()
        while len(self.battle_monsters) < num:
            monster = choice(temp_monsters)
            if self.battle_monsters.count(monster) < monster.max_amount:
                self.battle_monsters.append(monster)

    def show_debug(self):
        """Print the battle debug message."""

        if SHOW_MONSTERS:
            print "A battle has started on region #" + str(self.region) + (
                " with:")
            for monster in self.battle_monsters:
                print monster.name
