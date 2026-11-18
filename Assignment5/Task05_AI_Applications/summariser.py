"""Extractive summary ranked by normalized frequency of non-stopwords."""
import re
STOP={"the","a","an","and","or","but","is","are","was","were","to","from","of","in","on","at","it","this","that","with","for","we","i","they","there","has","have","not"}
def summarize(text, max_sentences=2):
    sentences=[s.strip() for s in re.split(r"(?<=[.!?])\s+",text.strip()) if s.strip()]
    if len(sentences)<=max_sentences: return " ".join(sentences)
    tokens=[re.findall(r"[a-z]+",s.lower()) for s in sentences]
    freq={}
    for ts in tokens:
        for t in set(ts)-STOP: freq[t]=freq.get(t,0)+1
    ranked=[]
    for i,ts in enumerate(tokens):
        terms=[t for t in ts if t not in STOP]
        value=sum(freq.get(t,0) for t in terms)/max(1,len(terms))
        ranked.append((value,i))
    picks=sorted(i for _,i in sorted(ranked,reverse=True)[:max_sentences])
    return " ".join(sentences[i] for i in picks)
