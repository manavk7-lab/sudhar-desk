"""bookpunct.py text.txt book_gu.txt[,book2_gu.txt] items.json sync.tsv [--dry]
Manav (15 Nov): where the speaker reads the book, the punctuation must be the book's — its અલ્પવિરામ, ?, !, ;, –, :
and its stops — and the book's visarga spellings (અંતઃમાં). Run on final.txt after the punctuation pass.

How: the Doc's words are aligned with the book's Gujarati words (spelling-normalised; OCR-damaged words matched
fuzzily). Inside a run of >= MINRUN aligned words (a passage he reads), at every word boundary where both neighbours
are aligned, the Doc's mark is replaced by the book's mark. Brackets in the book count as commas (no brackets in
transcripts). Boundaries at a paragraph break are changed only to a stop (. ? !). Each change is a ✎ item
("punctuation as in the book"); a change inside an existing item updates that item (no overlaps).
--dry: print what would change, write nothing."""
import re,sys,json,difflib,hashlib,os,subprocess
from rapidfuzz import fuzz
T,BKS,I,SY=sys.argv[1:5]; DRY='--dry' in sys.argv; MINRUN=6; UNDOBR='--undo-brackets' in sys.argv
PUN='.,?!;:–—-।॥'
QB='‘’“”"\''
def gu_lines(t):
    return '\n'.join(l for l in t.split('\n') if sum(1 for c in l if '઀'<=c<='૿')>=max(5,3*sum(1 for c in l if 'ऀ'<=c<='ॿ')))
def toks(t):
    """word tokens with spans: [(start,end,core,core_start,core_end)]; core = word without marks/quotes/brackets."""
    out=[]
    for m in re.finditer(r'\S+',t):
        w=m.group(); s=m.start()
        cs=len(w)-len(w.lstrip(PUN+QB+'()[]')); ce=len(w.rstrip(PUN+QB+'()[]'))
        if ce<=cs: continue
        out.append((s,m.end(),w[cs:ce],s+cs,s+ce))
    return out
def bmark(seg,br=False):
    """the book's mark between two words, from the raw text between them.
    Brackets are NOT marks (Manav, 15 Nov, ઉપનિષદ - 29: "એ જ (બ્રહ્મ પ્રાપ્તિનો) માર્ગ" is read as one sentence — he
    removed the commas the old rule put there). br=True is the old rule, used only by --undo-brackets."""
    seg=seg.replace('(',',' if br else ' ').replace(')',',' if br else ' ')
    for c in '?!':
        if c in seg: return c
    if any(c in seg for c in '.।॥'): return '.'
    for c in ';:':
        if c in seg: return c
    if any(c in seg for c in '–—') or re.search(r'\s-|-\s',seg): return '–'
    if ',' in seg: return ','
    return ''
def norm(w):
    w=re.sub(r'[^઀-૿A-Za-z0-9]','',w)
    for a,b in (('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ં',''),('ઃ',''),('્',''),('ૃ','ુ'),('ણ','ન'),('ષ','શ'),('સ','શ'),('ળ','લ'),('ઁ','')): w=w.replace(a,b)
    return w
t=open(T,encoding='utf-8').read()
book=re.sub(r'[ \t]+',' ',gu_lines('\n'.join(open(b,encoding='utf-8').read() for b in BKS.split(','))))
D=toks(t); Bk=toks(book)
dn=[norm(x[2]) for x in D]; bn=[norm(x[2]) for x in Bk]
pair={}
sm=difflib.SequenceMatcher(None,dn,bn,autojunk=False)
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='equal':
        for k in range(i2-i1): pair[i1+k]=j1+k
    elif op=='replace' and i2-i1==j2-j1:
        for k in range(i2-i1):
            if len(dn[i1+k])>=3 and fuzz.ratio(dn[i1+k],bn[j1+k])>=75: pair[i1+k]=j1+k
# runs of consecutive aligned words (book index also consecutive)
runs=[]; cur=[]
for i in range(len(D)):
    if i in pair and cur and cur[-1]+1==i and pair[cur[-1]]+1==pair[i]: cur.append(i)
    else:
        if len(cur)>=MINRUN: runs.append(cur)
        cur=[i] if i in pair else []
