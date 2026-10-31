import sys,json,re,difflib,collections; sys.path.insert(0,'t')
from learn import toks
def lev(a,b):
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False); 
    d=0
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': d+=max(i2-i1,j2-j1)
    return d
def evaluate(raw,fin,edits,show=False):
    R=toks(raw); F=toks(fin)
    # map raw char pos -> token index
    pos=[m.start() for m in re.finditer(r'[઀-૿A-Za-z0-9‌‍]+',raw)]
    import bisect
    sm=difflib.SequenceMatcher(None,R,F,autojunk=False)
    # raw token -> fin token index (approx) 
    rmap={}
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        for k in range(i1,i2): rmap[k]=j1+(k-i1)*(j2-j1)//max(1,i2-i1)
    res=collections.Counter(); bad=[]
    for e in edits:
        p=raw.find(e['find'])
        if p<0: res[e['conf'],'notfound']+=1; continue
        a=bisect.bisect_left(pos,p); b=bisect.bisect_left(pos,p+len(e['find']))
        a0=max(0,a-3); b0=min(len(R),b+3)
        fa=rmap.get(a0,0); fb=rmap.get(b0,len(F)) if b0<len(R) else len(F)
        win=F[max(0,fa-2):fb+2]
        before=R[a0:b0]; after=R[a0:a]+toks(e['replace'])+R[b:b0]
        d0=lev(before,win); d1=lev(after,win)
        r='good' if d1<d0 else ('bad' if d1>d0 else 'neutral')
        res[e['conf'],r]+=1
        if show and r!='good': bad.append((e['conf'],r,e['find'],'→',e['replace'],'| fin:',' '.join(win)))
    return res,bad
if __name__=='__main__':
    raw=open(sys.argv[1],encoding='utf-8-sig').read(); fin=open(sys.argv[2],encoding='utf-8-sig').read()
    E=json.load(open(sys.argv[3],encoding='utf-8'))
    res,bad=evaluate(raw,fin,E,True)
    for c in ('sure','likely','unsure'):
        g,b,n=res[c,'good'],res[c,'bad'],res[c,'neutral']; print(c,'good',g,'bad',b,'neutral',n,'notfound',res[c,'notfound'],f'precision {g/max(1,g+b+n):.0%}')
    for x in bad[:60]: print(*x)
