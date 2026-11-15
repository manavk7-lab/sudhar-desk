"""mergeover.py text.txt items.json — merge every pair of overlapping ✎ items into one (fallback when foldfix cannot).
Merged cur = the union of the two spans in text.txt; merged alt = that text with both items undone (the order that
works: the item whose cur is still found inside the other's undone text is undone second). Check items are only merged
with each other (their alt is a suggestion). Rewrites items.json; prints what it merged or could not."""
import json,sys
T,I=sys.argv[1:3]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8'))
def span(x):
    p=t.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 and t.count(x['cur'])==1 else None
def undo(s,x):
    return s.replace(x['cur'],x['alt'],1) if s.count(x['cur'])==1 else None
changed=True
while changed:
    changed=False
    sp=sorted([(span(x),x) for x in it if span(x)],key=lambda q:q[0][0])
    pairs=[(i,j) for i in range(len(sp)) for j in range(i+1,len(sp)) if sp[j][0][0]<sp[i][0][1]]
    for i,j in pairs:
        (a0,a1),A=sp[i]; (b0,b1),B=sp[j]
        if (A.get('kind')=='check')!=(B.get('kind')=='check'): print('SKIP check/applied',repr(A['cur'][:40]),repr(B['cur'][:40])); continue
        U0,U1=min(a0,b0),max(a1,b1); cur=t[U0:U1]
        alt=None
        for X,Y in ((B,A),(A,B)):
            s1=undo(cur,X)
            if s1 is None: continue
            # Y's cur must be found in the text with X undone — rebuild Y's span inside s1
            s2=undo(s1,Y)
            if s2 is not None: alt=s2; break
        if alt is None:
            # last resort: undo each inside its own span of the union, from the right
            print('could not merge',repr(A['cur'][:50]),'|',repr(B['cur'][:50])); continue
        A['cur']=cur; A['alt']=alt; A['why']=(A.get('why','')+' ; '+B.get('why','')).strip(' ;')
        A['conf']='unsure' if 'unsure' in (A.get('conf'),B.get('conf')) else A.get('conf','likely')
        it=[x for x in it if x is not B]; changed=True
        print('merged',repr(cur[:80]))
        break
json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('items',len(it))