if len(cur)>=MINRUN: runs.append(cur)
AUX={'છે','છું','છો','છીએ','હતો','હતી','હતું','હતા','હશે','હોય','જ'}
QW=re.compile(r'(^|\s)(શું|શા|કેમ|કેવી|કેવો|કેવું|કેવા|ક્યાં|ક્યારે|કોણ|કોને|કોનો|કોની|કોનું|કયો|કયું|કયા|કઈ|કઇ|કેટલા|કેટલું|કેટલી|ખરો|ખરું|ખરી|ને)(\s|$)')
changes=[]   # (start,end,newtext,why)
if UNDOBR:
    # remove the commas the old rule copied from book brackets — only where a "punctuation as in the book" item made them
    it=json.load(open(I,encoding='utf-8'))
    def span(x,txt):
        p=txt.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 and txt.count(x['cur'])==1 else None
    undo=[]
    for r in runs:
        for a_,b_ in zip(r,r[1:]):
            gap=t[D[a_][4]:D[b_][3]]; bgap=book[Bk[pair[a_]][4]:Bk[pair[b_]][3]].replace('\n',' ')
            if '\n' in gap or bmark(gap)!=',' or bmark(bgap,True)!=',' or bmark(bgap)!='': continue
            undo.append((D[a_][4],D[b_][3]))
    n=0
    for s0,e0 in sorted(undo,reverse=True):
        host=next((x for x in it if span(x,t) and span(x,t)[0]<=s0 and span(x,t)[1]>=e0 and 'punctuation as in the book' in x.get('why','')),None)
        if not host: continue
        hs,he=span(host,t)
        t=t[:s0]+' '+t[e0:]
        host['cur']=t[hs:he-(e0-s0-1)]
        n+=1; print('undo comma:',repr(host['cur'][:70]))
    it=[x for x in it if x['cur']!=x['alt']]
    if not DRY:
        open(T,'w',encoding='utf-8').write(t); json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('commas from brackets removed',n,'items',len(it)); sys.exit()
for r in runs:
    for a,b in zip(r,r[1:]):
        gap=t[D[a][4]:D[b][3]]          # Doc text between the two cores
        bgap=book[Bk[pair[a]][4]:Bk[pair[b]][3]]
        if '\n' in bgap: bgap=bgap.replace('\n',' ')
        if '?' in bgap and '.' in bgap: bgap=bgap.replace('?','')   # OCR noise like "જાણો.?"
        dm=bmark(gap.replace('\n',' ')); bm=bmark(bgap)
        para='\n' in gap
        if dm==bm or para: continue              # paragraph ends stay as they are
        # only ADD or CHANGE a mark: the OCR often loses a mark, so "book has none" is no evidence
        if bm=='': continue
        if dm and dm in '?!': continue           # his own question / exclamation stays
        # stops come from where he really stops (the pause pass); a book '.' with no mark in the Doc is mostly a
        # verse number or an OCR slip
        if bm=='.': continue
        # a book colon / dash only where the Doc already has some mark (otherwise it is a hyphenated compound or OCR)
        if bm in ':–' and not dm: continue
        if bm=='!' and dm!=',': continue         # હે મહર્ષિ, → હે મહર્ષિ!
        # never a comma between a verb and its auxiliary (OCR / alignment slips)
        if D[b][2] in AUX: continue
        # a question mark only where the Doc's sentence asks something
        if bm=='?':
            sst=max(t.rfind(c,0,D[a][3]) for c in '.?!\n')
            if not QW.search(t[sst+1:D[a][4]]): continue
        new={',':', ', '.':'. ', '?':'? ', '!':'! ', ';':'; ', ':':': ', '–':' – '}[bm]
        if para: new=bm+'\n\n'
        changes.append((D[a][4],D[b][3],new,f'book: {bm or "no mark"} (Doc: {dm or "no mark"})'))
    # visarga: the book writes ઃ inside a word the Doc writes without it (અંતઃમાં)
    for i in r:
        dw,bw=D[i][2],Bk[pair[i]][2]
        if 'ઃ' in bw and 'ઃ' not in dw and dw==bw.replace('ઃ',''):
            # inside a word (અંતઃમાં, દુઃખ) always; at the end of a word only in a list (ભૂઃ, ભુવઃ) — a final ઃ in
            # prose is usually the OCR of a colon
            j=pair[i]
            if not bw.endswith('ઃ') or ',' in book[Bk[j][4]:Bk[j+1][3] if j+1<len(Bk) else None] or (j>0 and ',' in book[Bk[j-1][4]:Bk[j][3]]):
                changes.append((D[i][3],D[i][4],bw,'visarga as in the book'))
