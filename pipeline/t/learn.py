import re,sys,difflib,collections,json
L='learn/'
TOK=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
def rd(n): return open(L+n+'.txt',encoding='utf-8-sig').read()
def toks(t): return TOK.findall(t)
def ops(A,B):
    sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
    return sm.get_opcodes()
if __name__=='__main__':
  sub=collections.Counter(); dele=collections.Counter(); ins=collections.Counter(); keep=collections.Counter()
  for v in sys.argv[1:]:
    R=toks(rd('raw'+v)); F=toks(rd('fin'+v))
    st=collections.Counter()
    for op,i1,i2,j1,j2 in ops(R,F):
        if op=='equal':
            st['same']+=i2-i1
            for w in R[i1:i2]: keep[w]+=1
        elif op=='delete': st['del']+=i2-i1; dele[' '.join(R[i1:i2])]+=1
        elif op=='insert': st['ins']+=j2-j1; ins[' '.join(F[j1:j2])]+=1
        else: st['subR']+=i2-i1; st['subF']+=j2-j1; sub[(' '.join(R[i1:i2]),' '.join(F[j1:j2]))]+=1
    print('video',v,'raw',len(R),'final',len(F),dict(st),f"unchanged {st['same']/len(R):.1%}")
  print('\nTOP DELETIONS', dele.most_common(40))
  print('\nTOP INSERTIONS', ins.most_common(40))
  print('\nTOP SUBS', sub.most_common(80))
