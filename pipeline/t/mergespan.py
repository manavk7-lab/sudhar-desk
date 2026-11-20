"""mergespan.py TEXT ITEMS DOC_ORIG spec.json — spec: [[text_old, text_new, alt_from_doc, why, kind]]
Replace text_old by text_new in TEXT (must occur once) and make ONE item (cur=text_new, alt=alt_from_doc) in place of every
item whose cur lies inside / overlaps text_old's span. kind: applied | check. alt '' = take alt of the merged items joined."""
import sys,json,hashlib
T,I,D,SP=sys.argv[1:5]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8')); d=open(D,encoding='utf-8').read()
for old,new,alt,why,kind in json.load(open(SP,encoding='utf-8')):
    assert t.count(old)==1,('text',old); a=t.find(old); b=a+len(old)
    pos=[]
    for x in it:
        if t.count(x['cur'])!=1: continue
        p=t.find(x['cur']); q=p+len(x['cur'])
        if p<b and q>a: pos.append(x)
    # widen to cover merged items
    lo=min([a]+[t.find(x['cur']) for x in pos]); hi=max([b]+[t.find(x['cur'])+len(x['cur']) for x in pos])
    cur=t[lo:a]+new+t[b:hi]
    if alt and d.count(alt)!=1: print('ALT not once in doc',repr(alt)); sys.exit(1)
    base=dict(pos[0]) if pos else {'conf':'likely','heard':''}
    base.update(id=hashlib.sha1(cur.encode()).hexdigest()[:8],cur=cur,alt=alt or ' / '.join(x['alt'] for x in pos),kind=kind,
                why='; '.join(dict.fromkeys([why]+[x['why'] for x in pos])))
    at=it.index(pos[0]) if pos else len(it)
    ids={x['id'] for x in pos}; it=[x for x in it if x['id'] not in ids]; it.insert(min(at,len(it)),base)
    t=t[:lo]+cur+t[hi:]
    print('merged',len(pos),'->',base['id'],repr(cur[:80]))
open(T,'w',encoding='utf-8').write(t); json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
