"""bookbrackets.py text.txt book_gu.txt[,b2] rows_out.json [--report] — put the BOOK's brackets back where he reads them.
Manav (16 Nov, ઉપનિષદ - 34: "you used to forget ( ) while checking from books"; RULES.md since 1 Nov): book
"હંસ (ચેતન જીવ) હંમેશાં" → transcript "હંસ (ચેતન જીવ) હંમેશા", not "હંસ, ચેતન જીવ," or "હંસ ચેતન જીવ".
Manav (19 Nov, ઉપનિષદ - 43: "still ( ) is missed … this type of mistakes not happen again"): the book prints
"જે (પુરુષ) સંન્યાસ-આશ્રમને … એવા (પુરુષ)ને આરૂઢચ્યુત (પાતકી-પાપી) સમજવો … અનુશાસન (આદેશ) છે.॥૩૧॥" and the first
version (exact words only) found none of them: his spelling (સન્યાસ), a bracket glued to a word ("(પુરુષ)ને"), a hyphen
inside ("પાતકી-પાપી"), and a verse number after the bracket all stopped the match.
Now: words are compared spelling-blind (anusvara, halant, long/short vowel signs) and fuzzy for long words; hyphens
split words; a glued ending is matched on the text's word; the word after may be a verse number / sentence end.
A row needs the book's word before the bracket, every word inside, and the word after (or a sentence end) in the
text in that order — so where he says એટલે / એટલે કે before the inside (explains, not reads) nothing is bracketed.
Inside the bracket and at its edges the book's punctuation is used (its hyphen, its comma); the words stay his.
Writes wordfix rows [old, new, why, conf] (old unique in the text) → t/wordfix1.py. --report prints the rows and
the "one side only" places to look at by hand."""
import re,sys,json
from rapidfuzz import fuzz
T,BK,OUT=sys.argv[1:4]; REP='--report' in sys.argv
t=open(T,encoding='utf-8').read()
W=r'[઀-૯A-Za-z0-9]+'          # a word: Gujarati letters/digits (not ૰ ૱), split at spaces, commas, hyphens, dandas
STOP={'કે','આ','એ','તે','જે','જ','પણ','અને','તથા','તો','છે','હું','એવો','એવી','એવું','અર્થાત્','એટલે','કેમકે','પરંતુ'}
def key(w): return re.sub(r'[ંઁ઼્ઃ]','',w).translate(str.maketrans('ીૂૈૌૃ','િુેોિ'))
def eq(a,b,cut=80):
    if not a or not b: return False
    ka,kb=key(a),key(b)
    return ka==kb or (min(len(ka),len(kb))>=4 and fuzz.ratio(ka,kb)>=cut)
def isnum(w): return bool(re.fullmatch(r'[૦-૯0-9]+',w))
TT=[(m.start(),m.end(),m.group()) for m in re.finditer(W,t)]
CTX=int(([a.split('=')[1] for a in sys.argv if a.startswith('--ctx=')] or ['70'])[0])
rows=[];maybe=[];used=set();stat={'book':0,'rows':0,'have':0,'one_side':0,'notunique':0}
def sep_of(s):          # book punctuation between two words → what to write
    s=s.strip()
    if re.search(r'[^\s,\-–—.;:।॥\'’‘“”"]',s): return ' '      # OCR noise / other script between: no comma from it
    if '-' in s: return '-'
    if ',' in s: return ', '
    return ' '
