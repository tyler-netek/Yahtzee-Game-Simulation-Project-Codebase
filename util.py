import numpy as np
from collections import Counter, defaultdict
from typing import Dict, List, Any, Callable
from logic import Scorecard, roll
from constant import (
    NUM_ROLLS, NUM_TURNS, CATEGORIES,
    UPPER_SECTION_BONUS_THRESHOLD, CATEGORY_YAHTZEE, NUM_DICE,
    LOWER_QUARTILE, UPPER_QUARTILE
)
from strats import STRATEGIES

def turn_init(strat_func: Callable, hand: List[int], card: Scorecard) -> List[int]:
    for __ in range(NUM_ROLLS - 1):
        keep = strat_func(hand, card)
        to_reroll = NUM_DICE - len(keep)
        if to_reroll == 0:
            break
        new = roll(to_reroll)
        hand = keep + new
    return hand

def game_run(strat_name: str) -> Dict[str, Any]:
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

def calc_stats(res: List[Dict[str, Any]]) -> Dict[str, Any]:
    scores = [r["score"] for r in res]
    avg = np.mean(scores)
    std = np.std(scores)
    min_s = np.min(scores)
    max_s = np.max(scores)
    med = np.median(scores)
    q1 = np.percentile(scores, LOWER_QUARTILE)
    q3 = np.percentile(scores, UPPER_QUARTILE)
    cv = (std / avg) * 100 if avg > 0 else 0
    
    bonus_pct = sum(
        1 for r in res if r['bonus']
    )/len(res) * 100
    ytz_pct = sum(
        1 for r in res if r["ytz"] > 0
    )/len(res) * 100
    
    return {
        "avg": avg,
        "std": std,
        "med": med,
        "min": min_s,
        "max": max_s,
        "q1": q1,
        "q3": q3,
        "cv": cv,
        "bonus_pct": bonus_pct,
        "ytz_pct": ytz_pct,
        "scores": scores
    }

def calc_cat_stats(res: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
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
    
    cat_avg = {c: np.mean(cat_scores) for c, cat_scores in cat_avgs.items()}
    cat_pct = {c: cat_dist.get(c, 0)/total*100 for c in cat_avg.keys()}
    
    return {"scores": cat_avg, "usage": cat_pct}

def print_strategy_list():
    print("\navailable strategies:")
    for i, s in enumerate(STRATEGIES.keys()):
        print("%d. %s" % (i+1, s))
    
def get_valid_int(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            else:
                print(f"please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("please enter a valid number")