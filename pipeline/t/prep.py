import os
import re,sys,json,difflib,bisect
sys.path.insert(0,os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'')
TOKR=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
def key(w):
    for a,b in [('‌',''),('‍',''),('ઁ',''),('ં',''),('઼',''),('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ણ','ન'),('ળ','લ')]: w=w.replace(a,b)
    return w.lower()
FILL={'હેને','હને','હેં','હેંને','હ','હાસ્ય','[હાસ્ય]'}
VID={'7':'D3l7ZWNJbR0','8':'xbT0_i5jYIw','9':'RMhKIMwo_Ug','10':'-ZSHmbN85HU','11':'aMW4vNKSgsQ','12':'R-JjINI9wZQ','13':'VeNDdNe_ofc'}
def mmss(ms): s=ms//1000; return f'{s//60}:{s%60:02d}'
for v,yt in VID.items():
    text=open(f'learn/cor{v}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    caps=[l.rstrip('\n').split('\t',1) for l in open(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+f'/sync/{yt}.tsv',encoding='utf-8') if l[0]!='#' and '\t' in l]
    C=[c[1].strip() for c in caps]; T=[int(c[0]) for c in caps]
    W=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(text)]
    D=[w[2] for w in W]
    sm=difflib.SequenceMatcher(None,[key(x) for x in D],[key(x) for x in C],autojunk=False)
    diffs=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        cw=[c for c in C[j1:j2] if c not in FILL and not c.startswith('[')]
        if op=='delete' and False: pass
        if op=='insert' and not cw: continue
        dpos=W[i1][0] if i1<len(W) else len(text)
        t=T[j1] if j1<len(T) else T[-1]
        diffs.append({'pos':dpos,'doc':' '.join(D[i1:i2]),'heard':' '.join(C[j1:j2]),'t':t,
                      'ctx':' '.join(D[max(0,i1-3):i1])+' ⟪'+' '.join(D[i1:i2])+'⟫ '+' '.join(D[i2:i2+3])})
    # chunks by paragraph, ~22k chars
    paras=[m.start() for m in re.finditer(r'\n\s*\n',text)]
    cuts=[0]; 
    for p in paras:
        if p-cuts[-1]>22000: cuts.append(p)
    if len(text)-cuts[-1]<6000 and len(cuts)>1: cuts.pop()
    cuts.append(len(text))
    for k in range(len(cuts)-1):
        a,b=cuts[k],cuts[k+1]; name=f'v{v}_{k+1}'
        open(f'proof/{name}.txt','w',encoding='utf-8').write(text[a:b])
        dd=[d for d in diffs if a<=d['pos']<b]
        with open(f'proof/{name}_ai.txt','w',encoding='utf-8') as f:
            for i,d in enumerate(dd):
                f.write(f"A{i+1}\t[{mmss(d['t'])}]\tdoc: {d['ctx']}\tASR heard: «{d['heard'] or '(nothing)'}»\n")
        json.dump({'video':v,'yt':yt,'offset':a,'end':b,'ai':dd},open(f'proof/{name}_meta.json','w',encoding='utf-8'),ensure_ascii=False)
        print(name,b-a,'chars',len(dd),'AI changes')
