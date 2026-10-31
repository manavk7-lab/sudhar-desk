"""cands.py doc.txt out.json [--from CHARPOS] S=sar.txt G=gem.txt Y=yt.tsv
Rule-based candidate spots for the lessons from video 9 (judged by an LLM afterwards):
  ERG  એને/આને/તેને/જેને that may be the doer (એણે/આણે/તેણે/જેણે)
  SHU  a lone 'શું?' standing between sentences (speaker's habit; Manav deletes)
  SKT  a word where an engine heard the same word + Sanskrit ending મ/મ્ (સદગુરુ→સદગુરુમ)
Items use the same format as fuse2 (id,a,b,pos,end,old,read,by,ctx,t,kind)."""
import re,sys,json
sys.path.insert(0,'t')
from fuse import TOKR,key,load_engine
from fuse2 import bmap
args=[a for a in sys.argv[1:] if '=' not in a or a.startswith('--')]
doc=open(sys.argv[1],encoding='utf-8').read(); out=sys.argv[2]
start=0
if '--from' in sys.argv: start=int(sys.argv[sys.argv.index('--from')+1])
eng={}
for a in sys.argv[3:]:
    if '=' in a and not a.startswith('--'):
        n,p=a.split('=',1); eng[n]=load_engine(p)
toks=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(doc)]
D=[t[2] for t in toks]; N=len(D)
maps={n:bmap(D,E)[0] for n,(E,T) in eng.items()}
def read(n,a,b):
    m=maps[n]; E=eng[n][0]
    if a in m and b in m: return ' '.join(E[m[a]:m[b]])
    return None
def tm(a):
    if 'Y' in eng and eng['Y'][1]:
        m=maps['Y']; T=eng['Y'][1]
        for k in range(a,max(-1,a-40),-1):
            if k in m and m[k]<len(T): return T[m[k]]
    return None
def ctx(a,b,w=12):
    cs=toks[max(0,a-w)][0]; ce=toks[min(N-1,b+w-1)][1]
    pos,end=toks[a][0],toks[b-1][1]
    return (doc[cs:pos]+'⟪'+doc[pos:end]+'⟫'+doc[end:ce]).replace('\n',' ')
items=[]
def add(kind,a,b):
    pos,end=toks[a][0],toks[b-1][1]
    if kind=='SHU' and end<len(doc) and doc[end]=='?': end+=1
    if pos<start: return
    r={n:read(n,a,b) for n in eng}
    c=ctx(a,b)
    if kind=='SHU': c=c.replace('⟪શું⟫?','⟪શું?⟫')
    items.append({'kind':kind,'a':a,'b':b,'pos':pos,'end':end,'old':doc[pos:end],'read':r,'by':[kind],'ctx':c,'t':tm(a)})
for i,w in enumerate(D):
    if w in ('એને','આને','તેને','જેને'): add('ERG',i,i+1)
for m in re.finditer(r'(?<=[.!?])(\s+)(શું\?)(?=\s)',doc):
    s=m.start(2); i=next(k for k,t in enumerate(toks) if t[0]==s); add('SHU',i,i+1)
for i,w in enumerate(D):
    kw=key(w)
    for n in ('S','G'):
        if n not in eng: continue
        r=read(n,i,i+1)
        if r and len(r.split())==1:
            rk=key(r)
            if rk in (kw+'મ',kw+'ત') and len(kw)>=3: add('SKT',i,i+1); break
items.sort(key=lambda x:x['pos'])
seen=set();uniq=[]
for it in items:
    k=(it['a'],it['kind'])
    if k in seen: continue
    seen.add(k); uniq.append(it)
for k,it in enumerate(uniq): it['id']=f"{it['kind'][0].lower()}{k+1}"
json.dump(uniq,open(out,'w',encoding='utf-8'),ensure_ascii=False)
import collections; print(len(uniq),collections.Counter(x['kind'] for x in uniq))
