from collections import Counter
from logic import (calc_upper, calc_n_of_kind, calc_full_house, 
                        calc_str, calc_yahtzee)
from constant import (
    VALUES, CATEGORIES, SECTION_UPPER, SECTION_LOWER,
    CATEGORY_ACES, CATEGORY_TWOS,
    CATEGORY_THREE_OF_A_KIND, CATEGORY_FOUR_OF_A_KIND, CATEGORY_FULL_HOUSE,
    CATEGORY_SMALL_STRAIGHT, CATEGORY_LARGE_STRAIGHT, CATEGORY_YAHTZEE, CATEGORY_CHANCE,
    UPPER_SECTION_BONUS_THRESHOLD
)

def upper_strat_re(dice, card):
    avail = [
        cat for cat in CATEGORIES[SECTION_UPPER] if not card.is_cat_used(cat)
    ]
    if not avail:
        cnts = Counter(dice)
        mode, _ = cnts.most_common(1)[0]
        return [d for d in dice if d == mode]
    for v in range(6, 0, -1):
        cat = [k for k, val in VALUES.items() if val == v][0]
        if cat in avail:
            return [d for d in dice if d == v]
    return []

def upper_strat_turn(dice, card):
    avail = card.get_avail_cats()
    best_cat = None
    best_sc = -1

    for cat in CATEGORIES[SECTION_UPPER]:
        if cat in avail:
            sc = calc_upper(dice, VALUES[cat])
            if sc > best_sc:
                best_sc = sc
                best_cat = cat
    
    if best_cat is not None:
        return best_cat
    if CATEGORY_YAHTZEE in avail and calc_yahtzee(dice) > 0:
        return CATEGORY_YAHTZEE
    if CATEGORY_CHANCE in avail:
        return CATEGORY_CHANCE
    for cat in CATEGORIES[SECTION_UPPER]:
        if cat in avail:
            return cat
    for cat in CATEGORIES[SECTION_LOWER]:
        if cat in avail:
            return cat
    return avail[0]

def hybrid_strat_re(dice, card):
    cnts = Counter(dice)
    if 5 in cnts.values(): return dice
    if 4 in cnts.values():
        val = [k for k,v in cnts.items() if v==4][0]
        return [d for d in dice if d == val]

    uniq = sorted(list(set(dice)))
    if len(uniq) == 5 and (uniq[4] - uniq[0] == 4):
        return dice
    if len(uniq) >= 4:
        for i in range(len(uniq) - 3):
             if uniq[i+3] - uniq[i] == 3:
                return [d for d in dice if d in uniq[i:i+4]]
    if sorted(cnts.values()) == [2, 3]:
        return dice
    if 3 in cnts.values():
        val = [k for k, v in cnts.items() if v == 3][0]
        return [d for d in dice if d == val]
    if list(cnts.values()).count(2) == 2:
        pairs = [k for k, v in cnts.items() if v == 2]
        return [d for d in dice if d == max(pairs)]
    if 2 in cnts.values():
        val = [k for k, v in cnts.items() if v == 2][0]
        return [d for d in dice if d == val]
        
    return [max(dice)]


