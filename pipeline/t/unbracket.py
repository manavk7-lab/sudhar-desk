"""unbracket.py final.txt doc_orig.txt book_gu.txt[,b2] rows_out.json — commas that came from the Doc's BOOK brackets.
Manav (15 Nov, ઉપનિષદ - 29): "તેઓ, જાગૃતિ, સ્વપ્ન, સુષુપ્તિ ત્રણેય અવસ્થાઓથી પર તુર્યા, ચોથી અવસ્થા, સ્વરૂપ" — the book
prints "તેઓ (જાગૃતિ, સ્વપ્ન તેમજ સુષુપ્તિ) ત્રણેય અવસ્થાઓથી પર તુરીયાવસ્થા (ચોથી અવસ્થા) સ્વરૂપ": the brackets were
turned into commas (backbone_m.py), "so many alpaviram … in the book it is not there … don't add too much".
For every "(…)" in the Doc as it was read whose inside is the book's text (the speaker reads a book bracket), find the
same words in final.txt and drop the comma that stands where "(" or ")" was (only where the Doc had no comma of its
own there). The speaker's own asides in brackets (not in the book) keep their commas.
Writes wordfix rows [old, new, why, conf] (old unique in final.txt); apply with t/wordfix.py."""
import re,sys,json
from rapidfuzz import fuzz
F,D,BK,OUT=sys.argv[1:5]
t=open(F,encoding='utf-8').read()
d=open(D,encoding='utf-8').read().replace('"','').replace('“','').replace('”','')
book=' '.join(open(b,encoding='utf-8').read() for b in BK.split(','))
def nz(s): return re.sub(r'[^઀-૿ ]','',re.sub(r'\s+',' ',s)).strip()
bookn=nz(book)
rows=[];seen=set();stat={'book':0,'aside':0,'nomatch':0,'nocomma':0}
for m in re.finditer(r'(\S+)\s*\(([^()\n]{1,200})\)(\S*)\s*(\S*)',d):
    L,inner,suf,R=m.group(1),m.group(2).strip(),m.group(3),m.group(4)
    if '(' in L or ')' in R: continue
    ni=nz(inner)
    if len(ni)<2: continue
    inbook = ni in bookn or (len(ni)>=6 and fuzz.partial_ratio(ni,bookn,score_cutoff=88)>0)
    # also the bracket with its left word: the book usually prints "L (inner)"
    if not inbook: stat['aside']+=1; continue
    stat['book']+=1
    Lw=re.sub(r'[,]$','',L); Lcomma=L.endswith(',')
    iw=inner.split()
    after_comma = suf.startswith(',') or (suf=='' and R.startswith(','))
    # pattern in final: L[,] inner-words[,]  next   (judges may have changed a word: then no match)
    pat=re.escape(Lw)+r'(,?)(\s+)'+r'\s+'.join(re.escape(w) for w in iw)
    hits=[x for x in re.finditer(pat,t)]
    if len(hits)!=1: stat['nomatch']+=1; continue
    h=hits[0]; s0,e0=h.start(),h.end()
    # the comma right after the inner words (where ")" was)
    tail=t[e0:e0+1]
    new=None; old=t[s0:e0]
    seg=old; changed=False
    if h.group(1)==',' and not Lcomma:
        seg=Lw+h.group(2)+seg[len(Lw)+1+len(h.group(2)):]; changed=True
    e1=e0
    if tail==',' and not after_comma and suf=='' :
        e1=e0+1; old=t[s0:e1]; seg=seg; changed=True
    if not changed: stat['nocomma']+=1; continue
    # widen to make old unique and give a word of context after
    j=t.find(' ',e1+1); j=len(t) if j<0 else j
    nl=t.find('\n',e1)
    if 0<=nl<j: j=nl
    old=t[s0:j]; new=seg+t[e0:j].lstrip(',') if e1>e0 else seg+t[e0:j]
    k=0
    while t.count(old)!=1 and k<5:
        i=t.rfind(' ',0,s0-1); s0=i+1 if i>=0 else 0; old=t[s0:j]; new=t[s0:h.start()]+new; k+=1
    if t.count(old)!=1 or old==new or old in seen: continue
    seen.add(old)
    rows.append([old,new,'no comma where the book has a bracket (Doc: '+L+' ('+inner+')'+suf+')','sure'])
json.dump(rows,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(stat,'rows',len(rows))
for r in rows[:12]: print('  ',repr(r[0]),'->',repr(r[1]))
