"""Transparent baseline word-list sentiment scorer with local negation."""
import re
POSITIVE = {"good", "clean", "fast", "helpful", "improved", "excellent", "safe", "fixed"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken", "unsafe", "worse"}
NEGATORS = {"not", "never", "no"}
def score(text):
    words=re.findall(r"[a-z]+",text.lower()); total=0
    for i,word in enumerate(words):
        value=1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if value and i and words[i-1] in NEGATORS: value=-value
        total+=value
    return total
def label(text):
    value=score(text)
    return "positive" if value>0 else "negative" if value<0 else "neutral"
def improved_label(text):
    """Improvement over baseline: honor wider negation and complaint phrases."""
    words=re.findall(r"[a-z]+",text.lower()); total=0
    for i,word in enumerate(words):
        value=1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if value and any(w in NEGATORS for w in words[max(0,i-2):i]): value=-value
        total+=value
    low=text.lower()
    if re.search(r"\bno\s+(staff|response|inspection|service)\b",low): total-=1
    return "positive" if total>0 else "negative" if total<0 else "neutral"
