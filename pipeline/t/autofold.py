"""autofold.py VM text.txt items.json groups_out.json — suggest fold groups for t/foldfix.py.
1. Items whose spans in text.txt overlap (what overlapcheck.py calls BAD) are grouped.
2. Items collect_items.py could not find (LOST: an id in a stage file but not in items.json) are grouped with the
   later-stage item that changed text inside them (its alt shares >= 6 characters with the LOST item's cur at an edge).
Members are ordered by stage (backbone, rev_new, rev_manual, rev_mantra, rev_agale, rev_punct). Prints the groups."""
import json,sys,os,difflib
VM,T,I,OUT=sys.argv[1:5]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8'))
STAGES=['backbone_items','rev_new','rev_manual','rev_mantra','rev_agale','rev_punct']
stage={}; src={}
for k,f in enumerate(STAGES):
    p=os.path.join(VM,f+'.json')
    if not os.path.exists(p): continue
    for x in json.load(open(p,encoding='utf-8')):
        if 'id' in x: stage.setdefault(x['id'],k); src.setdefault(x['id'],x)
have={x['id'] for x in it}
# items made from stage rows without an id (rev_manual / rev_agale rows) exist only in items.json: later than the judges
for x in it:
    if x['id'] not in src: src[x['id']]=x; stage[x['id']]=3.5
par={}
def find(a):
    while par.setdefault(a,a)!=a: par[a]=par[par[a]]; a=par[a]
    return a
def union(a,b): par[find(a)]=find(b)
# 1. overlaps
sp=[]
for x in it:
    p=t.find(x['cur'])
    if p>=0 and t.count(x['cur'])==1 and x.get('kind')!='check': sp.append((p,p+len(x['cur']),x['id']))
sp.sort()
for i in range(len(sp)):
    for j in range(i+1,len(sp)):
        if sp[j][0]>=sp[i][1]: break
        union(sp[i][2],sp[j][2])
# 2. LOST
for lid,x in src.items():
    if lid in have: continue
    k=stage[lid]; best=None
    for yid,y in src.items():
        if stage[yid]<=k or yid==lid: continue
        a,b=x['cur'],y['alt']
        m=difflib.SequenceMatcher(None,a,b,autojunk=False).find_longest_match(0,len(a),0,len(b))
        edge=(m.a==0 or m.a+m.size==len(a) or m.b==0 or m.b+m.size==len(b))
        if m.size>=6 and edge and (best is None or m.size>best[0]): best=(m.size,yid)
    if best: union(lid,best[1])
    else: print('LOST without partner:',lid,repr(x['cur'][:60]))
groups={}
for a in list(par): groups.setdefault(find(a),[]).append(a)
out=[sorted(g,key=lambda i:(stage.get(i,9),i)) for g in groups.values() if len(g)>1]
json.dump(out,open(OUT,'w'),ensure_ascii=False)
for g in out: print(g,[repr((src.get(i) or next((x for x in it if x['id']==i),{})).get('cur','')[:30]) for i in g])