def hybrid_strat_turn(dice, card):
    avail = card.get_avail_cats()
    
    scs = {}
    if CATEGORY_YAHTZEE in avail: scs[CATEGORY_YAHTZEE] = calc_yahtzee(dice)
    if CATEGORY_LARGE_STRAIGHT in avail: scs[CATEGORY_LARGE_STRAIGHT] = calc_str(dice, 5)
    if CATEGORY_SMALL_STRAIGHT in avail: scs[CATEGORY_SMALL_STRAIGHT] = calc_str(dice, 4)
    if CATEGORY_FULL_HOUSE in avail: scs[CATEGORY_FULL_HOUSE] = calc_full_house(dice)
    if CATEGORY_FOUR_OF_A_KIND in avail: scs[CATEGORY_FOUR_OF_A_KIND] = calc_n_of_kind(dice, 4)
    if CATEGORY_THREE_OF_A_KIND in avail: scs[CATEGORY_THREE_OF_A_KIND] = calc_n_of_kind(dice, 3)

    best_low = max(
        scs, key=scs.get
    ) if scs and max(scs.values()) > 0 else None
    
    if best_low:return best_low

    up_scs = {}
    for cat in CATEGORIES[SECTION_UPPER]:
        if cat in avail:
            up_scs[cat] = calc_upper(dice, VALUES[cat])
    
    best_up = max(up_scs, key=up_scs.get) if up_scs and max(up_scs.values()) > 0 else None
    
    if best_up:
        return best_up

    if CATEGORY_ACES in avail: return CATEGORY_ACES
    if CATEGORY_TWOS in avail: return CATEGORY_TWOS
    if CATEGORY_CHANCE in avail: return CATEGORY_CHANCE
    
    return avail[0]

def win_or_bust_re(dice, card):
    cnts = Counter(dice)
    most = cnts.most_common(1)
    if most:
        val, cnt = most[0]
        if cnt >= 2:
            return [d for d in dice if d == val]
    return [max(dice)] if dice else []

def win_or_bust_turn(dice, card):
    avail = card.get_avail_cats()
    
    if CATEGORY_YAHTZEE in avail and calc_yahtzee(dice) > 0:
        return CATEGORY_YAHTZEE
    
    if CATEGORY_FOUR_OF_A_KIND in avail and calc_n_of_kind(dice, 4) > 0:
        return CATEGORY_FOUR_OF_A_KIND
    
    if CATEGORY_THREE_OF_A_KIND in avail and calc_n_of_kind(dice, 3) > 0:
        return CATEGORY_THREE_OF_A_KIND
    
    cnts = Counter(dice)
    for v in range(6, 0, -1):
        cat = [k for k, val in VALUES.items() if val == v][0]
        if cat in avail and cnts[v] > 0:
            return cat
    
    if CATEGORY_CHANCE in avail:
        return CATEGORY_CHANCE
    
    return avail[0]

def low_priority_re(dice, card):
    cnts = Counter(dice)
    uniq = sorted(list(set(dice)))
    
    if 5 in cnts.values(): return dice
    
    if 4 in cnts.values():
        val = [k for k,v in cnts.items() if v==4][0]
        return [d for d in dice if d == val]
    
    if len(uniq) == 5 and (uniq[4] - uniq[0] == 4):
        return dice
    
    if len(uniq) >= 4:
        for i in range(len(uniq) - 3):
            if uniq[i+3] - uniq[i] == 3:
                return [d for d in dice if d in uniq[i:i+4]]
    
    if sorted(cnts.values()) == [2, 3]: return dice
    
    if 3 in cnts.values():
        val = [k for k, v in cnts.items() if v == 3][0]
        return [d for d in dice if d == val]
    
    for i in range(len(uniq) - 2):
        if uniq[i+2] - uniq[i] == 2:
            return [d for d in dice if d in uniq[i:i+3]]
    
    if 2 in cnts.values():
        val = [k for k, v in cnts.items() if v == 2][0]
        return [d for d in dice if d == val]
    
    return [max(dice)] if dice else []

