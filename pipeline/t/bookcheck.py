"""bookcheck.py book_ocr.txt doc.txt sar.txt out.txt [start-marker] — put the book next to the Doc where the speaker reads it.
Takes the book's Gujarati lines (Devanagari verse lines dropped), splits them into clauses, finds each clause in the Doc
and in Sarvam's text (fuzzy, rapidfuzz), and writes the word differences  B (book) / D (Doc) / S (Sarvam)  for review.
How to read it (video 39): where D = S but differs from B, the speaker said it his own way — keep D. Fix only where
S agrees with B against D (a mishearing), or where D garbles a name or term the book spells (અંતર્જ્ઞાન, અખંડાકાર)."""
import re,sys,difflib
from rapidfuzz import fuzz
bk,dc,sr,out=sys.argv[1:5]; mark=sys.argv[5] if len(sys.argv)>5 else None
raw=open(bk,encoding='utf-8').read()
if mark and mark in raw: raw=raw[raw.find(mark):]
lines=[l.strip() for l in raw.split('\n') if sum(1 for c in l if '઀'<=c<='૿')>max(5,sum(1 for c in l if 'ऀ'<=c<='ॿ'))]
gu=re.sub(r'\([^)]*\)','',re.sub(r'\s+',' ',' '.join(lines)))
cl=[c.strip(' |') for c in re.split(r'[,.।;?!॥]+',gu) if len(c.split())>=5]
dn=re.sub(r'\s+',' ',open(dc,encoding='utf-8').read()); sar=re.sub(r'\s+',' ',open(sr,encoding='utf-8').read())
T=lambda s:re.findall(r'[઀-૿‌‍]+',s)
res=[]
for c in cl:
    a=fuzz.partial_ratio_alignment(c,dn,score_cutoff=60)
    if not a: continue
    d=dn[a.dest_start:a.dest_end]; b=fuzz.partial_ratio_alignment(c,sar,score_cutoff=55); s=sar[b.dest_start:b.dest_end] if b else ''
    sm=difflib.SequenceMatcher(None,T(c),T(d)); bt,dt=T(c),T(d)
    df=[(' '.join(bt[i1:i2]),' '.join(dt[j1:j2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
    if df: res.append((a.dest_start,round(a.score),c,d,s,df))
res.sort()
with open(out,'w',encoding='utf-8') as f:
    for k,(p,sc,c,d,s,df) in enumerate(res): f.write(f"b{k} @{p} {sc}\n  B: {c}\n  D: {d}\n  S: {s}\n  diff: {df}\n")
print('book clauses',len(cl),'found in the Doc with differences',len(res),'->',out)
