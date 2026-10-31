"""fixitems.py before.txt after.txt items.json out.json — carry ✎ items made on before.txt over to after.txt when only
punctuation changed in between (same whitespace tokens): an item's cur/alt get the punctuation the words have now."""
import sys,json,re
B=open(sys.argv[1],encoding='utf-8').read(); A=open(sys.argv[2],encoding='utf-8').read(); items=json.load(open(sys.argv[3],encoding='utf-8'))
TB=[(m.start(),m.end(),m.group()) for m in re.finditer(r'\S+',B)]; TA=[m.group() for m in re.finditer(r'\S+',A)]
assert len(TB)==len(TA), ('token count differs',len(TB),len(TA))
strip=lambda w: re.sub(r'[.,?!]','',w)
assert all(strip(x[2])==strip(y) for x,y in zip(TB,TA)), 'words differ'
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
start={s:i for i,(s,e,w) in enumerate(TB)}
out=[];moved=0;lost=0
for it in items:
    if len(re.findall(flex(it['cur']),A))==1: out.append(it); continue
    m=list(re.finditer(flex(it['cur']),B))
    if len(m)!=1 or m[0].start() not in start: lost+=1; print('lost',it['cur'][:60]); continue
    i=start[m[0].start()]; n=len(it['cur'].split())
    cur_old=it['cur'].split(); cur_new=TA[i:i+n]
    alt=it['alt'].split()
    # common prefix / suffix of cur and alt take the new punctuation
    p=0
    while p<min(len(cur_old),len(alt)) and cur_old[p]==alt[p]: p+=1
    s=0
    while s<min(len(cur_old),len(alt))-p and cur_old[-1-s]==alt[-1-s]: s+=1
    alt_new=cur_new[:p]+alt[p:len(alt)-s]+(cur_new[len(cur_new)-s:] if s else [])
    it=dict(it); it['cur']=' '.join(cur_new); it['alt']=' '.join(alt_new)
    if len(re.findall(flex(it['cur']),A))!=1: lost+=1; print('not unique now',it['cur'][:60]); continue
    out.append(it); moved+=1
json.dump(out,open(sys.argv[4],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('items',len(items),'carried over',moved,'lost',lost)
