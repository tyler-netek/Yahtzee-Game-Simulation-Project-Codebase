import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from constant import (
    DEFAULT_NUM_SIMULATIONS, FIGURE_WIDTH, FIGURE_HEIGHT, 
    LARGE_FIGURE_WIDTH, LARGE_FIGURE_HEIGHT, HIST_BINS, BAR_WIDTH, 
    COMPARISON_DIR, SCORE_DIST_FILE, STRATEGY_COMP_FILE, CATEGORIES
)
from strats import STRATEGIES
import os
from util import game_run, calc_stats, calc_cat_stats

def res_analyze(res: List[Dict[str, Any]], strat_name: str) -> Dict[str, Any]:
    stats = calc_stats(res)
    cat_stats = calc_cat_stats(res)
    
    print("\nanalysis for strategy: " + strat_name)
    print("basic statistics:")
    print("\taverage score: %.2f" % stats["avg"])
    print("\tmedian score: %.2f" % stats["med"])
    print("\tstandard deviation: %.2f" % stats["std"])
    print("\tmin score: %d/max score: %d" % (stats["min"], stats["max"]))
    print("\tupper section bonus rate: %.2f%%" % stats["bonus_pct"])
    print("\tyahtzee success rate: %.2f%%" % stats["ytz_pct"])
    print("\ncategory usage patterns:")
    for sec, cats in CATEGORIES.items():
        print("\t%s section:" % sec.lower())
        for c in cats:
            use_pct = cat_stats["usage"].get(c, 0)
            avg_score = cat_stats["scores"].get(c, 0)
            print("\t\t%s: %.2f%% usage, avg score: %.2f" % (c, use_pct, avg_score))
    
    return stats

def plot_dist(stats: Dict[str, Dict[str, Any]]) -> None:
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    for name, s in stats.items():
        plt.hist(s["scores"], bins=HIST_BINS, alpha=0.5, label=name)
    plt.title("score distribution by strategy")
    plt.xlabel("score")
    plt.ylabel("frequency")
    plt.legend()
    out = os.path.join(COMPARISON_DIR, SCORE_DIST_FILE)
    plt.savefig(out)
    print("\nscore distribution plot saved as '%s'" % out)

def plot_comp(stats: Dict[str, Dict[str, Any]]) -> None:
    strats = list(stats.keys())
    avgs = [s["avg"] for s in stats.values()]
    stds = [s["std"] for s in stats.values()]
    bonus = [s["bonus_pct"] for s in stats.values()]
    ytz = [s["ytz_pct"] for s in stats.values()]
    x = np.arange(len(strats))
    fig, ax = plt.subplots(figsize=(LARGE_FIGURE_WIDTH, LARGE_FIGURE_HEIGHT))
    ax.bar(x - BAR_WIDTH*1.5, avgs, BAR_WIDTH, label='avg score/10')
    ax.bar(x - BAR_WIDTH/2, stds, BAR_WIDTH, label='std dev')
    ax.bar(x + BAR_WIDTH/2, bonus, BAR_WIDTH, label='bonus rate %')
    ax.bar(x + BAR_WIDTH*1.5, ytz, BAR_WIDTH, label='yahtzee rate %')
    ax.set_ylabel('value')
    ax.set_title('strategy comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(strats, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    out = os.path.join(COMPARISON_DIR, STRATEGY_COMP_FILE)
    plt.savefig(out)
    print("strategy comparison chart saved as '%s'" % out)

def run_sim() -> None:
    n_sims = DEFAULT_NUM_SIMULATIONS
    print("running yahtzee simulation (%d games per strategy)\n" % n_sims)

    stats = dict()

    for name in STRATEGIES:
        print("simulating %s strategy.." % name)
        res = [game_run(name) for _ in range(n_sims)]
        stats[name] = res_analyze(res, name)

    print("\n\nstrategy comparison summary")
    sorted_stats = sorted(stats.items(), reverse=True, key=lambda x: x[1]["avg"])

    for i, (name, s) in enumerate(sorted_stats):
        print("%d. %s:" % (i+1, name))
        print("\taverage: %.2f ± %.2f" % (s['avg'], s['std']))
        print("\tmedian: %.2f" % s['med'])
        print("\tbonus rate: %.2f%%" % s['bonus_pct'])
        print("\tyahtzee rate: %.2f%%" % s['ytz_pct'])
        print("\trisk (std dev): %.2f" % s['std'])
        print("\trange: %d - %d" % (s['min'], s['max']))

    plot_dist(stats)
    plot_comp(stats)

run_sim()