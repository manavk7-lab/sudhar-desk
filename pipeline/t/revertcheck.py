"""revertcheck.py final.txt items.json doc_orig.txt — undo every applied ✎ item (cur→alt) on final.txt and compare with the
Doc as it was read (quotation marks removed): every change must be on the ✎ list, so this must print 0 unexplained diffs."""
import json,re,sys,difflib
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
t=open(sys.argv[1],encoding='utf-8').read(); I=json.load(open(sys.argv[2],encoding='utf-8'))
pos=[]
for it in I:
    m=list(re.finditer(flex(it['cur']),t))
    if len(m)!=1: print('item not found once:',it['cur'][:60]); continue
    pos.append((m[0].start(),m[0].end(),it))
pos.sort(key=lambda x:-x[0]); r=t
for s,e,it in pos:
    if it.get('kind')!='check': r=r[:s]+it['alt']+r[e:]
o=re.sub(r'["“”]','',open(sys.argv[3],encoding='utf-8').read())
A=re.sub(r'\s+',' ',o).split(); B=re.sub(r'\s+',' ',r).split()
d=[(op,' '.join(A[i1:i2]),' '.join(B[j1:j2])) for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,B,autojunk=False).get_opcodes() if op!='equal']
print('words',len(A),len(B),'unexplained diffs',len(d))
for x in d[:40]: print('  ',x)
