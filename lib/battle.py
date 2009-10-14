from config import *
from constants import *
from random import choice
from dice import Die
from monsters import *

class Battle(object):
    """A battle has started."""

    def __init__(self, scene):
        self.scene = scene
        self.map = scene.map
        self.window = scene.window
        self.region = int(scene.player.current_region)
        self.monster_quantity = {}
        self.monster_list = []

    def create_monsters(self):
        """Create a random list of monsters from the current region number."""

        # Create a dictionary for the amount of each type of monster.
        for monster in MONSTER_DICT[self.region]:
            self.monster_quantity[monster] = 0

        # Pick monsters randomly while staying within the maximum allowed.
        times = 0
        while times < Die(MAX_MONSTERS).roll():
            monster = choice(MONSTER_DICT[self.region])
            if self.monster_quantity[monster] < monster(self).max_amount:
                self.monster_list.append(monster)
                self.monster_quantity[monster] += 1
            times += 1

        # Show monsters for battle.
        if SHOW_MONSTERS:
            print "A battle has started on region #" + str(self.region) + (
                " with:")
            for monster in self.monster_list:
                print monster(self).name