changes.sort()
print(f'runs {len(runs)} words in runs {sum(len(r) for r in runs)} of {len(D)}; changes {len(changes)}')
from collections import Counter
print(Counter(c[3] for c in changes).most_common(12))
for s,e,new,why in changes[:400] if DRY else []:
    print(f'  {why:34} | {t[max(0,s-40):s]}⟦{t[s:e]}→{new.strip() or "␣"}⟧{t[e:e+30]}'.replace('\n','¶'))
if DRY: sys.exit()
# apply from the end, building items
it=json.load(open(I,encoding='utf-8'))
def span(x,txt):
    p=txt.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 and txt.count(x['cur'])==1 else None
new_items=[]
for s,e,new,why in sorted(changes,reverse=True):
    host=None
    for x in it+new_items:
        sp=span(x,t)
        if sp and sp[0]<e and sp[1]>s: host=(sp,x); break
    if host:
        (hs,he),x=host
        x['cur']=t[hs:s]+new+t[e:he]; x['why']=(x.get('why','')+'; punctuation as in the book').strip('; ')
        t=t[:s]+new+t[e:]
        continue
    # two words of context each side, not across a paragraph break
    L=s
    for _ in range(2):
        j=t.rfind(' ',0,L-1); nl=t.rfind('\n',0,L-1)
        if nl>j: L=nl+1; break
        L=j+1 if j>=0 else 0
    R=e
    for _ in range(2):
        j=t.find(' ',R+1); nl=t.find('\n',R+1)
        if j<0: j=len(t)
        if 0<=nl<j: R=nl; break
        R=j
    # if the context touches other items, fold them all into one item (so no two items overlap)
    touch=sorted([(sp,x) for x in it+new_items for sp in [span(x,t)] if sp and sp[0]<R and sp[1]>L],key=lambda q:q[0][0])
    if touch:
        Us=min(L,touch[0][0][0]); Ue=max(R,max(q[0][1] for q in touch))
        alt=''; pos=Us
        for (hs,he),x in touch: alt+=t[pos:hs]+x['alt']; pos=he
        alt+=t[pos:Ue]
        d=len(new)-(e-s)
        t=t[:s]+new+t[e:]
        host=touch[0][1]
        host['cur']=t[Us:Ue+d]; host['alt']=alt
        host['why']=' ; '.join([q[1].get('why','') for q in touch]+['punctuation as in the book — '+why])
        drop={id(q[1]) for q in touch[1:]}
        it=[x for x in it if id(x) not in drop]; new_items=[x for x in new_items if id(x) not in drop]
        continue
    alt=t[L:R]; cur=t[L:s]+new+t[e:R]
    t=t[:s]+new+t[e:]
    x={'id':hashlib.md5(('bp'+cur+str(s)).encode()).hexdigest()[:8],'cur':cur,'alt':alt,'kind':'applied','conf':'likely','why':'punctuation as in the book — '+why,'heard':''}
    new_items.append(x)
t=re.sub(r'  +',' ',t)
for x in new_items: x['cur']=re.sub(r'  +',' ',x['cur'])
bad=[x['cur'] for x in new_items if t.count(x['cur'])!=1]
if bad: print('NOT UNIQUE (widen by hand):',bad[:5])
open(T,'w',encoding='utf-8').write(t)
tmp=I+'.bp.json'; json.dump(new_items,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run(['python3',os.path.join(os.path.dirname(os.path.abspath(__file__)),'addtimes.py'),T,SY,tmp],check=True)
it+=json.load(open(tmp,encoding='utf-8')); os.remove(tmp)
json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('items',len(it),'new',len(new_items))
