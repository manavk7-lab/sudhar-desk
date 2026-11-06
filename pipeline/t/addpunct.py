"""addpunct.py VM — after fixitems.py: add the punctuation items (VM/rev_punct.json) to VM/items_all_final.json,
with ids, skipping any whose cur is not found once in VM/final.txt (fold those by hand)."""
import json,re,hashlib,sys
d=sys.argv[1]
def norm(s): return re.sub(r'\s+',' ',s).strip()
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
t=open(f'{d}/final.txt',encoding='utf-8').read()
I=json.load(open(f'{d}/items_all_final.json',encoding='utf-8')); P=json.load(open(f'{d}/rev_punct.json',encoding='utf-8'))
have={i['id'] for i in I}; n=0
for it in P:
    it=dict(it); it.setdefault('id',hid(norm(it['cur']),norm(it['alt']))); it.setdefault('kind','applied'); it.setdefault('conf','likely')
    if it['id'] in have: continue
    if len(re.findall(flex(it['cur']),t))!=1: print('skip (not once):',it['cur'][:60]); continue
    I.append(it); n+=1
json.dump(I,open(f'{d}/items_all_final.json','w',encoding='utf-8'),ensure_ascii=False,indent=0); print('punct items added',n,'total',len(I))
