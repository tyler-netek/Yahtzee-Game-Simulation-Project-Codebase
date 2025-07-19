import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from logic import Scorecard, roll
from constant import (
    NUM_ROLLS, NUM_TURNS, CATEGORIES, DEFAULT_NUM_SIMULATIONS,
    FIGURE_WIDTH, FIGURE_HEIGHT, LARGE_FIGURE_WIDTH, LARGE_FIGURE_HEIGHT,
    HIST_BINS, BAR_WIDTH, COMPARISON_DIR, SCORE_DIST_FILE, STRATEGY_COMP_FILE,
    UPPER_SECTION_BONUS_THRESHOLD, CATEGORY_YAHTZEE, NUM_DICE
)
from strats import STRATEGIES
import os

def turn_init(strat_func, hand, card):
    for __ in range(NUM_ROLLS - 1):
        keep = strat_func(hand, card)
        to_reroll = NUM_DICE - len(keep)
        if to_reroll == 0:
            break
        new = roll(to_reroll)
        hand = keep + new
    return hand

def game_run(strat_name):
    card = Scorecard()
    strat = STRATEGIES[strat_name]
    choices = list()
    for _ in range(NUM_TURNS):
        hand = roll(NUM_DICE)
        final = turn_init(strat['reroll'], hand, card)
        cat = strat['score'](final, card)
        card.rec_score(cat, final)
        choices.append(cat)
    upper = card.get_upper()
    bonus = upper >= UPPER_SECTION_BONUS_THRESHOLD
    ytz_score = card.scores[CATEGORY_YAHTZEE]
    
    return {
        "score": card.get_total(),
        "upper": upper,
        "bonus": bonus,
        "ytz": ytz_score,
        "cats": choices,
        "all_scores": dict(card.scores)
    }

def res_analyze(res, strat_name):
    scores = [r["score"] for r in res]
    avg = np.mean(scores)
    std = np.std(scores)
    min_s = np.min(scores)
    max_s = np.max(scores)
    med = np.median(scores)
    bonus_pct = sum(
        1 for r in res if r['bonus']
    )/len(res) * 100
    ytz_pct = sum(
        1 for r in res if r["ytz"] > 0
    )/len(res) * 100
    cats = list()
    for r in res:
        cats.extend(r["cats"])
    
    cat_dist = Counter(cats)
    total = len(cats)
    
    cat_avgs = defaultdict(list)
    for r in res:
        for c, s in r["all_scores"].items():
            if s is not None:
                cat_avgs[c].append(s)
    cat_avg = {c: np.mean(scores) for c, scores in cat_avgs.items()}
    print("\nanalysis for strategy: " + strat_name)
    print("basic statistics:")
    print("\taverage score: %.2f" % avg)
    print("\tmedian score: %.2f" % med)
    print("\tstandard deviation: %.2f" % std)
    print("\tmin score: %d/max score: %d" % (min_s, max_s))
    print("\tupper section bonus rate: %.2f%%" % bonus_pct)
    print("\tyahtzee success rate: %.2f%%" % ytz_pct)
    print("\ncategory usage patterns:")
    for sec, cats in CATEGORIES.items():
        print("\t%s section:" % sec.lower())
        for c in cats:
            use_pct = cat_dist.get(c, 0)/total * 100
            avg_score = cat_avg.get(c, 0)
            print("\t\t%s: %.2f%% usage, avg score: %.2f" % (c, use_pct, avg_score))
    
    return {
        "avg": avg,
        "std": std,
        "med": med,
        "min": min_s,
        "max": max_s,
        "bonus_pct": bonus_pct,
        "ytz_pct": ytz_pct,
        "scores": scores
    }

def plot_dist(stats):
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
    for name, s in stats.items():
        plt.hist(s["scores"], bins=HIST_BINS, alpha=0.5, label=name)
    plt.title("score  distribution by strategy")
    plt.xlabel("score")
    plt.ylabel("frequency")
    plt.legend()
    out = os.path.join(COMPARISON_DIR, SCORE_DIST_FILE)
    plt.savefig(out)
    print("\nscore distribution plot saved as'%s'" % out)

def plot_comp(stats):
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

def run_sim():
    n_sims = DEFAULT_NUM_SIMULATIONS
    print("running yahtzee simulation (%d games per strategy)\n" % n_sims)

    stats = dict()

    for name in STRATEGIES:
        print("simulating %s strategy.." % name)
        res = [game_run(name) for _ in range(n_sims)]
        stats[name] = res_analyze(res, name)

    print("\n\nstrategy comparison summary")
    sorted_stats = sorted(stats.items(),reverse=True, key=lambda x: x[1]["avg"] )

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