"""Cluster engine disagreements with a backbone Doc.
usage: fuse2.py doc.txt out.json S=sarvam.txt G=gemini.txt [Y=youtube.tsv]   (engines listed before Y trigger items; Y is info only)
item: {id,a,b,pos,end,old,read:{S:..,G:..,Y:..},t,ctx,kind}"""
import re,sys,json,difflib,collections
sys.path.insert(0,__import__('os').path.dirname(__file__))
from fuse import TOKR,FILL,key,load_engine
INFO={'Y'}
def bmap(D,E):
    """boundary map doc index->engine index, plus list of nonequal blocks"""
    sm=difflib.SequenceMatcher(None,[key(x) for x in D],[key(x) for x in E],autojunk=False)
    m={};blocks=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal':
            for k in range(i2-i1+1): m[i1+k]=j1+k
        else:
            m.setdefault(i1,j1); m[i2]=j2
            # a pure insertion is shown on the doc word before it (so engines' extra words are visible)
            blocks.append((i1-1,i2) if (op=='insert' and i1>0) else (i1,i2))
    return m,blocks
def main():
    doc=open(sys.argv[1],encoding='utf-8-sig').read().replace('\r\n','\n'); out=sys.argv[2]
    eng={}
    for a in sys.argv[3:]:
        n,p=a.split('=',1); eng[n]=load_engine(p)
    toks=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(doc)]
    D=[t[2] for t in toks]; N=len(D)
    maps={};blocks={}
    gaps={}
    for n,(E,T) in eng.items():
        maps[n],blocks[n]=bmap(D,E)
        gi=[j for j,w in enumerate(E) if w=='ZZGAPZZ']
        gaps[n]=[]
        if gi:
            sm=difflib.SequenceMatcher(None,[key(x) for x in D],[key(x) for x in E],autojunk=False)
            ops=sm.get_opcodes()
            for k,(op,i1,i2,j1,j2) in enumerate(ops):
                if op!='equal' and any(j1<=g<j2 for g in gi):
                    lo,hi=k,k
                    while lo>=2 and ops[lo-1][0]=='equal' and ops[lo-1][2]-ops[lo-1][1]<6: lo-=2
                    while hi+2<len(ops) and ops[hi+1][0]=='equal' and ops[hi+1][2]-ops[hi+1][1]<6: hi+=2
                    gaps[n].append((ops[lo][1],ops[hi][2]))
            blocks[n]=[b for b in blocks[n] if not any(g[0]<=b[0] and b[1]<=g[1] for g in gaps[n])]
            print(n,'gaps (doc tokens):',gaps[n])
    def ingap(n,a,b): return any(g[0]<b and a<g[1] or (a==b and g[0]<a<g[1]) for g in gaps[n])
    # trigger spans from non-info engines; grow with any engine's blocks overlapping
    allb=sorted(set(b for n in eng for b in blocks[n]))
    trig=sorted(set(b for n in eng if n not in INFO for b in blocks[n]))
    # union-find style sweep: merge blocks that overlap or touch
    spans=[]
    for a,b in sorted(allb):
        if spans and a<=spans[-1][1] and (a<spans[-1][1] or a==b or spans[-1][0]==spans[-1][1]):
            spans[-1][1]=max(spans[-1][1],b)
        elif spans and a==spans[-1][1] and (a==b or spans[-1][0]==spans[-1][1]):
            spans[-1][1]=max(spans[-1][1],b)
        else: spans.append([a,b])
    # make sure every span boundary is a valid boundary in all engines
    def ok(i): return all(i in maps[n] or any(g[0]<i<g[1] for g in gaps[n]) for n in eng)
    fixed=[]
    for a,b in spans:
        while not ok(a): a-=1
        while not ok(b): b+=1
        if fixed and a<fixed[-1][1]: fixed[-1][1]=max(fixed[-1][1],b)
        else: fixed.append([a,b])
    items=[]
    for a,b in fixed:
        if not any(a<=t1 and t2<=b and (t1,t2)!=(None,None) for t1,t2 in trig if (t1<b or (t1==t2 and t1<=b)) and t2>=a): continue
        read={}
        for n,(E,T) in eng.items():
            read[n]=None if ingap(n,a,b) or a not in maps[n] or b not in maps[n] else ' '.join(E[maps[n][a]:maps[n][b]])
        old=' '.join(D[a:b])
        trig_eng=[n for n in eng if n not in INFO and read[n] is not None and ' '.join(key(x) for x in read[n].split())!=' '.join(key(x) for x in old.split())]
        if not trig_eng: continue
        if a<b: pos,end=toks[a][0],toks[b-1][1]
        else:
            pos=end=toks[a-1][1] if a>0 else 0
        cs=toks[max(0,a-8)][0] if toks else 0; ce=toks[min(N-1,b+7)][1] if toks else 0
        t=None
        for n,(E,T) in eng.items():
            if T and a in maps[n]:
                j=maps[n][a]; t=T[min(j,len(T)-1)] if T else None
        items.append({'a':a,'b':b,'pos':pos,'end':end,'old':old,'read':read,'by':trig_eng,
                      'ctx':(doc[cs:pos]+'⟪'+doc[pos:end]+'⟫'+doc[end:ce]).replace('\n',' '),'t':t})
    for k,it in enumerate(items): it['id']=f'c{k+1}'
    json.dump(items,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    c=collections.Counter('+'.join(x['by']) for x in items); print(len(items),'items',dict(c))
if __name__=='__main__': main()
