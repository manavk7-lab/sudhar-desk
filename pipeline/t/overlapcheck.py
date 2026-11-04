"""overlapcheck.py text.txt items.json — list ✎ items whose text spans overlap where the shared part is CHANGED text of one of them
(sharing only unchanged context words is harmless)."""
import json,re,sys
t=open(sys.argv[1]).read(); P=json.load(open(sys.argv[2]))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def core(it,s0):
    c,a=it['cur'],it.get('alt','')
    i=0
    while i<min(len(c),len(a)) and c[i]==a[i]: i+=1
    j=0
    while j<min(len(c),len(a))-i and c[-1-j]==a[-1-j]: j+=1
    return (s0+i, s0+len(c)-j)
sp=[]
for it in P:
    m=list(re.finditer(flex(it['cur']),t)); 
    if len(m)!=1: print('NOT UNIQUE',it['cur']); continue
    s,e=m[0].span(); sp.append((s,e,core(it,s),it))
sp.sort(key=lambda x:x[0]); bad=0
for i in range(len(sp)):
    for j in range(i+1,len(sp)):
        a,b=sp[i],sp[j]
        if b[0]>=a[1]: break
        o0,o1=b[0],min(a[1],b[1])
        hit=any(max(o0,c0)<min(o1,c1) or (c0==c1 and o0<=c0<=o1) for c0,c1 in (a[2],b[2]))
        if hit: bad+=1; print('BAD',repr(a[3]['cur']),'|',repr(b[3]['cur']))
print('items',len(sp),'bad overlaps',bad)
