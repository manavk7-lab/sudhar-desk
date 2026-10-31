import sys,json,difflib,collections,re
sys.path.insert(0,__import__('os').path.dirname(__file__))
from fuse import TOKR,key
doc=open(sys.argv[1],encoding='utf-8-sig').read(); fin=open(sys.argv[2],encoding='utf-8-sig').read()
C=json.load(open(sys.argv[3],encoding='utf-8'))
D=TOKR.findall(doc); F=TOKR.findall(fin)
his=[]
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,D,F,autojunk=False).get_opcodes():
    if op!='equal': his.append((i1,i2,' '.join(F[j1:j2])))
def kk(s): return ' '.join(key(x) for x in s.split())
st=collections.Counter(); hit=set()
for c in C:
    cls='+'.join(c['by'])
    exact=[h for h in his if h[0]==c['i1'] and h[1]==c['i2'] and kk(h[2])==kk(c['new'])]
    near=[h for h in his if h[0]<=c['i2'] and c['i1']<=h[1]]
    r='exact' if exact else ('area' if near else 'none')
    st[(cls,r)]+=1
    for h in near: hit.add(h)
classes=sorted(set(k[0] for k in st))
for cl in classes:
    e,a,n=st[(cl,'exact')],st[(cl,'area')],st[(cl,'none')]
    print(f'{cl:8s} cands {e+a+n:4d}  same fix as Manav {e:3d}  he changed that spot differently {a:3d}  he left it {n:4d}')
print('Manav edits',len(his),'— spots touched by some candidate',len(hit))
