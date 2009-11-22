from random import seed, choice
from time import time

class Die(object):
    """Die used to determine outcomes of game events."""

    def __init__(self, sides=6):
        try: self.sides = range(1, sides + 1)
        except TypeError: self.sides = list(sides)

    def roll(self, times=1):
        """Seed randomization with current time and rolls a die the specified
            number of times."""

        t = time()
        seed(t)
        total = 0
        for i in range(1, times + 1):
            roll = choice(self.sides)
            total += roll
        return total
