"""Compare a backbone Doc text with several ASR engines and list candidate changes.
usage: fuse.py doc.txt out.json S=sarvam.txt G=gemini.txt Y=youtube.txt [Y may be a .tsv with times]"""
import re,sys,json,difflib,collections
TOKR=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
FILL={'હેને','હને','હેં','હેંને','હાસ્ય','હમ્મ','ઓમ'}
def key(w):
    for a,b in [('‌',''),('‍',''),('ઁ',''),('ં',''),('઼',''),('્',''),('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ણ','ન'),('ળ','લ'),('શ','સ'),('ષ','સ')]: w=w.replace(a,b)
    return w
def load_engine(path):
    if path.endswith('.tsv'):
        W=[];T=[]
        for l in open(path,encoding='utf-8'):
            if l[0]=='#' or '\t' not in l: continue
            t,w=l.rstrip('\n').split('\t',1); w=w.strip()
            for x in TOKR.findall(w):
                if x not in FILL: W.append(x); T.append(int(t))
        return W,T
    W=[x for x in TOKR.findall(open(path,encoding='utf-8-sig').read()) if x not in FILL]
    return W,None
def opcodes(D,E):
    return difflib.SequenceMatcher(None,[key(x) for x in D],[key(x) for x in E],autojunk=False).get_opcodes()
def main():
    doc=open(sys.argv[1],encoding='utf-8-sig').read().replace('\r\n','\n')
    out=sys.argv[2]
    eng={}
    for a in sys.argv[3:]:
        n,p=a.split('=',1); eng[n]=load_engine(p)
    toks=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(doc)]
    D=[t[2] for t in toks]
    props=collections.defaultdict(dict)   # (i1,i2) -> {engine: newtext}
    times={}
    for n,(E,T) in eng.items():
        for op,i1,i2,j1,j2 in opcodes(D,E):
            if op=='equal':
                if T:
                    for k in range(i2-i1): times.setdefault(i1+k,T[j1+k])
                continue
            new=' '.join(E[j1:j2])
            # ignore pure filler deletions in doc that engines also lack? keep all
            props[(i1,i2)][n]=new
            if T and j1<len(T): times.setdefault(i1,T[j1])
    cands=[]
    for (i1,i2),d in props.items():
        old=' '.join(D[i1:i2])
        # group engines by key-equal proposal
        groups=collections.defaultdict(list)
        for n,new in d.items(): groups[' '.join(key(x) for x in new.split())].append((n,new))
        for k,lst in groups.items():
            names=sorted(n for n,_ in lst)
            s=toks[i1][0] if i1<len(toks) else len(doc)
            e=toks[i2-1][1] if i2>i1 else s
            ctx_s=toks[max(0,i1-6)][0] if toks else 0; ctx_e=toks[min(len(toks)-1,i2+5)][1] if toks else 0
            cands.append({'i1':i1,'i2':i2,'old':old,'new':lst[0][1],'by':names,'pos':s,'end':e,
                          'ctx':doc[ctx_s:s]+'⟪'+doc[s:e]+'⟫'+doc[e:ctx_e],'t':times.get(i1)})
    cands.sort(key=lambda c:(c['pos'],-len(c['by'])))
    json.dump(cands,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    c=collections.Counter('+'.join(x['by']) for x in cands); print(len(cands),'candidates',dict(c))
if __name__=='__main__': main()
