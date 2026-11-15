"""Contact merging keyed by normalized Indian phone number."""
import re, timeit
def normalize_phone(value):
    if not value: return None
    digits=''.join(ch for ch in str(value) if ch.isdigit())
    if digits.startswith('0091'): digits=digits[4:]
    elif digits.startswith('91') and len(digits)==12: digits=digits[2:]
    if len(digits)!=10 or digits[0] not in '6789': return None
    return '+91'+digits
def normalize_name(value): return ' '.join(re.findall(r'[a-z]+',str(value or '').casefold()))
def merge_contacts(*lists):
    parent={}; details={}
    def find(phone):
        parent.setdefault(phone,phone)
        if parent[phone]!=phone: parent[phone]=find(parent[phone])
        return parent[phone]
    def union(left,right):
        a,b=find(left),find(right)
        if a!=b: parent[b]=a
    for contacts in lists:
        for c in contacts:
            phones={p for raw in c.get('phones',[]) if (p:=normalize_phone(raw))}
            emails={str(e).strip().casefold() for e in c.get('emails',[]) if e and str(e).strip()}
            if not phones: continue
            phones=sorted(phones)
            for p in phones: find(p)
            for p in phones[1:]: union(phones[0],p)
            for p in phones:
                record=details.setdefault(p,{'phones':set(),'emails':set(),'names':set()})
                record['phones'].add(p); record['emails'].update(emails)
                if c.get('name'): record['names'].add(str(c['name']).strip())
    groups={}
    for phone,info in details.items():
        root=find(phone); group=groups.setdefault(root,{'phones':set(),'emails':set(),'names':set()})
        group['phones'].update(info['phones']); group['emails'].update(info['emails']); group['names'].update(info['names'])
    result=[]
    for v in groups.values():
        names=sorted(v['names'],key=str.casefold)
        result.append({'name':names[0] if names else '', 'phones':sorted(v['phones']), 'emails':sorted(v['emails']), 'also_known_as':names})
    return sorted(result,key=lambda x:x['name'].casefold())
def main():
    a=[{'name':'Dr. Ravi','phones':['+91 98400 12345','+91 90000 11111'],'emails':['RAVI@example.com']},{'name':'Same Name','phones':['9876543210']}]
    b=[{'name':'ravi kumar','phones':['9840012345'],'emails':['ravi@example.com','rk@example.com']},{'name':'Same Name','phones':['+91-98765-43211']},{'name':'Missing fields','phones':['9876543212']},{'name':'Bad','phones':['123']}]
    print('merged:',merge_contacts(a,b)); print('empty:',merge_contacts([],[])); print('manual match:',normalize_phone('+91 98400 12345')==normalize_phone('9840012345'))
    for n in (1000,10000):
        data=[{'name':f'Person {i}','phones':[f'9{i%1000000000:09d}']} for i in range(n)]
        print(f'{n} contacts average seconds:',timeit.timeit(lambda:merge_contacts(data),number=3)/3)
    print('design: contacts connect through canonical valid phones, including all numbers in one record; similar names alone never merge. Missing/invalid phone records are skipped. Limitation: shared/family phone numbers can combine distinct people; manual review or stronger identifiers is needed.')
    print('pairwise comparison O(n^2); dictionary-backed disjoint sets group phone identities in near-linear O(p alpha(p)) time and O(p) space, for p unique phones. Name normalization is for display/search only, never identity.')
if __name__=='__main__': main()
