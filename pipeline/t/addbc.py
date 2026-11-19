"""addbc.py vN — fold vN/bc_checks.json into vN/items_all_final.json (a check that overlaps an item goes into that item's why)."""
import json,re,sys
V=sys.argv[1]
t=open(f'{V}/final.txt').read()
d=json.load(open(f'{V}/items_all_final.json')); c=json.load(open(f'{V}/bc_checks.json'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def span(x):
    m=list(re.finditer(flex(x['cur']),t)); return m[0].span() if len(m)==1 else None
sp=[(span(x),x) for x in d]
for k in c:
    s=span(k)
    if not s: print('not found',k['cur'][:40]); continue
    hit=[x for (q,x) in sp if q and q[0]<s[1] and q[1]>s[0]]
    if hit: hit[0]['why']=hit[0].get('why','')+'; '+k['why']; print('folded',hit[0]['id'])
    else: d.append(k); print('added',k['cur'][:30])
json.dump(d,open(f'{V}/items_all_final.json','w'),ensure_ascii=False,indent=1)
