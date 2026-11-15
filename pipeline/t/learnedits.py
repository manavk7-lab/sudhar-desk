"""learnedits.py mine.txt manav.txt book_gu.txt [out.json]
What did Manav change in a Doc I posted (mine = my posted text, manav = his finished Doc), and does the book explain it?
- Punctuation after a word (or a dash between words) that he changed, with the book's mark at that place when the
  passage is read from the book (a run of >= 5 words matching the book).
- Words he changed, and whether his word is the book's word.
- In read passages: every boundary where my mark differs from the book's, and what he did there (took the book's
  mark / kept mine / something else).
Prints counts and examples; writes all rows to out.json."""
import re,sys,json,difflib,collections
M,H,BK=sys.argv[1:4]; OUT=sys.argv[4] if len(sys.argv)>4 else None
PUN='.,?!;:–—-।॥'
def gu_lines(t):
    return '\n'.join(l for l in t.split('\n') if sum(1 for c in l if '઀'<=c<='૿')>=max(5,3*sum(1 for c in l if 'ऀ'<=c<='ॿ')))
def seq(t):
    """[(core, mark_after, para_after)] — mark_after is the punctuation after the word (dash tokens included)."""
    out=[]
    for tok in re.finditer(r'\S+|\n\s*\n',t):
        w=tok.group()
        if '\n' in w:
            if out: out[-1][2]=True
            continue
        core=w.strip(PUN+'‘’“”"\'()[]')
        lead=w[:len(w)-len(w.lstrip(PUN+'‘’“”"\'()[]'))]
        trail=w[len(w.rstrip(PUN+'‘’“”"\'()[]')):]
        if not core:   # a lone dash / mark
            if out: out[-1][1]+=w.strip('‘’“”"\'()[]')
            continue
        if lead.strip('‘’“”"\'()[]') and out: out[-1][1]+=lead.strip('‘’“”"\'()[]')
        out.append([core,''.join(c for c in trail if c in PUN),False])
    return out
def norm(w):
    w=re.sub(r'[^઀-૿A-Za-z0-9]','',w)
    for a,b in (('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ં',''),('ઃ',''),('્',''),('ૃ','ુ'),('ણ','ન'),('ષ','શ'),('સ','શ'),('ળ','લ')): w=w.replace(a,b)
    return w
def mk(p):  # canonical mark: the strongest one
    for c in '?!।॥.;:,':
        if c in p: return {'।':'.','॥':'.'}.get(c,c)
    return '–' if any(c in p for c in '–—-') else ''
m=seq(open(M,encoding='utf-8').read()); h=seq(open(H,encoding='utf-8').read())
b=seq(gu_lines(open(BK,encoding='utf-8').read()))
# book alignment of Manav's text: book mark for each of his words (only inside runs of >= 5 matching words)
hn=[norm(x[0]) for x in h]; bn=[norm(x[0]) for x in b]
bookmark={}; bookword={}
sm=difflib.SequenceMatcher(None,hn,bn,autojunk=False)
for a,bb,n in sm.get_matching_blocks():
    if n>=5:
        for k in range(n):
            bookword[a+k]=b[bb+k][0]
            if k<n-1: bookmark[a+k]=mk(b[bb+k][1])
# mine vs his
mn=[norm(x[0]) for x in m]
sm2=difflib.SequenceMatcher(None,mn,hn,autojunk=False)
rows=[]; C=collections.Counter()
def ctx(seqq,i,r=4): return ' '.join(x[0]+x[1] for x in seqq[max(0,i-r):i+r+1])
for op,i1,i2,j1,j2 in sm2.get_opcodes():
    if op=='equal':
        for k in range(i2-i1):
            i,j=i1+k,j1+k
            pm,ph=mk(m[i][1]),mk(h[j][1])
            if m[i][0]!=h[j][0]:
                inbook=j in bookword; bw=bookword.get(j)
                rows.append({'type':'spell','mine':m[i][0],'his':h[j][0],'book':bw,'ctx':ctx(h,j)})
                C['spell']+=1; C['spell_his=book']+= (bw==h[j][0]); C['spell_inbook']+=inbook
            if j in bookmark:
                bkm=bookmark[j]
                if pm!=bkm:
                    C['rd_mine!=book']+=1
                    if ph==bkm: C['rd_he_took_book']+=1; res='took book'
                    elif ph==pm: C['rd_he_kept_mine']+=1; res='kept mine'
                    else: C['rd_other']+=1; res='other'
                    rows.append({'type':'readmark','mine':pm,'his':ph,'book':bkm,'res':res,'ctx':ctx(h,j)})
                else:
                    C['rd_mine=book']+=1
                    if ph!=pm: C['rd_he_left_book']+=1; rows.append({'type':'readmark','mine':pm,'his':ph,'book':bkm,'res':'left book','ctx':ctx(h,j)})
            if pm!=ph:
                C['mark_changes']+=1; C[f'mark {pm or "∅"}→{ph or "∅"}']+=1
                if j in bookmark: C['mark_changes_in_read']+=1; C['mark_changes_his=book']+= (ph==bookmark[j])
                rows.append({'type':'mark','mine':pm,'his':ph,'book':bookmark.get(j),'ctx':ctx(h,j)})
    else:
        C['word_'+op]+=1
        rows.append({'type':'word','op':op,'mine':' '.join(x[0] for x in m[i1:i2]),'his':' '.join(x[0] for x in h[j1:j2]),
                     'book':' '.join(bookword.get(j,'') for j in range(j1,j2)).strip() or None,'ctx':ctx(h,j1)})
print(M, 'words', len(m), len(h), 'book-matched words of his', len(bookword))
for k,v in sorted(C.items(),key=lambda x:-x[1]): print(f'  {k}: {v}')
if OUT: json.dump(rows,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
