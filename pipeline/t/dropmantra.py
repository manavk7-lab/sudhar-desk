"""dropmantra.py items.json mantra_draft.json doc.txt out.json — drop fusion items that fall inside a recited mantra (replaced later by standard text)."""
import sys,json,re
items=json.load(open(sys.argv[1],encoding='utf-8')); M=json.load(open(sys.argv[2],encoding='utf-8')); doc=open(sys.argv[3],encoding='utf-8').read()
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
R=[]
for m in M:
    mm=list(re.finditer(flex(m.get('core',m['alt'])),doc))
    if len(mm)==1: R.append(mm[0].span())
    else: print('mantra not unique/found:',m['alt'][:50])
keep=[it for it in items if not any(a<it['end'] and it['pos']<b for a,b in R)]
json.dump(keep,open(sys.argv[4],'w',encoding='utf-8'),ensure_ascii=False)
print('items',len(items),'-> outside mantras',len(keep))
