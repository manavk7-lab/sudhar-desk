import sys,json,difflib,collections
sys.path.insert(0,'t')
from fuse import TOKR,key
doc=open(sys.argv[1],encoding='utf-8-sig').read(); fin=open(sys.argv[2],encoding='utf-8-sig').read()
C=json.load(open(sys.argv[3],encoding='utf-8')); cls=sys.argv[4]; want=sys.argv[5]
D=TOKR.findall(doc); F=TOKR.findall(fin)
his=[]
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,D,F,autojunk=False).get_opcodes():
    if op!='equal': his.append((i1,i2,' '.join(F[j1:j2])))
def kk(s): return ' '.join(key(x) for x in s.split())
for c in C:
    if '+'.join(c['by'])!=cls: continue
    exact=[h for h in his if h[0]==c['i1'] and h[1]==c['i2'] and kk(h[2])==kk(c['new'])]
    near=[h for h in his if h[0]<=c['i2'] and c['i1']<=h[1]]
    r='exact' if exact else ('area' if near else 'none')
    if r==want: print(f"[{c['old']}] → [{c['new']}]", ('| Manav: '+' / '.join(f'[{" ".join(D[h[0]:h[1]])}]→[{h[2]}]' for h in near)) if r=='area' else '', '|', c['ctx'].replace('\n',' ')[:90])
