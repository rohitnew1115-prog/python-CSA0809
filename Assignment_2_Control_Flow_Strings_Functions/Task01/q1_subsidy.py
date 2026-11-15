"""Q1: Electricity subsidy decisions and comparison of control-flow designs."""
from math import inf

def decisions_separate(units, ration_card, senior_over_80):
    decisions = []
    if units <= 100: decisions.append("Full subsidy")
    if 101 <= units <= 200 and ration_card: decisions.append("Partial subsidy")
    if units > 200 and senior_over_80: decisions.append("Senior exception: subsidy")
    if not decisions: decisions.append("No subsidy")
    return decisions

def decision_chain(units, ration_card, senior_over_80):
    if units <= 100: return "Full subsidy"
    elif units <= 200: return "Partial subsidy" if ration_card else "No subsidy"
    else: return "Senior exception: subsidy" if senior_over_80 else "No subsidy"

def decision_match(units, ration_card, senior_over_80):
    match units:
        case n if n <= 100: return "Full subsidy"
        case n if n <= 200: return "Partial subsidy" if ration_card else "No subsidy"
        case _: return "Senior exception: subsidy" if senior_over_80 else "No subsidy"

def decision_lookup(units, ration_card, senior_over_80):
    for upper, slab in ((100, "full"), (200, "middle"), (inf, "above")):
        if units <= upper:
            if slab == "full": return "Full subsidy"
            if slab == "middle": return "Partial subsidy" if ration_card else "No subsidy"
            return "Senior exception: subsidy" if senior_over_80 else "No subsidy"

CASES = [(80,False,False),(100,True,False),(101,False,False),(150,True,False),
         (200,False,False),(200,True,False),(201,True,False),(250,False,True)]

def main():
    print("Q1 | Predicted outcomes tested against four implementations")
    for case in CASES:
        expected = decision_chain(*case)
        assert decisions_separate(*case) == ([expected] if expected != "No subsidy" else ["No subsidy"])
        assert decision_match(*case) == decision_lookup(*case) == expected
        print(f"units={case[0]:3} ration={str(case[1]):5} senior>80={str(case[2]):5} -> {expected}")
    # Independent if statements can emit multiple actions when ranges overlap.
    overlap = []
    if 100 <= 150: overlap.append("broad first slab")
    if 101 <= 150 <= 200: overlap.append("middle slab")
    print("Overlapping independent conditions demonstrate multiple decisions:", overlap)
    print("Complexity: chain/match O(1) time O(1) space; lookup O(k) time, O(k) table space.")
    print("Conclusion: mutually exclusive if/elif with nested exception checks is clearest.")

if __name__ == '__main__': main()