def low_priority_turn(dice, card):
    avail = card.get_avail_cats()
    
    pri = [CATEGORY_YAHTZEE, CATEGORY_LARGE_STRAIGHT, CATEGORY_SMALL_STRAIGHT, CATEGORY_FULL_HOUSE, 
                     CATEGORY_FOUR_OF_A_KIND, CATEGORY_THREE_OF_A_KIND]
    
    for cat in pri:
        if cat in avail:
            sc = 0
            if cat == CATEGORY_YAHTZEE: sc = calc_yahtzee(dice)
            elif cat == CATEGORY_LARGE_STRAIGHT: sc = calc_str(dice, 5)
            elif cat == CATEGORY_SMALL_STRAIGHT: sc = calc_str(dice, 4)
            elif cat == CATEGORY_FULL_HOUSE: sc = calc_full_house(dice)
            elif cat == CATEGORY_FOUR_OF_A_KIND: sc = calc_n_of_kind(dice, 4)
            elif cat == CATEGORY_THREE_OF_A_KIND: sc = calc_n_of_kind(dice, 3)
            
            if sc > 0:
                return cat
    
    up_scs = {}
    for cat in CATEGORIES[SECTION_UPPER]:
        if cat in avail:
            up_scs[cat] = calc_upper(dice, VALUES[cat])
    
    if up_scs:
        best = max(up_scs, key=up_scs.get)
        if up_scs[best] > 0:
            return best
    
    if CATEGORY_CHANCE in avail:
        return CATEGORY_CHANCE
    
    return avail[0]

def adapt_strat_re(dice, card):
    filled = sum(1 for sc in card.scores.values() if sc is not None)
    
    if filled < 4:
        return early_re(dice, card)
    elif filled < 9:
        return mid_re(dice, card)
    else:
        return late_re(dice, card)

def early_re(dice, card):
    cnts = Counter(dice)
    uniq = sorted(list(set(dice)))
    
    if 5 in cnts.values() or 4 in cnts.values(): return dice
    
    if len(uniq) == 5 and (uniq[4] - uniq[0] == 4):
        return dice
    
    if sorted(cnts.values()) == [2, 3]: return dice
    
    if len(uniq) >= 4:
        for i in range(len(uniq) - 3):
            if uniq[i+3] - uniq[i] == 3:
                return [d for d in dice if d in uniq[i:i+4]]
    
    if 3 in cnts.values():
        val = [k for k, v in cnts.items() if v == 3][0]
        if val >= 4:
            return [d for d in dice if d == val]
    
    hi_pairs = [k for k, v in cnts.items() if v == 2 and k >= 4]
    if hi_pairs:
        return [d for d in dice if d in hi_pairs]
    
    return [d for d in dice if cnts[d] > 1] or [max(dice)]

def mid_re(dice, card):
    cnts = Counter(dice)
    up_sc = card.get_upper()
    up_filled = sum(1 for cat in CATEGORIES[SECTION_UPPER] if card.scores[cat] is not None)
    up_left = 6 - up_filled
    if up_left > 0 and up_sc < UPPER_SECTION_BONUS_THRESHOLD:
        pts_needed = UPPER_SECTION_BONUS_THRESHOLD - up_sc
        avg_need = pts_needed/up_left
        if avg_need > 10:
            hi = [d for d in dice if d >= 4]
            if hi:
                return hi
    if 5 in cnts.values(): return dice
    if 4 in cnts.values():
        val = [k for k,v in cnts.items() if v==4][0]
        return [d for d in dice if d == val]
    uniq = sorted(list(set(dice)))
    if len(uniq) == 5 and (uniq[4] - uniq[0] == 4):
        return dice
    if len(uniq) >= 4:
        for i in range(len(uniq) - 3):
            if uniq[i+3] - uniq[i] == 3:
                return [d for d in dice if d in uniq[i:i+4]]
    if sorted(cnts.values()) == [2, 3]: return dice
    if 3 in cnts.values():
        val = [k for k, v in cnts.items() if v == 3][0]
        return [d for d in dice if d == val]
    if 2 in cnts.values():
        val = [k for k, v in cnts.items() if v == 2][0]
        return [d for d in dice if d == val]
    
    return [max(dice)]

