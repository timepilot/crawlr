#!/usr/bin/env python

import sys
sys.path.insert(0, "lib")
from game import Game

if __name__ == "__main__":
    crawlr = Game()
    crawlr.create()
    crawlr.run()
