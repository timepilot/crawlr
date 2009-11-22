#!/usr/bin/env python

import sys
sys.path.insert(0, "lib")
from screens import Screen
from states import *

if __name__ == "__main__":
    game = TitleScreenState()
    game.run()
