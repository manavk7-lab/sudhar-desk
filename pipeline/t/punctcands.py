"""punctcands.py text.txt pauses.json out_prefix [from_char] [to_char]
Builds regions around candidate word boundaries for the punctuation judge:
  A: a full stop / question mark where the speaker does not pause (<0.15 s)
  B: no punctuation (or a comma) where the speaker pauses >= 0.7 s
Writes out_prefix.json (boundaries) and out_prefix.txt (regions for the judge)."""
import os
import re,json,sys
sys.path.insert(0,os.environ.get('SD_WORK','.')+'/t')
from fuse import TOKR
txt=open(sys.argv[1],encoding='utf-8').read(); P=json.load(open(sys.argv[2])); W=json.load(open(sys.argv[2]+'.words')); pre=sys.argv[3]
lo=int(sys.argv[4]) if len(sys.argv)>4 else 0; hi=int(sys.argv[5]) if len(sys.argv)>5 else len(txt)
pause={r['i']:r['pause'] for r in P}; conf={r['i']:r['conf'] for r in P}
N=len(W)
def sep(i): return txt[W[i][1]:W[i+1][0]]
def lab(i):
    s=sep(i); return '.' if re.search(r'[.!]',s) else ('?' if '?' in s else (',' if ',' in s else ''))
cand=[]
for i in range(N-1):
    if W[i][1]<lo or W[i][1]>hi: continue
    if '\n' in sep(i) or i not in pause: continue
    p=pause[i]; l=lab(i)
    if l in ('.','?') and p<0.15: cand.append(i)
    elif l in ('',',') and p>=0.7: cand.append(i)
# regions
regions=[];cur=[]
for i in cand:
    if cur and i-cur[-1]>8: regions.append(cur); cur=[]
    cur.append(i)
if cur: regions.append(cur)
B={};lines=[]
def ts(t):
    s=t//1000; return f'[{s//3600}:{s%3600//60:02d}:{s%60:02d}]' if s>=3600 else f'[{s//60}:{s%60:02d}]'
for rn,reg in enumerate(regions,1):
    a=max(0,reg[0]-12); b=min(N-1,reg[-1]+12)
    parts=[];k=0;ids={}
    for i in range(a,b+1):
        w=txt[W[i][0]:W[i][1]]
        s=sep(i) if i<N-1 else ''
        punct=''.join(ch for ch in s if ch in '.,?!')
        mark=''
        if i in reg:
            k+=1; bid=f'r{rn}.{k}'; ids[i]=bid; mark=f'[{k}]'
            B[bid]={'i':i,'pos':W[i][1],'end':W[i+1][0],'cur':lab(i),'pause':pause.get(i),'t':W[i][2]}
        pz=pause.get(i,0) or 0
        pm=f'⟨{pz:.1f}⟩' if pz>=0.3 else ''
        parts.append(w+punct+mark+pm)
    lines.append(f"r{rn} {ts(W[reg[0]][2])} …{' '.join(parts)}…")
json.dump(B,open(pre+'.json','w',encoding='utf-8'),ensure_ascii=False)
open(pre+'.txt','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('candidates',len(cand),'regions',len(regions))
