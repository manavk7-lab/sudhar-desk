"""mergeov.py out.txt A.txt B.txt C.txt — join transcripts of overlapping recordings by matching the overlap words"""
import sys,difflib,re
sys.path.insert(0,'t')
from fuse import key
out=sys.argv[1]; parts=[open(p,encoding='utf-8-sig').read().split() for p in sys.argv[2:]]
W=parts[0]
for B in parts[1:]:
    tailn=min(len(W),250); headn=min(len(B),250)
    ta=[key(re.sub(r'[^\w઀-૿]','',x)) for x in W[-tailn:]]; hb=[key(re.sub(r'[^\w઀-૿]','',x)) for x in B[:headn]]
    sm=difflib.SequenceMatcher(None,ta,hb,autojunk=False); m=sm.find_longest_match(0,tailn,0,headn)
    print('overlap match',m.size,'words; cut A at',len(W)-tailn+m.a,'B from',m.b)
    if m.size<4: print('WARNING weak overlap'); W=W+B; continue
    W=W[:len(W)-tailn+m.a]+B[m.b:]
open(out,'w',encoding='utf-8').write(' '.join(W)); print(out,len(W),'words')