def late_re(dice, card):
    avail = card.get_avail_cats()
    cnts = Counter(dice)
    
    for cat in avail:
        if cat in CATEGORIES[SECTION_UPPER]:
            val = VALUES[cat]
            if cnts[val] > 0:
                return [d for d in dice if d == val]
        elif cat == CATEGORY_YAHTZEE:
            if 3 in cnts.values() or 4 in cnts.values() or 5 in cnts.values():
                val = cnts.most_common(1)[0][0]
                return [d for d in dice if d == val]
        elif cat == CATEGORY_LARGE_STRAIGHT or cat == CATEGORY_SMALL_STRAIGHT:
            uniq = sorted(list(set(dice)))
            if len(uniq) >= 4:
                return dice
        elif cat == CATEGORY_FULL_HOUSE:
            if 3 in cnts.values() or list(cnts.values()).count(2) == 2:
                return dice
        elif cat == CATEGORY_FOUR_OF_A_KIND or cat == CATEGORY_THREE_OF_A_KIND:
            if 2 in cnts.values() or 3 in cnts.values() or 4 in cnts.values():
                val = cnts.most_common(1)[0][0]
                return [d for d in dice if d == val]
    
    return sorted(dice, reverse=True)[:3]

def adapt_strat_turn(dice, card):
    avail = card.get_avail_cats()
    filled = sum(1 for sc in card.scores.values() if sc is not None)
    
    scs = {}
    
    if CATEGORY_YAHTZEE in avail: scs[CATEGORY_YAHTZEE] = calc_yahtzee(dice)
    if CATEGORY_LARGE_STRAIGHT in avail: scs[CATEGORY_LARGE_STRAIGHT] = calc_str(dice, 5)
    if CATEGORY_SMALL_STRAIGHT in avail: scs[CATEGORY_SMALL_STRAIGHT] = calc_str(dice, 4)
    if CATEGORY_FULL_HOUSE in avail: scs[CATEGORY_FULL_HOUSE] = calc_full_house(dice)
    if CATEGORY_FOUR_OF_A_KIND in avail: scs[CATEGORY_FOUR_OF_A_KIND] = calc_n_of_kind(dice, 4)
    if CATEGORY_THREE_OF_A_KIND in avail: scs[CATEGORY_THREE_OF_A_KIND] = calc_n_of_kind(dice, 3)
    if CATEGORY_CHANCE in avail: scs[CATEGORY_CHANCE] = sum(dice)
    
    for cat in CATEGORIES[SECTION_UPPER]:
        if cat in avail:
            scs[cat] = calc_upper(dice, VALUES[cat])
    
    if filled < 4:
        good = {k: v for k, v in scs.items() if v > 0}
        if good:
            return max(good, key=good.get)
    
    elif filled < 9:
        up_sc = card.get_upper()
        up_filled = sum(1 for cat in CATEGORIES[SECTION_UPPER] if card.scores[cat] is not None)
        up_left = 6 - up_filled
        
        if up_left > 0 and up_sc < UPPER_SECTION_BONUS_THRESHOLD:
            pts_needed = UPPER_SECTION_BONUS_THRESHOLD - up_sc
            avg_need = pts_needed/up_left
            
            up_scs = {k: v for k, v in scs.items() if k in CATEGORIES[SECTION_UPPER] and v > 0}
            if up_scs and max(up_scs.values()) >= avg_need:
                return max(up_scs, key=up_scs.get)
        
        good = {k: v for k, v in scs.items() if v > 0}
        if good:
            return max(good, key=good.get)
    
    else:
        good = {k: v for k, v in scs.items() if v > 0}
        if good:
            return max(good, key=good.get)
    if scs:
        return min(scs, key=scs.get)
    
    return avail[0]

STRATEGIES = {
    "greedy upper section": {
        "reroll": upper_strat_re,
        "score": upper_strat_turn
    },
    "hybrid probability": {
        "reroll": hybrid_strat_re,
        "score": hybrid_strat_turn
    },
    "yahtzee or bust": {
        "reroll": win_or_bust_re,
        "score": win_or_bust_turn
    },
    "lower section priority": {
        "reroll": low_priority_re,
        "score": low_priority_turn
    },
    "adaptive strategy": {
        "reroll": adapt_strat_re,
        "score": adapt_strat_turn
    }
}