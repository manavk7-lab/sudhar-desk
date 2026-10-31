"""snipapply.py current_doc.txt items.json out.txt out_items.json — apply ✎ items (alt -> cur) onto a doc that may have changed since."""
import sys,json,re,hashlib
doc=open(sys.argv[1],encoding='utf-8').read(); items=json.load(open(sys.argv[2],encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
done=[];skip=[]
for it in items:
    m=list(re.finditer(flex(it['alt']),doc))
    if len(m)!=1: skip.append(it); continue
    a,b=m[0].span()
    # keep the doc's own whitespace (e.g. paragraph breaks) where token count matches
    seg=doc[a:b]; toks_old=it['alt'].split(); toks_new=it['cur'].split()
    if len(toks_old)==len(toks_new):
        ws=re.findall(r'\s+',seg); rep=toks_new[0]+''.join(w+t for w,t in zip(ws,toks_new[1:]))
    else: rep=it['cur']
    doc=doc[:a]+rep+doc[b:]; done.append(it)
open(sys.argv[3],'w',encoding='utf-8').write(doc)
json.dump(done,open(sys.argv[4],'w',encoding='utf-8'),ensure_ascii=False)
print('applied',len(done),'skipped',len(skip),'sha',hashlib.sha256(doc.encode()).hexdigest()[:16])
for it in skip: print('  skipped:',it['alt'][:70])
