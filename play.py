#!/usr/bin/env python

import sys
sys.path.insert(0, "lib")
from config import PROFILING
from states import InitState

if __name__ == "__main__":
    if not PROFILING:
        game = InitState()
    else:
        import cProfile, pstats
        prof = cProfile.run("InitState()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)
