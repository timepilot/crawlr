from random import choice
from constants import *
from dice import Die
from monsters import *

class Battle(object):
    """A battle has started."""

    def __init__(self, scene):
        self.scene = scene
        self.map = scene.map
        self.window = scene.window
        self.region = int(scene.player.current_region)
        self.region_monsters = MONSTER_DICT[self.region]
        self.temp_monsters = []
        self.battle_monsters = []

    def create_monsters(self):
        """Randomly create the monsters for the battle."""

        # Create a list of monster instances for the current region.
        for monster in self.region_monsters:
            self.temp_monsters.append(monster(self))

        # Randomly select 1-4 regional monsters.
        num = Die(MONSTERS_MAX_AMOUNT).roll()
        while len(self.battle_monsters) < num:
            monster = choice(self.temp_monsters)
            if self.battle_monsters.count(monster) < monster.max_amount:
                self.battle_monsters.append(monster)

        # Show monsters for battle.
        if SHOW_MONSTERS:
            print "A battle has started on region #" + str(self.region) + (
                " with:")
            for monster in self.battle_monsters:
                print monster.name
