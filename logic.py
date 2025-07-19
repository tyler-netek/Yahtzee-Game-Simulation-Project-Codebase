import random
from collections import Counter
from constant import (
    CATEGORIES, VALUES, NUM_SIDES,
    UPPER_SECTION_BONUS_THRESHOLD, UPPER_SECTION_BONUS_SCORE,
    FULL_HOUSE_SCORE, SMALL_STRAIGHT_SCORE, LARGE_STRAIGHT_SCORE, YAHTZEE_SCORE,
    SECTION_UPPER, SECTION_LOWER, CATEGORY_THREE_OF_A_KIND, CATEGORY_FOUR_OF_A_KIND,
    CATEGORY_FULL_HOUSE, CATEGORY_SMALL_STRAIGHT, CATEGORY_LARGE_STRAIGHT,
    CATEGORY_YAHTZEE, CATEGORY_CHANCE
)

def roll(n):
    return [
        random.randint(1, NUM_SIDES) for _ in range(n)
    ]

def calc_upper(dice, val):
    return dice.count(val) * val

def calc_n_of_kind(dice, n):
    cnts = Counter(dice)
    if any(
        cnt >= n for cnt in cnts.values()
    ):
        return sum(dice)
    return 0

def calc_full_house(dice):
    cnts = Counter(dice)
    return FULL_HOUSE_SCORE if sorted(cnts.values()) == [2, 3] else 0

def calc_str(dice, length):
    uniq = sorted(list(set(dice)))
    if len(uniq) < length:
        return 0
    
    for i in range(len(uniq) - length + 1):
        is_str = True
        for j in range(length - 1):
            if uniq[i+j] + 1 != uniq[i+j+1]:
                is_str = False
                break
        if is_str:
            return SMALL_STRAIGHT_SCORE if length == 4 else LARGE_STRAIGHT_SCORE
            
    return 0


def calc_yahtzee(dice):
    return YAHTZEE_SCORE if len(set(dice)) == 1 else 0

class Scorecard:    
    def __init__(self):
        self.scores = {
            cat: None for sec in CATEGORIES.values() for cat in sec
        }

    def is_cat_used(self, cat):
        return self.scores[cat] is not None

    def rec_score(self, cat, dice):
        if self.is_cat_used(cat):
            print("warning: category %s already used." % cat)
            return False

        score = {
            **{k: lambda d, v=v: calc_upper(d, v) for k, v in VALUES.items()},
            CATEGORY_THREE_OF_A_KIND: lambda d: calc_n_of_kind(d, 3),
            CATEGORY_FOUR_OF_A_KIND: lambda d: calc_n_of_kind(d, 4),
            CATEGORY_FULL_HOUSE: calc_full_house,
            CATEGORY_SMALL_STRAIGHT: lambda d: calc_str(d, 4),
            CATEGORY_LARGE_STRAIGHT: lambda d: calc_str(d, 5),
            CATEGORY_YAHTZEE: calc_yahtzee,
            CATEGORY_CHANCE: sum
        }.get(cat, lambda d: 0)(dice)

        self.scores[cat] = score
        return True

    def get_upper(self):
        return sum(
            self.scores[cat] for cat in CATEGORIES[SECTION_UPPER] if self.scores[cat] is not None
        )

    def get_total(self):
        upper = self.get_upper()
        bonus = UPPER_SECTION_BONUS_SCORE if upper >= UPPER_SECTION_BONUS_THRESHOLD else 0
        lower = sum(
            self.scores[cat] for cat in CATEGORIES[SECTION_LOWER] if self.scores[cat] is not None
        )
        return upper + bonus + lower

    def get_avail_cats(self):
        return [
            cat for cat, score in self.scores.items() 
            if score is None
        ]