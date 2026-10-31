import sys,collections; sys.path.insert(0,'t')
from learn import rd,toks,ops
FILL={'હેને','હને','હેં','હેંને','હાસ્ય','હ','હે'}
def pairs(R,F):
    """word-level (raw_index, raw_word, final_phrase) for every raw word; 1:1 inside equal-length replace blocks"""
    out=[]
    for op,i1,i2,j1,j2 in ops(R,F):
        if op=='equal':
            for k in range(i2-i1): out.append((i1+k,R[i1+k],R[i1+k]))
        elif op=='delete':
            for k in range(i1,i2): out.append((k,R[k],''))
        elif op=='replace':
            if i2-i1==j2-j1:
                for k in range(i2-i1): out.append((i1+k,R[i1+k],F[j1+k]))
            elif i2-i1==1: out.append((i1,R[i1],' '.join(F[j1:j2])))
            else:
                for k in range(i1,i2): out.append((k,R[k],None))   # unknown mapping
    return out
def learn(vs):
    uni=collections.defaultdict(collections.Counter); nxt=collections.defaultdict(collections.Counter); prv=collections.defaultdict(collections.Counter)
    for v in vs:
        R=toks(rd('raw'+v)); F=toks(rd('fin'+v))
        for i,w,f in pairs(R,F):
            if f is None: continue
            uni[w][f]+=1
            nxt[(w,R[i+1] if i+1<len(R) else '')][f]+=1
            prv[(R[i-1] if i else '',w)][f]+=1
    return uni,nxt,prv
def decide(w,p,n,M,minc=2,thr=0.9):
    uni,nxt,prv=M
    for tab,k in ((nxt,(w,n)),(prv,(p,w)),(uni,w)):
        c=tab.get(k)
        if not c: continue
        tot=sum(c.values()); f,cnt=c.most_common(1)[0]
        if tot>=minc and cnt/tot>=thr: return (f,cnt,tot)
        if tab is uni: return None
        if tot>=4: return None   # context seen enough and ambiguous: don't fall back
    return None
if __name__=='__main__':
    vids=['1','2','3','4','5','6']
    G=collections.Counter()
    for v in vids:
        M=learn([x for x in vids if x!=v])
        R=toks(rd('raw'+v)); F=toks(rd('fin'+v))
        truth={i:f for i,w,f in pairs(R,F)}
        st=collections.Counter(); bad=collections.Counter()
        for i,w in enumerate(R):
            d=decide(w,R[i-1] if i else '',R[i+1] if i+1<len(R) else '',M)
            if d and d[0]!=w:
                t=truth.get(i)
                if t is None: st['unk']+=1
                elif t==d[0]: st['right']+=1
                else: st['wrong']+=1; bad[(w,d[0],t)]+=1
            # missed
            t=truth.get(i)
            if t is not None and t!=w and not (d and d[0]==t): st['missed']+=1
        G+=st
        print(v,dict(st),'precision',round(st['right']/max(1,st['right']+st['wrong']),3),'recall',round(st['right']/max(1,st['right']+st['missed']),3), bad.most_common(6))
    print('ALL',dict(G),round(G['right']/(G['right']+G['wrong']),3),round(G['right']/(G['right']+G['missed']),3))
