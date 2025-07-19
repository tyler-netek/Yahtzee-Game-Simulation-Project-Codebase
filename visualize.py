import numpy as np
from strats import STRATEGIES
import matplotlib.pyplot as plt
from sim import game_run
from collections import defaultdict
import os
from constant import (
    DEFAULT_VISUALIZATION_GAMES, DETAILED_FIGURE_WIDTH, DETAILED_FIGURE_HEIGHT,
    HIST_BINS, RUNNING_AVG_WINDOW, STRATEGIES_DIR
)

def vis_strat_perf(strat, n_games=DEFAULT_VISUALIZATION_GAMES):
    print("analyzing %s over %d games.." % (strat, n_games))
    
    res = [game_run(strat) for _ in range(n_games)]
    scs = [r["score"] for r in res]
    
    cat_scs = defaultdict(list)
    for r in res:
        for cat, sc in r["all_scores"].items():
            if sc is not None:
                cat_scs[cat].append(sc)
    
    fig = plt.figure(figsize=(DETAILED_FIGURE_WIDTH, DETAILED_FIGURE_HEIGHT))
    
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.hist(scs, bins=HIST_BINS, color='skyblue', edgecolor='black')
    ax1.set_title('%s score distribution' % strat)
    ax1.set_xlabel('score')
    ax1.set_ylabel('frequency')
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
    ax2.set_title('average score by category')
    ax2.set_xlabel('average score')
    
    ax3 = fig.add_subplot(2, 2, 3)
    cat_use = defaultdict(int)
    for r in res:
        for cat in r["cats"]:
            cat_use[cat] += 1
    
    cats = list(cat_use.keys())
    uses = [cat_use[cat] for cat in cats]
    
    idxs = np.argsort(uses)
    s_cats = [cats[i] for i in idxs]
    s_uses = [uses[i] for i in idxs]
    
    ax3.barh(s_cats, s_uses, color='salmon')
    ax3.set_title('category usage frequency')
    ax3.set_xlabel('number of times used')
    
    ax4 = fig.add_subplot(2, 2, 4)
    
    win = min(RUNNING_AVG_WINDOW, n_games)
    run_avg = np.convolve(scs, np.ones(win)/win, mode='valid')
    
    ax4.plot(range(len(run_avg)), run_avg, color='purple')
    ax4.set_title('running average score (window: %d games)' % win)
    ax4.set_xlabel('game number')
    ax4.set_ylabel('average score')
    ax4.axhline(np.mean(scs), color='red', linestyle='dashed', 
                label='overall mean: %.2f' % np.mean(scs))
    ax4.legend()
    
    plt.tight_layout()
    out = os.path.join(STRATEGIES_DIR, "%s_analysis.png" % strat.replace(' ', '_'))
    plt.savefig(out)
    print("visualization saved as '%s'" % out)
    
    print("\nsummary statistics for %s:" % strat)
    print("average score: %.2f" % np.mean(scs))
    print("median score: %.2f" % np.median(scs))
    print("standard deviation: %.2f" % np.std(scs))
    print("min score: %d" % np.min(scs))
    print("max score: %d" % np.max(scs))
    
    bonus_pct = sum(1 for r in res if r["bonus"]) / n_games*100
    ytz_pct = sum(1 for r in res if r["ytz"] > 0) / n_games * 100
    
    print("upper section bonus rate: %.2f%%" % bonus_pct)
    print("yahtzee success rate: %.2f%%" % ytz_pct)
    
    return {
        "scs": scs,
        "cat_scs": cat_scs,
        "cat_use": cat_use
    }

print("yahtzee strategy visualization tool")
print("\navailable strategies:")

strats = list(STRATEGIES.keys())
for i, s in enumerate(strats):
    print("%d. %s" % (i+1, s))

idx = int(input("\nselect a strategy to visualize (number): ")) - 1
n = int(input("number of games to simulate (default: %d): " % DEFAULT_VISUALIZATION_GAMES) or str(DEFAULT_VISUALIZATION_GAMES))

if 0 <= idx < len(strats):
    vis_strat_perf(strats[idx], n)
else:
    print("invalid strategy selection.")