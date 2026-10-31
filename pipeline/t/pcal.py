import json,sys,re,collections
txt=open(sys.argv[1],encoding='utf-8').read(); P=json.load(open(sys.argv[2])); lim=int(sys.argv[3]) if len(sys.argv)>3 else len(txt)
W=json.load(open(sys.argv[2]+'.words'))
rows=[]
for r in P:
    i=r['i']
    if W[i][1]>lim: continue
    sep=txt[W[i][1]:W[i+1][0]]
    lab='DOT' if re.search(r'[.?!]',sep) else ('COMMA' if ',' in sep else ('PARA' if '\n' in sep else 'NONE'))
    rows.append((r['pause'],lab,r['conf']))
def stat(f):
    by=collections.defaultdict(list)
    for p,l,c in rows:
        if f(c): by[l].append(p)
    for k,v in sorted(by.items()):
        v=sorted(v); print(f'  {k:6s} n={len(v):5d} pause median {v[len(v)//2]:.2f}  p25 {v[len(v)//4]:.2f}  p75 {v[3*len(v)//4]:.2f}  share>0.5s {sum(1 for x in v if x>=0.5)/len(v):.0%}')
print('matched words only:'); stat(lambda c:c==1)
print('threshold table (matched): pause>=x -> how many are his DOT / COMMA / NONE; DOTs below x')
R=[(p,l) for p,l,c in rows if c==1]
for x in [0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.2]:
    a=collections.Counter(l for p,l in R if p>=x); b=sum(1 for p,l in R if p<x and l=='DOT')
    tot=sum(a.values()); print(f'  >= {x:.1f}s: {tot:5d} boundaries  DOT {a["DOT"]:4d} ({a["DOT"]/max(1,tot):.0%})  COMMA {a["COMMA"]:4d}  NONE {a["NONE"]:4d} | his DOTs with shorter pause: {b}')
