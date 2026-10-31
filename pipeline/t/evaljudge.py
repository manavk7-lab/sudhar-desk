"""evaljudge.py doc.txt final.txt kept.json judgeout.json [ids-file-of-judged-lines]"""
import sys,json,collections,re
sys.path.insert(0,'t')
from fuse import TOKR,key
from fuse2 import bmap
doc=open(sys.argv[1],encoding='utf-8-sig').read(); fin=open(sys.argv[2],encoding='utf-8-sig').read()
K={it['id']:it for it in json.load(open(sys.argv[3],encoding='utf-8'))}
J={x['id']:x for x in json.load(open(sys.argv[4],encoding='utf-8'))}
ids=[l.split()[0] for l in open(sys.argv[5],encoding='utf-8')] if len(sys.argv)>5 else list(K)
D=TOKR.findall(doc); F=TOKR.findall(fin); m,_=bmap(D,F)
def kk(s): return ' '.join(key(x) for x in TOKR.findall(s))
st=collections.Counter(); ex=collections.defaultdict(list)
for i in ids:
    it=K[i]; a,b=it['a'],it['b']
    while a not in m: a-=1
    while b not in m: b+=1
    man=' '.join(F[m[a]:m[b]]); old=' '.join(D[a:b])
    # judge version of the same widened span
    j=J.get(i)
    if j:
        pre=' '.join(D[a:it['a']]); post=' '.join(D[it['b']:b])
        jv=' '.join(x for x in [pre,j['text'],post] if x)
        if kk(man)==kk(old): r='WRONG(he kept doc)'
        elif kk(man)==kk(jv): r='same as Manav'
        else: r='he wrote other'
        st[(j['d'],r)]+=1; ex[(j['d'],r)].append(f"{i} [{old}]→[{j['text']}] Manav:[{man}] | S:{it['read'].get('S')} G:{it['read'].get('G')}")
    else:
        r='missed' if kk(man)!=kk(old) else 'ok'
        st[('keep',r)]+=1; ex[('keep',r)].append(f"{i} [{old}] Manav:[{man}] | S:{it['read'].get('S')} G:{it['read'].get('G')}")
for k in sorted(st): print(k,st[k])
if '-v' in sys.argv[0:1] or True:
    for k in [('fix','WRONG(he kept doc)'),('maybe','WRONG(he kept doc)'),('keep','missed'),('fix','he wrote other')]:
        print('\n==',k)
        for e in ex[k][:25]: print(' ',e)