import bisect
# the book files keep the OCR's line breaks (mid-sentence), so join everything; "((" and ".(" at a line start are OCR noise
_bk=' '.join(open(b,encoding='utf-8').read() for b in BK.split(','))
_bk=re.sub(r'\s+',' ',_bk); _bk=re.sub(r'\(+','(',_bk); _bk=re.sub(r'\.\(','(',_bk)
for para in [_bk]:
    BT=[(m.start(),m.end(),m.group()) for m in re.finditer(W,para)]; BS=[x[0] for x in BT]
    for m in re.finditer(r'\(([^()]{1,120})\)',para):
        o,c=m.start(),m.end()
        lo=bisect.bisect_left(BS,o); hi=bisect.bisect_left(BS,c)
        ins=BT[lo:hi]
        if not ins or not re.search(r'[઀-૿]',m.group(1)): continue
        inner=[x[2] for x in ins]
        if ' '.join(inner) in STOP or sum(len(w) for w in inner)<3: continue
        stat['book']+=1
        bef=BT[max(0,lo-8):lo]; aft=BT[hi:hi+4]
        if not bef: continue
        Lb=bef[-1]
        if re.search(r'[.?!।॥]',para[Lb[1]:o]): continue           # bracket opens a sentence: no word before to anchor
        glue=aft[0][2] if aft and aft[0][0]==c else ''              # "(પુરુષ)ને"
        Rb=(aft[1] if glue else aft[0]) if aft and (len(aft)>1 or not glue) else None
        Rend = Rb is None or isnum(Rb[2]) or bool(re.search(r'[.?!।॥]',para[(aft[0][1] if glue else c):(Rb[0] if Rb else len(para))]))
        k=len(inner)
        for i in range(1,len(TT)-k+1):
            if i in used: continue
            last=TT[i+k-1][2]
            if not all(eq(TT[i+j][2],inner[j],86) for j in range(k-1)): continue
            if glue:
                if not ((eq(last,inner[-1]+glue,86) or eq(last,inner[-1],86)) and len(last)>len(glue)): continue
            elif not eq(last,inner[-1],86): continue
            if not eq(TT[i-1][2],Lb[2]): continue
            gapL=t[TT[i-1][1]:TT[i][0]]
            if re.search(r'[.?!।\n(]',gapL): continue
            span=t[TT[i][0]:TT[i+k-1][1]]
            if re.search(r'[.?!\n()]',span): continue
            nx=TT[i+k] if i+k<len(TT) else None
            gapR=t[TT[i+k-1][1]:nx[0]] if nx else t[TT[i+k-1][1]:]
            if ')' in gapR: stat['have']+=1; continue
            endR=bool(re.search(r'[.?!]',gapR)) or nx is None
            okR = (Rb is not None and nx is not None and not endR and (eq(nx[2],Rb[2]) or (len(nx[2])>=3 and key(nx[2])[:3]==key(Rb[2])[:3]))) or (Rend and endR)
            bc=' '.join(x[2] for x in bef[-6:]+ins+aft[:3]); tc=' '.join(x[2] for x in TT[max(0,i-6):i+k+3])
            sc=fuzz.ratio(key(bc),key(tc))
            if not okR and sc<CTX:
                stat['one_side']+=1; maybe.append([m.group(0),t[TT[max(0,i-4)][0]:(nx[1] if nx else TT[i+k-1][1])],sc]); continue
            # build: his words, the book's punctuation inside and at the edges
            parts=[TT[i+j][2] for j in range(k)]
            if glue:
                cut=[q for q in range(len(last)-1,0,-1) if key(last[q:])==key(glue)]
                q=cut[0] if cut and eq(last[:cut[0]],inner[-1],86) else len(last)   # his ending differs: bracket his whole word
                parts[-1]=last[:q]; tail=last[q:]
            else: tail=''
            inside=parts[0]
            for j in range(1,k): inside+=sep_of(para[ins[j-1][1]:ins[j][0]])+parts[j]
            sl=sep_of(para[Lb[1]:o]); sl=' ' if sl=='-' else sl
            a=TT[i-1][0]
            if endR: b=TT[i+k-1][1]; after=''
            else:
                b=nx[1]; sr=sep_of(para[(aft[0][1] if glue else c):Rb[0]]) if Rb else ' '
                if glue and not tail: sr=' '      # book "(આત્મા)જ," but he says "આત્મા જ": his next word is the book's ending
                g=gapR.replace(',','').replace('–','').replace('-','')     # keep the text's own "(" etc., drop its comma/dash
                g=re.sub(r'\s+',' ',g) if g.strip() else ''
                after=(', ' if sr==', ' else ' ')+g.strip()+nx[2]
            new=TT[i-1][2]+sl+'('+inside+')'+tail+after
            old=t[a:b]
            # unique context: widen left by whole words
            lw=i-1
            while t.count(old)>1 and lw>0:
                lw-=1; a=TT[lw][0]; new=t[a:TT[i-1][0]]+TT[i-1][2]+sl+'('+inside+')'+tail+after; old=t[a:b]
            if t.count(old)!=1: stat['notunique']+=1; continue
            if old==new: continue
            used.add(i); stat['rows']+=1
            rows.append([old,new,('[ctx %d] '%sc)+'book bracket as printed: '+para[max(0,Lb[0]):min(len(para),c+20)].strip(),'sure'])
            break
json.dump(rows,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(stat)
for r in (rows if REP else rows[:6]): print('   ',r[0],' → ',r[1])
if REP:
    for x in maybe: print('  ? book',x[0],'| text:',x[1],'| ctx',x[2])
