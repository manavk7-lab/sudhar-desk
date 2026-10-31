"""mydiff.py posted.txt now.txt review.json out.txt — what Manav changed after our pass.
Word changes (punctuation ignored) and punctuation changes, with context; which of our ✎ items he undid."""
import sys,re,json,difflib,collections
P=open(sys.argv[1],encoding='utf-8').read(); N=open(sys.argv[2],encoding='utf-8').read()
R=json.load(open(sys.argv[3],encoding='utf-8'))['items']; out=sys.argv[4]
TOK=re.compile(r'\S+')
def toks(t): return [(m.group(),m.start()) for m in TOK.finditer(t)]
TP,TN=toks(P),toks(N)
def core(w): return re.sub(r'[^\w઀-૿]','',w)
def punc(w): return re.sub(r'[\w઀-૿]','',w)
cp=[core(w) for w,_ in TP]; cn=[core(w) for w,_ in TN]
sm=difflib.SequenceMatcher(None,cp,cn,autojunk=False)
W=[];Pc=collections.Counter();PL=[]
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='equal':
        for k in range(i2-i1):
            a=punc(TP[i1+k][0]); b=punc(TN[j1+k][0])
            if a!=b:
                Pc[(a or '∅')+'→'+(b or '∅')]+=1
                ctx=' '.join(w for w,_ in TN[max(0,j1+k-5):j1+k+5])
                PL.append(f'{a or "∅"}→{b or "∅"} | {ctx}')
        continue
    old=' '.join(w for w,_ in TP[i1:i2]); new=' '.join(w for w,_ in TN[j1:j2])
    pre=' '.join(w for w,_ in TN[max(0,j1-6):j1]); post=' '.join(w for w,_ in TN[j2:j2+6])
    W.append((op,old,new,pre,post,TN[j1][1] if j1<len(TN) else len(N)))
# our items: kept / undone / changed
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
st=collections.Counter(); undone=[]
for it in R:
    if it.get('kind') not in ('applied','auto'): continue
    inP=len(re.findall(flex(it['cur']),P))==1
    if not inP: st['not in posted']+=1; continue
    c=len(re.findall(flex(it['cur']),N)); a=len(re.findall(flex(it['alt']),N))
    if c: st['kept']+=1
    elif a: st['undone']+=1; undone.append(it)
    else: st['changed further']+=1
with open(out,'w',encoding='utf-8') as f:
    f.write(f'WORD CHANGES {len(W)}\n')
    for op,old,new,pre,post,pos in W: f.write(f'{op}: «{old}» → «{new}»   …{pre} [{new}] {post}…\n')
    f.write(f'\nPUNCT CHANGES {sum(Pc.values())} {Pc.most_common(12)}\n')
    for l in PL: f.write(l+'\n')
    f.write(f'\nOUR ITEMS {dict(st)}\nUNDONE:\n')
    for it in undone: f.write(f"  {it.get('why','')} | {it['alt']} ⇒ {it['cur']}\n")
print(sys.argv[2],'word changes',len(W),'punct',sum(Pc.values()),dict(st))
