import numpy as np
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Any
from constant import (
    DEFAULT_HEAD_TO_HEAD_GAMES, DEFAULT_VISUALIZATION_GAMES, DEFAULT_TOURNAMENT_GAMES,
    FIGURE_WIDTH, FIGURE_HEIGHT, TOURNAMENT_DIR, TOURNAMENT_RESULTS_FILE
)
from strats import STRATEGIES
from util import game_run, calc_stats, calc_cat_stats, print_strategy_list, get_valid_int

def head_to_head(s1: str, s2: str, n_games: int = DEFAULT_HEAD_TO_HEAD_GAMES) -> Tuple[Dict[str, int], List[int]]:
    print("running head-to-head: %s vs %s" % (s1, s2))
    wins: Dict[str, int] = {
        s1: 0,
        s2: 0, "tie": 0
    }
    diffs: List[int] = list()
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

def analyze_consist(strat: str, n_games: int = DEFAULT_VISUALIZATION_GAMES) -> Dict[str, Any]:
    print("analyzing consistency for %s.." % strat)
    res = [game_run(strat) for _ in range(n_games)]
    stats = calc_stats(res)
    cat_stats = calc_cat_stats(res)
    cat_turns = defaultdict(list)
    for r in res:
        for turn, cat in enumerate(r["cats"]):
            cat_turns[cat].append(turn + 1)
    
    print("\nconsistency analysis for %s:" % strat)
    print("interquartile range (iqr): %.2f" % (stats["q3"] - stats["q1"]))
    print("25th percentile: %.2f" % stats["q1"])
    print("75th percentile: %.2f" % stats["q3"])
    print("coefficient of variation: %.2f%%" % stats["cv"])
    
    print("\ncategory usage patterns:")
    for cat in sorted(cat_stats["scores"].keys()):
        avg_score = cat_stats["scores"][cat]
        avg_turn = np.mean(cat_turns[cat])
        print("\t%s: avg score %.2f, avg turn %.1f" % (cat, avg_score, avg_turn))
    
    print("\ncategory turn distribution (when each category is typically used):")
    early_cats = list()
    mid_cats = list()
    late_cats = list()
    
    for cat, turns in cat_turns.items():
        avg_turn = np.mean(turns)
        if avg_turn <= 4:
            early_cats.append((cat, avg_turn))
        elif avg_turn <= 9:
            mid_cats.append((cat, avg_turn))
        else:
            late_cats.append((cat, avg_turn))
    
    print("\tearly game (turns 1-4):")
    for cat, avg in sorted(early_cats, key=lambda x: x[1]):
        print("\t\t%s: turn %.1f" % (cat, avg))
        
    print("\tmid game (turns 5-9):")
    for cat, avg in sorted(mid_cats, key=lambda x: x[1]):
        print("\t\t%s: turn %.1f" % (cat, avg))
        
    print("\tlate game (turns 10-13):")
    for cat, avg in sorted(late_cats, key=lambda x: x[1]):
        print("\t\t%s: turn %.1f" % (cat, avg))
    
    return stats

def tournament_start(n_games: int = DEFAULT_TOURNAMENT_GAMES) -> Tuple[np.ndarray, np.ndarray]:
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

try:
    while True:
        choice = input("\nenter your choice (1-4): ")
        if choice not in ["1", "2", "3", "4"]:
            print("please enter a number between 1 and 4")
            continue
        if choice == "1":
            print_strategy_list()
            strats = list(STRATEGIES.keys())
            idx1 = get_valid_int("\nselect first strategy (number): ", 1, len(strats)) - 1
            idx2 = get_valid_int("select second strategy (number): ", 1, len(strats)) - 1
            if idx1 == idx2:
                print("please select two different strategies")
                continue
            head_to_head(strats[idx1], strats[idx2], DEFAULT_HEAD_TO_HEAD_GAMES)
            break
        elif choice == "2":
            print_strategy_list()
            strats = list(STRATEGIES.keys())
            
            idx = get_valid_int("\nselect strategy to analyze (number): ", 1, len(strats)) - 1
            analyze_consist(strats[idx], DEFAULT_VISUALIZATION_GAMES)
            break
            
        elif choice == "3":
            tournament_start(DEFAULT_TOURNAMENT_GAMES)
            break
            
        elif choice == "4":
            print("exiting..")
            break
            
except KeyboardInterrupt:
    print("\nexiting..")