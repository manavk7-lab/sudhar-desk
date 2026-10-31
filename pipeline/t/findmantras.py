"""findmantras.py doc.txt verses.json [verses2.json ...] > report — where the book's Sanskrit pādas are recited in the Doc."""
import sys,re,json
from rapidfuzz import fuzz
doc=open(sys.argv[1],encoding='utf-8').read()
V=[]
for f in sys.argv[2:]:
    for v in json.load(open(f,encoding='utf-8')): v['src']=f.split('/')[-1].split('_')[0]; V.append(v)
MAP={'ી':'િ','ૂ':'ુ','ઈ':'ઇ','ઊ':'ઉ','ષ':'સ','શ':'સ','ણ':'ન','ળ':'લ','ૃ':'ર','ઋ':'ર','ં':'મ','ઁ':'મ','ૅ':'ે','ૉ':'ો'}
DROP=set('્ઃ઼ઽ')
def norm(s):
    out=[];idx=[]
    for i,c in enumerate(s):
        if c in DROP: continue
        if not ('઀'<=c<='૿') or c in '૦૧૨૩૪૫૬૭૮૯': continue
        out.append(MAP.get(c,c)); idx.append(i)
    return ''.join(out),idx
DN,DI=norm(doc)
used=[]
res=[]
for v in V:
    segs=[s.strip() for s in re.split(r'[।॥\n]|[૦-૯]+',v['gu']) if s.strip()]
    for s in segs:
        sn,_=norm(s)
        if len(sn)<10: continue
        r=fuzz.partial_ratio_alignment(sn,DN,score_cutoff=62)
        if not r: res.append((v['src'],v['n'],s,0,None,None)); continue
        a=DI[r.dest_start]; b=DI[max(r.dest_start,r.dest_end-1)]+1
        # expand to word boundaries
        while a>0 and not doc[a-1].isspace(): a-=1
        while b<len(doc) and not doc[b].isspace(): b+=1
        res.append((v['src'],v['n'],s,round(r.score),a,b))
for src,n,s,sc,a,b in res:
    if a is None: print(f'{src} v{n} -- | {s}'); continue
    print(f'{src} v{n} {sc} @{a} | {s}\n      DOC: {doc[a:b]}')
