"""mergealign.py final.txt items.json doc_orig.txt — merge every group of overlapping applied ✎ items into ONE item whose
alt is taken from the Doc itself (no undo order needed): the words of final.txt and of the Doc (quotation marks removed,
as revertcheck.py compares) are aligned; the merged span is widened to the nearest unchanged words on both sides, and
alt = the Doc's text for that span. Use it when foldfix / mergeover say "could not". Check items are left alone (their
alt is a suggestion); a check item that overlaps a merged item is reported. Rewrites items.json; run revertcheck after."""
import json,re,sys,difflib
T,I,D=sys.argv[1:4]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8'))
ref=open(D,encoding='utf-8').read().replace('"','').replace('“','').replace('”','')
def toks(s): return [(m.start(),m.end(),m.group()) for m in re.finditer(r'\S+',s)]
TF,TR=toks(t),toks(ref)
sm=difflib.SequenceMatcher(None,[x[2] for x in TF],[x[2] for x in TR],autojunk=False)
ops=sm.get_opcodes()
# token-level map final i -> ref j for equal tokens
eq={}
for tag,a0,a1,b0,b1 in ops:
    if tag=='equal':
        for k in range(a1-a0): eq[a0+k]=b0+k
def span(x):
    p=t.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 and t.count(x['cur'])==1 else None
app=[(span(x),x) for x in it if x.get('kind')!='check' and span(x)]
app.sort(key=lambda q:q[0][0])
# groups of overlapping applied items
groups=[];cur=None
for (s,e),x in app:
    if cur and s<cur[1]: cur[2].append(x); cur[1]=max(cur[1],e)
    else:
        cur=[s,e,[x]]; groups.append(cur)
groups=[g for g in groups if len(g[2])>1]
merged=0
for s,e,members in groups:
    i0=next(k for k,(a,b,_) in enumerate(TF) if b>s)
    i1=max(k for k,(a,b,_) in enumerate(TF) if a<e)
    # widen to unchanged words on both sides
    while i0>0 and i0 not in eq: i0-=1
    while i1<len(TF)-1 and i1 not in eq: i1+=1
    for _ in range(6):
        j0,j1=eq.get(i0),eq.get(i1)
        if j0 is None or j1 is None: print('no anchor for group at',s); break
        c=t[TF[i0][0]:TF[i1][1]]; a=ref[TR[j0][0]:TR[j1][1]]
        if t.count(c)==1: break
        i0=max(0,i0-1); i1=min(len(TF)-1,i1+1)
        while i0>0 and i0 not in eq: i0-=1
        while i1<len(TF)-1 and i1 not in eq: i1+=1
    else:
        print('not unique',repr(c[:60])); continue
    if j0 is None or j1 is None: continue
    A=members[0]
    A['cur']=c; A['alt']=a; A['kind']='applied'
    A['why']=' ; '.join(dict.fromkeys(m.get('why','') for m in members if m.get('why')))
    A['heard']=' · '.join(dict.fromkeys(m.get('heard') for m in members if m.get('heard'))) or A.get('heard')
    A['conf']='unsure' if any(m.get('conf')=='unsure' for m in members) else ('likely' if any(m.get('conf')=='likely' for m in members) else A.get('conf','sure'))
    ts=[m['t'] for m in members if m.get('t')];
    if ts: A['t']=min(ts)
    drop={id(m) for m in members[1:]}
    it=[x for x in it if id(x) not in drop]
    merged+=1; print('merged',len(members),'->',repr(c[:90]))
    # check items inside
    for x in it:
        if x.get('kind')=='check':
            p=t.find(x['cur'])
            if p>=0 and p<TF[i1][1] and p+len(x['cur'])>TF[i0][0]: print('  NOTE check item overlaps:',repr(x['cur'][:50]))
json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('groups merged',merged,'items',len(it))
