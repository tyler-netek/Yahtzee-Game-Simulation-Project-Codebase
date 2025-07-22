import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Dict, Any
from constant import (
    DEFAULT_VISUALIZATION_GAMES, DETAILED_FIGURE_WIDTH, DETAILED_FIGURE_HEIGHT,
    HIST_BINS, RUNNING_AVG_WINDOW, STRATEGIES_DIR
)
from strats import STRATEGIES
from util import game_run, calc_stats, calc_cat_stats, print_strategy_list

def vis_strat_perf(strat: str, n_games: int = DEFAULT_VISUALIZATION_GAMES) -> Dict[str, Any]:
    print("Analyzing %s over %d games.." % (strat, n_games))
    
    res = [game_run(strat) for _ in range(n_games)]
    stats = calc_stats(res)
    cat_stats = calc_cat_stats(res)
    
    scs = stats["scores"]
    cat_scs = dict()
    cat_use = dict()
    
    for r in res:
        for cat, sc in r["all_scores"].items():
            if sc is not None:
                if cat not in cat_scs:
                    cat_scs[cat] = []
                cat_scs[cat].append(sc)
        
        for cat in r["cats"]:
            cat_use[cat] = cat_use.get(cat, 0) + 1
    
    fig = plt.figure(figsize=(DETAILED_FIGURE_WIDTH, DETAILED_FIGURE_HEIGHT))
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.hist(scs, bins=HIST_BINS, color='skyblue', edgecolor='black')
    ax1.set_title('%s Score distribution' % strat)
    ax1.set_xlabel('Score')
    ax1.set_ylabel('Frequency')
    ax1.axvline(np.mean(scs), color='red', linestyle='dashed', linewidth=1, 
                label='mean: %.2f' % np.mean(scs))
    ax1.axvline(np.median(scs), color='green', linestyle='dashed', linewidth=1,
                label='median: %.2f' % np.median(scs))
    ax1.legend()
    
    ax2 = fig.add_subplot(2, 2, 2)
    cats = list(cat_scs.keys())
    avgs = [np.mean(cat_scs[cat]) for cat in cats]
    
    idxs = np.argsort(avgs)
    s_cats = [cats[i] for i in idxs]
    s_scs = [avgs[i] for i in idxs]
    
    ax2.barh(s_cats, s_scs, color='lightgreen')
    ax2.set_title('Average score by Category')
    ax2.set_xlabel('Average score')
    
    ax3 = fig.add_subplot(2, 2, 3)
    cats = list(cat_use.keys())
    uses = [cat_use[cat] for cat in cats]
    
    idxs = np.argsort(uses)
    s_cats = [cats[i] for i in idxs]
    s_uses = [uses[i] for i in idxs]
    
    ax3.barh(s_cats, s_uses, color='salmon')
    ax3.set_title('Category usage frequency')
    ax3.set_xlabel('Number of times used')
    
    ax4 = fig.add_subplot(2, 2, 4)
    
    win = min(RUNNING_AVG_WINDOW, n_games)
    run_avg = np.convolve(scs, np.ones(win)/win, mode='valid')
    
    ax4.plot(range(len(run_avg)), run_avg, color='purple')
    ax4.set_title('Running average score (window: %d games)' % win)
    ax4.set_xlabel('Game number')
    ax4.set_ylabel('Average score')
    ax4.axhline(np.mean(scs), color='red', linestyle='dashed', 
                label='Overall Mean: %.2f' % np.mean(scs))
    ax4.legend()
    
    plt.tight_layout()
    out = os.path.join(STRATEGIES_DIR, "%s_analysis.png" % strat.replace(' ', '_'))
    plt.savefig(out)
    print("Visualization saved as '%s'" % out)
    
    print("\nSummary statistics for %s:" % strat)
    print("\nAverage score: %.2f" % np.mean(scs))
    print("Median score: %.2f" % np.median(scs))
    print("Standard deviation: %.2f" % np.std(scs))
    print("Min score: %d" % np.min(scs))
    print("Max score: %d" % np.max(scs))
    
    bonus_pct = sum(1 for r in res if r["bonus"]) / n_games*100
    ytz_pct = sum(1 for r in res if r["ytz"] > 0) / n_games * 100
    
    print("Upper section bonus rate: %.2f%%" % bonus_pct)
    print("Yahtzee success rate: %.2f%%" % ytz_pct)
    
    return stats

print("Yahtzee strategy visualization tool")
print_strategy_list()

strats = list(STRATEGIES.keys())
try:
    idx = int(input("\nSelect a strategy to visualize (number): ")) - 1
    if 0 <= idx < len(strats):
        n = input("Number of games to simulate (default: %d): " % DEFAULT_VISUALIZATION_GAMES)
        n = int(n) if n else DEFAULT_VISUALIZATION_GAMES
        vis_strat_perf(strats[idx], n)
    else:
        print("Invalid strategy selection.")
except ValueError:
    print("Please enter a valid number")
except KeyboardInterrupt:
    print("\nExiting..")
    