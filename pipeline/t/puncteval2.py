import os
import re,json,difflib,collections,sys,glob
sys.path.insert(0,'t')
from fuse import TOKR
S=os.environ.get('SD_WORK','.')+''
# puncteval2.py base.txt now.txt pc.json out1.json [out2.json ...] — judge decisions vs what Manav has now
new2=open(sys.argv[1],encoding='utf-8').read(); now9=open(sys.argv[2],encoding='utf-8').read()
B=json.load(open(sys.argv[3],encoding='utf-8'))
D=[]
for p in sys.argv[4:]: D+=json.load(open(p,encoding='utf-8'))
A=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(new2)]; H=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(now9)]
mp={}
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,[t[2] for t in A],[t[2] for t in H],autojunk=False).get_opcodes():
    if op=='equal':
        for k in range(i2-i1): mp[i1+k]=j1+k
endidx={t[1]:k for k,t in enumerate(A)}
def lab(txt,a,b):
    s=txt[a:b]; return '.' if re.search(r'[.!]',s) else ('?' if '?' in s else (',' if ',' in s else ''))
def his(bid):
    b=B[bid]; k=endidx.get(b['pos'])
    if k is None or k not in mp or (k+1) not in mp or mp[k+1]!=mp[k]+1: return None
    j=mp[k]; return lab(now9,H[j][1],H[j+1][0])
leak={'નાખશે','જોશે','દીધી','બેસવાનું','જાતની','અંદર','પછી','જાણે','આપણે','તો'}
dec={d['id']:d['p'] for d in D}
st=collections.Counter(); ex=[]
for bid,b in B.items():
    h=his(bid)
    if h is None: continue
    cur=b['cur']; mine=dec.get(bid,cur)
    w=new2[A[endidx[b['pos']]][0]:b['pos']]
    if bid in dec:
        r='RIGHT (he did the same)' if mine==h else ('WRONG (he kept it)' if h==cur else 'he chose another mark')
        st[r]+=1; ex.append(f"{r[:5]} {bid} {w} cur={cur!r} → {mine!r} his={h!r} pause={b['pause']}")
    else:
        st['kept; he changed' if h!=cur else 'kept; he kept']+=1
for k,v in st.most_common(): print(v,k)
for e in ex: print('  ',e)
dd=sum(v for k,v in st.items() if k[:5] in ('RIGHT','WRONG','he ch'))
print('decided',dd,'right',st['RIGHT (he did the same)'],'touched-spot',st['RIGHT (he did the same)']+st['he chose another mark'])
