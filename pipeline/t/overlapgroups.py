"""overlapgroups.py text.txt items.json groups.json — like overlapcheck.py, but writes the overlapping items as id groups
(chains merged) for foldfix.py."""
import json,re,sys
t=open(sys.argv[1],encoding='utf-8').read(); P=json.load(open(sys.argv[2],encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def core(it,s0):
    c,a=it['cur'],it.get('alt',''); i=0
    while i<min(len(c),len(a)) and c[i]==a[i]: i+=1
    j=0
    while j<min(len(c),len(a))-i and c[-1-j]==a[-1-j]: j+=1
    return (s0+i, s0+len(c)-j)
sp=[]
for it in P:
    m=list(re.finditer(flex(it['cur']),t))
    if len(m)==1: s,e=m[0].span(); sp.append((s,e,core(it,s),it))
sp.sort(key=lambda x:x[0]); par={}
def find(x):
    while par.get(x,x)!=x: x=par[x]
    return x
for i in range(len(sp)):
    for j in range(i+1,len(sp)):
        a,b=sp[i],sp[j]
        if b[0]>=a[1]: break
        o0,o1=b[0],min(a[1],b[1])
        if any(max(o0,c0)<min(o1,c1) or (c0==c1 and o0<=c0<=o1) for c0,c1 in (a[2],b[2])):
            par[find(b[3]['id'])]=find(a[3]['id'])
groups={}
for s,e,c,it in sp:
    if it['id'] in par or any(find(k)==it['id'] for k in par): groups.setdefault(find(it['id']),[]).append(it['id'])
G=[g for g in groups.values() if len(g)>1]
json.dump(G,open(sys.argv[3],'w'),ensure_ascii=False); print('groups',len(G),G)
