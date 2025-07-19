import os
from sim import run_sim
from analyze import tournament_start
from visualize import vis_strat_perf
from strats import STRATEGIES
from constant import (
    DEFAULT_VISUALIZATION_GAMES, DEFAULT_TOURNAMENT_GAMES,
    COMPARISON_DIR, STRATEGIES_DIR, TOURNAMENT_DIR,
    SCORE_DIST_FILE, STRATEGY_COMP_FILE, TOURNAMENT_RESULTS_FILE
)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
print("yahtzee strategy analysis suite")
print("\nthis script will run a comprehensive analysis of all yahtzee strategies.")
print("the analysis includes:")
print("\t1. basic simulation of all strategies")
print("\t2. tournament-style head-to-head comparisons")
print("\t3. detailed visualization of each strategy")
print("\nnote: this may take some time to complete.")

input("\npress enter to begin..")

clear()
print("step 1 - running basic simulation for all strategies")
run_sim()

input("\npress enter to continue to tournament analysis..")

clear()
print("step 2 - running tournament analysis")
tournament_start(n_games=DEFAULT_TOURNAMENT_GAMES)

input("\npress enter to continue to individual strategy visualizations..")

for s in STRATEGIES:
    clear()
    print("step 3 - visualizing %s strategy" % s)
    vis_strat_perf(s, n_games=DEFAULT_VISUALIZATION_GAMES)
    
    if s != list(STRATEGIES.keys())[-1]:
        input("\npress enter to visualize the next strategy..")

clear()
print("analysis complete")
print("\nall analysis has been completed. the following files were generated:")
print("\t- %s -overall score distribution comparison" % os.path.join(COMPARISON_DIR, SCORE_DIST_FILE))
print("\t- %s - key metrics comparison" % os.path.join(COMPARISON_DIR, STRATEGY_COMP_FILE))
print("\t- %s - head-to-head win rates" % os.path.join(TOURNAMENT_DIR, TOURNAMENT_RESULTS_FILE))

for s in STRATEGIES:
    print("\t- %s - detailed analysis" % os.path.join(STRATEGIES_DIR, "%s_analysis.png" % s.replace(' ', '_')))

print("\nreview these files to determine the most effective yahtzee strategy.")