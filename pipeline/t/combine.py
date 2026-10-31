import sys,difflib; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wer import TOK,key,FILL,wer
def toks(f): return [w for w in TOK.findall(open(f,encoding='utf-8-sig').read()) if w not in FILL]
def mapto(B,O):
    """for each backbone index: the other system's word (or None if missing)"""
    m=[None]*len(B); kb=[key(x) for x in B]; ko=[key(x) for x in O]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,kb,ko,autojunk=False).get_opcodes():
        if op in('equal','replace') and (op=='equal' or i2-i1==j2-j1):
            for k in range(i2-i1): m[i1+k]=O[j1+k]
    return m
ref,back,*others=sys.argv[1:]
B=toks(back); M=[mapto(B,toks(o)) for o in others]
# vote
out=[]; agree=[]
for i,w in enumerate(B):
    cands=[w]+[m[i] for m in M if m[i]]
    ks=[key(c) for c in cands]
    best=max(set(ks),key=ks.count)
    out.append(next(c for c in cands if key(c)==best))
    agree.append(all(m[i] and key(m[i])==key(w) for m in M))
open('hyp_vote.txt','w',encoding='utf-8').write(' '.join(out))
R=[key(x) for x in toks(ref)]; V=[key(x) for x in out]
# which voted words are wrong vs reference
wrong=[True]*len(V)
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,R,V,autojunk=False).get_opcodes():
    if op=='equal':
        for k in range(j1,j2): wrong[k]=False
a=sum(agree); wa=sum(1 for i in range(len(V)) if agree[i] and wrong[i]); wd=sum(1 for i in range(len(V)) if not agree[i] and wrong[i])
print(f'all engines agree on {a}/{len(V)} words ({a/len(V):.0%}); wrong among those: {wa} ({wa/max(1,a):.1%})')
print(f'disagreement spots: {len(V)-a} words; wrong among those: {wd} ({wd/max(1,len(V)-a):.0%})')
print('voted output WER (ignoring spelling):',f"{wer(open(ref).read(),' '.join(out),True)[0]:.1%}")
runs=0;prev=True
for g in agree:
    if not g and prev: runs+=1
    prev=g
print('review spots (groups of disagreeing words):',runs,'in 15 min')
tot_err=sum(wrong); print('share of all errors that sit in a review spot:',f'{wd/max(1,tot_err):.0%}')
