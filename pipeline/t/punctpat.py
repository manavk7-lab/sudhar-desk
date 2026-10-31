import os
import re,json,difflib,collections,sys
sys.path.insert(0,'t')
from fuse import TOKR
S=os.environ.get('SD_WORK','.')+''
new2=open(S+'/v9/new2.txt',encoding='utf-8').read(); now9=open(S+'/v9/now9.txt',encoding='utf-8').read()
P=json.load(open(S+'/v9/pauses_new2.json')); W=json.load(open(S+'/v9/pauses_new2.json.words'))
pause_at={W[r['i']][1]:r['pause'] for r in P}
def toks(txt,lim): return [(m.start(),m.end(),m.group()) for m in TOKR.finditer(txt[:lim])]
def lab(txt,a,b):
    sep=txt[a:b]; return '.' if re.search(r'[.!]',sep) else ('?' if '?' in sep else (',' if ',' in sep else ''))
A=toks(new2,46246); B=toks(now9,46222)
# boundary list in new2 with my label, his label (None if not aligned), pause
bl=[]
m={}
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,[t[2] for t in A],[t[2] for t in B],autojunk=False).get_opcodes():
    if op=='equal':
        for k in range(i2-i1): m[i1+k]=j1+k
for i in range(len(A)-1):
    la=lab(new2,A[i][1],A[i+1][0]); j=m.get(i); j2=m.get(i+1)
    lb=lab(now9,B[j][1],B[j2][0]) if j is not None and j2==j+1 else None
    bl.append((la,lb,pause_at.get(A[i][1]),A[i][2]))
# pattern: dot with no pause, and within +-3 boundaries a no-punct boundary with pause>=0.5 (no other punctuation in between)
cands=[]
for i,(la,lb,p,w) in enumerate(bl):
    if la!='.' or p is None or p>=0.15: continue
    best=None
    for d in (1,2,3,-1,-2,-3):
        k=i+d
        if not (0<=k<len(bl)): continue
        rng=range(min(i,k)+ (1 if d>0 else 0), max(i,k)+(0 if d>0 else 0))
        if any(bl[x][0] for x in range(min(i,k)+1,max(i,k))): break
        if bl[k][0]=='' and bl[k][2] is not None and bl[k][2]>=0.5:
            if best is None or bl[k][2]>best[1]: best=(k,bl[k][2])
    if best: cands.append((i,best[0],best[1]))
moved=0; partial=0
for i,k,p in cands:
    his_i=bl[i][1]; his_k=bl[k][1]
    if his_i in ('',',') and his_k in ('.','?'): moved+=1
    elif his_i!='.' or his_k not in ('',None): partial+=1
print('move-candidates',len(cands),'he moved exactly so',moved,'he changed something there',partial)
for i,k,p in cands[:40]:
    ctx=' '.join(x[3]+(x[0] if x[0] else '') for x in bl[max(0,min(i,k)-3):max(i,k)+3])
    print(f'  {"MOVED" if bl[i][1] in ("",",") and bl[k][1] in (".","?") else "kept "}  pause {p:.2f} | {ctx}')
