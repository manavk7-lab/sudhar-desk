import re,sys,difflib,collections
def toks(s):
    s=re.sub(r'[\[\]().,!?;:"“”‘’\'।…\-–—]',' ',s)
    return s.split()
ins=collections.Counter(); suf=collections.Counter(); ctx=collections.defaultdict(list)
pairs=[(f'learn/raw{i}.txt',f'learn/fin{i}.txt') for i in range(1,7)]+[('now/cor7.txt','live/cor7.txt')]
for a,b in pairs:
    A=toks(open(a,encoding='utf-8').read()); B=toks(open(b,encoding='utf-8').read())
    sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='insert':
            for w in B[j1:j2]:
                ins[w]+=1
                if len(ctx[w])<4: ctx[w].append(' '.join(B[max(0,j1-4):j2+3]))
        elif op=='replace' and i2-i1==j2-j1:
            for x,y in zip(A[i1:i2],B[j1:j2]):
                if y.startswith(x) and len(y)>len(x):
                    s=y[len(x):]; suf[s]+=1
                    if len(ctx['+'+s])<6: ctx['+'+s].append(f'{x}→{y}')
        elif op=='replace' and j2-j1>i2-i1:
            # e.g. raw word merged
            pass
print('INSERTED WORDS (top 30):')
for w,c in ins.most_common(30): print(c,w,'|',ctx[w][:2])
print('\nSUFFIX ADDED (top 15):')
for s,c in suf.most_common(15): print(c,'+'+s,ctx['+'+s][:6])
