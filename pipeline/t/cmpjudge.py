"""cmpjudge.py j.txt A.json B.json [nameA nameB] — compare two judge runs on the same j file.
Lines absent from an output count as keep. Prints counts per run, agreement, and every line where the two differ
(decision or text), with the line's context so a reviewer can say which run was right."""
import json,re,sys
J,A,B=sys.argv[1:4]; na=sys.argv[4] if len(sys.argv)>4 else 'A'; nb=sys.argv[5] if len(sys.argv)>5 else 'B'
lines={}
for l in open(J,encoding='utf-8'):
    m=re.match(r'(\S+) ',l)
    if m: lines[m.group(1)]=l.rstrip('\n')
def load(p):
    d={}
    for x in json.load(open(p,encoding='utf-8')): d[x['id']]=x
    return d
a=load(A); b=load(B)
def dec(d,i): return (d[i]['d'],d[i].get('text','')) if i in d else ('keep','')
from collections import Counter
ca=Counter(dec(a,i)[0] for i in lines); cb=Counter(dec(b,i)[0] for i in lines)
print(f'lines {len(lines)}'); print(f'{na}: {dict(ca)}'); print(f'{nb}: {dict(cb)}')
same=0; diff=[]
for i in lines:
    da,db=dec(a,i),dec(b,i)
    # applied text: fix/maybe apply, keep/ask leave the Doc
    ta=da[1] if da[0] in ('fix','maybe') else None; tb=db[1] if db[0] in ('fix','maybe') else None
    if da==db: same+=1
    else: diff.append((i,da,db,ta!=tb))
print(f'identical decisions {same}/{len(lines)}; differ {len(diff)}; of those the resulting text differs in {sum(1 for x in diff if x[3])}')
for i,da,db,td in diff:
    ctx=re.sub(r' \|\| B:.*?(?= \|\||$)','',lines[i])
    print(f'\n{"*" if td else " "} {i}  {na}: {da[0]} [{da[1]}]  {(a.get(i) or {}).get("why","")[:90]}')
    print(f'      {nb}: {db[0]} [{db[1]}]  {(b.get(i) or {}).get("why","")[:90]}')
    print('      '+ctx[:330])
