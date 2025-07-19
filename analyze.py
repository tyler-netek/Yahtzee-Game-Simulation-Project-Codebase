import numpy as np
import matplotlib.pyplot as plt
from sim import game_run
from strats import STRATEGIES
from collections import defaultdict
import os
from constant import (
    DEFAULT_HEAD_TO_HEAD_GAMES, DEFAULT_VISUALIZATION_GAMES, DEFAULT_TOURNAMENT_GAMES,
    FIGURE_WIDTH, FIGURE_HEIGHT, TOURNAMENT_DIR, TOURNAMENT_RESULTS_FILE,
    LOWER_QUARTILE, UPPER_QUARTILE
)

def head_to_head(s1, s2, n_games=DEFAULT_HEAD_TO_HEAD_GAMES):
    print("running head-to-head: %s vs %s" % (s1, s2))
    wins = {
        s1: 0,
        s2: 0, "tie": 0
    }
    diffs = list()
    for __ in range(n_games):
        sc1 = game_run(s1)['score']
        sc2 = game_run(s2)['score']
        if sc1 > sc2:
            wins[s1] += 1
        elif sc2 > sc1:
            wins[s2] += 1
        else:
            wins['tie'] += 1
        diffs.append(sc1 - sc2)
    
    print("\nresults after %d games:" % n_games)
    print("%s wins:%d (%.2f%%)" % (s1, wins[s1], wins[s1]/n_games*100))
    print("%s wins: %d (%.2f%%)" % (s2, wins[s2], wins[s2]/n_games*100))
    print("ties: %d(%.2f%%)" % (wins['tie'], wins['tie']/n_games*100))
    print("average score difference: %.2f" % np.mean(diffs))
    
    return wins, diffs

def analyze_consist(strat, n_games=DEFAULT_VISUALIZATION_GAMES):
    print("analyzing consistency for %s.." % strat)
    scs = []
    cat_use = defaultdict(int)
    for __ in range(n_games):
        res = game_run(strat)
        scs.append(res["score"])
        for cat in res["cats"]:
            cat_use[cat] += 1
    q1 = np.percentile(scs, LOWER_QUARTILE)
    q3 = np.percentile(scs, UPPER_QUARTILE)
    iqr = q3 - q1
    tot = sum(cat_use.values())
    cat_pcts = {cat: cnt/tot*100 for cat, cnt in cat_use.items()}
    print("\nconsistency analysis for %s:" % strat)
    print("interquartile range (iqr): %.2f" % iqr)
    print("25th percentile: %.2f" % q1)
    print("75th percentile: %.2f" % q3)
    print("coefficient of variation: %.2f%%" % (np.std(scs)/np.mean(scs)*100))
    print("\ncategory usage patterns:")
    for cat, pct in sorted(cat_pcts.items(), key=lambda x: x[1], reverse=True):
        print("\t%s: %.2f%%" % (cat, pct))
    return {
        "iqr": iqr,
        "q1": q1,
        "q3": q3,
        "cv": np.std(scs)/np.mean(scs)*100,
        "cat_use": cat_pcts
    }

def tournament_start(n_games=DEFAULT_TOURNAMENT_GAMES):
    strats = list(STRATEGIES.keys())
    n = len(strats)
    res = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            s1 = strats[i]
            s2 = strats[j]
            wins,_ = head_to_head(s1,s2,n_games)
            res[i,j] = wins[s1]/n_games * 100
            res[j,i] = wins[s2]/n_games * 100
    win_pcts = np.sum(res,axis=1)/(n-1)
    print("\ntournament results:")
    idxs = np.argsort(win_pcts)[::-1]
    for i,idx in enumerate(idxs):
        s = strats[idx]
        print("%d. %s: %.2f%% average win rate" % (i+1,s,win_pcts[idx]))
    
    plt.figure(figsize=(FIGURE_WIDTH,FIGURE_HEIGHT))
    plt.imshow(res,cmap='YlGnBu')
    plt.colorbar(label='win %')
    plt.xticks(range(n),strats,rotation=45,ha='right')
    plt.yticks(range(n), strats)
    plt.title('strategy tournament results (win %)')
    for i in range(n):
        for j in range(n):
            if i != j:
                plt.text(j, i, "%.1f%%" % res[i,j],ha='center', va='center', 
                         color='black' if res[i, j] < 50 else 'white')
            else:
                plt.text(j, i,"X", ha='center', va='center')
    
    plt.tight_layout()
    out = os.path.join(TOURNAMENT_DIR, TOURNAMENT_RESULTS_FILE)
    plt.savefig(out)
    print("\ntournament results heatmap saved as '%s'" % out)
    
    return res,win_pcts

print("yahtzee strategy analysis tool")
print("\n1.) run head-to-head comparison")
print("2.) analyze strategy consistency")
print("3.) run full tournament")
print("4.) exit")

choice = input("\nenter your choice (1-4): ")

if choice == "1":
    print("\navailable strategies:")
    for i,s in enumerate(STRATEGIES.keys()):
        print("%d. %s" % (i+1,s))
    idx1 = int(input("\nselect first strategy (number): ")) - 1
    idx2 = int(input("select second strategy (number): ")) - 1
    strats = list(STRATEGIES.keys())
    head_to_head(strats[idx1],strats[idx2], DEFAULT_HEAD_TO_HEAD_GAMES)
    
elif choice == "2":
    print("\navailable strategies:")
    for i, s in enumerate(STRATEGIES.keys()):
        print("%d. %s" % (i+1, s))
    idx = int(input("\nselect strategy to analyze (number): ")) - 1
    strats = list(STRATEGIES.keys())
    analyze_consist(strats[idx], DEFAULT_VISUALIZATION_GAMES)
elif choice == "3":
    tournament_start(DEFAULT_TOURNAMENT_GAMES)
else:
    print("exiting..")