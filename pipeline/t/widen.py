"""widen.py final.txt items.json doc_orig.txt — give every ✎ item whose cur occurs more than once in final.txt a unique
context: add the same unchanged words before (then after) to cur and alt until cur is unique in final.txt and alt is
unique in the Doc as read (quotes removed). Items that share a cur get different occurrences. Prints what it could not fix
(cur not found at all = a stale item: fix by hand)."""
import json,re,sys
F,I,O=sys.argv[1:4]
t=open(F,encoding='utf-8').read()
o=re.sub(r'["“”]','',open(O,encoding='utf-8').read()); o=re.sub(r"(?<![઀-૿])'|'(?![઀-૿])",'',o)
D=json.load(open(I,encoding='utf-8')); d=D['items'] if isinstance(D,dict) else D
def fl(s): return r'\s+'.join(re.escape(w) for w in s.split())
def cnt(p,s): return len(re.findall(fl(p),s)) if p.strip() else 0
used=set(); fixed=0; bad=[]
for x in d:
    c=x['cur']
    if not c.strip() or cnt(c,t)==1: continue
    occ=[m.span() for m in re.finditer(fl(c),t)]
    if not occ: bad.append(('stale',x['id'],c[:50])); continue
    done=False
    for side in ('L','R','LR'):
        for k in range(1,15):
            for (s,e) in occ:
                if (s,e) in used: continue
                L=t[:s].split()[-k:] if 'L' in side else []
                R=t[e:].split()[:k] if 'R' in side else []
                if 'L' in side and len(t[:s].split())<k or 'R' in side and len(t[e:].split())<k: continue
                pre=' '.join(L)+' ' if L else ''; post=' '+' '.join(R) if R else ''
                # keep the item's own spacing: only join with single spaces at the edges
                nc=pre+c+post; na=pre+x['alt']+post
                if cnt(nc,t)==1 and cnt(na,o)==1:
                    m=re.search(fl(nc),t); nc=t[m.start():m.end()]
                    x['cur']=nc; x['alt']=na; used.add((s,e)); done=True; fixed+=1; break
            if done: break
        if done: break
    if not done: bad.append(('nofix',x['id'],c[:50]))
json.dump(D,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('widened',fixed,'left',bad)
