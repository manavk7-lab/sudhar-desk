"""bookalign.py doc.txt out.json book1.txt[,book2.txt] [min_score]
Manav (1 Nov): where the speaker reads the book's Gujarati translation, write what the book says (incl. its brackets).
For every book clause found in the Doc (fuzzy, score >= min_score, default 80) the words are aligned; each place where the
Doc has DIFFERENT words than the book (a substitution) becomes a candidate {alt, cur, book, score}. Words the speaker adds
(Doc only) are kept; book words he skipped are listed as 'skip' candidates for review, not applied.
Differences that are only spacing of જ / punctuation are ignored."""
import re,sys,json,difflib
from rapidfuzz import fuzz
doc=open(sys.argv[1],encoding='utf-8').read(); out=sys.argv[2]; books=sys.argv[3].split(','); MIN=float(sys.argv[4]) if len(sys.argv)>4 else 80
raw='\n'.join(open(b,encoding='utf-8').read() for b in books)
lines=[l.strip() for l in raw.split('\n') if sum(1 for c in l if '઀'<=c<='૿')>max(5,3*sum(1 for c in l if 'ऀ'<=c<='ॿ'))]
gu=re.sub(r'\s+',' ',' '.join(lines))
# keep brackets (Manav keeps the book's brackets); split into clauses
cl=[c.strip(' |-—') for c in re.split(r'(?<=[,.।;?!॥])\s+',gu) if len(re.findall(r'[઀-૿]+',c))>=4]
W=[(m.start(),m.end(),m.group()) for m in re.finditer(r'\S+',doc)]
def norm(w): return re.sub(r'[^઀-૿A-Za-z0-9]','',w).replace('જ','') if False else re.sub(r'[^઀-૿A-Za-z0-9]','',w)
cands=[];seen=set()
for c in cl:
    a=fuzz.partial_ratio_alignment(c,doc,score_cutoff=MIN)
    if not a: continue
    # doc words overlapping the aligned span
    di=[i for i,(s,e,w) in enumerate(W) if e>a.dest_start and s<a.dest_end]
    if not di: continue
    dw=[W[i][2] for i in di]; bw=c.split()
    dn=[norm(w) for w in dw]; bn=[norm(w) for w in bw]
    sm=difflib.SequenceMatcher(None,dn,bn,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        dtxt=''.join(dn[i1:i2]); btxt=''.join(bn[j1:j2])
        if dtxt.replace('જ','')==btxt.replace('જ','') and dtxt and btxt: continue      # only જ joined/split
        if op=='insert' and i1 in (0,len(dn)): continue                                # edge of the window
        if op=='delete' and (i1==0 or i2==len(dn)): continue
        s0=W[di[i1]][0] if i1<len(di) else W[di[-1]][1]
        e0=W[di[i2-1]][1] if i2>i1 else s0
        k=(s0,e0,btxt)
        if k in seen: continue
        seen.add(k)
        kind={'replace':'sub','delete':'extra','insert':'skip'}[op]
        cands.append({'kind':kind,'pos':s0,'end':e0,'doc':doc[s0:e0],'book':' '.join(bw[j1:j2]),
                      'ctx':doc[max(0,s0-60):s0]+'⟪'+doc[s0:e0]+'⟫'+doc[e0:e0+60],'clause':c,'score':round(a.score)})
cands.sort(key=lambda x:x['pos'])
json.dump(cands,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
import collections; print('clauses',len(cl),'candidates',len(cands),collections.Counter(c['kind'] for c in cands))
