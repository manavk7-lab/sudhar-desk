"""bookref.py items_kept.json book_gu.txt[,book2_gu.txt] out.json — add the book's matching sentence (B) to each judge item.
B is info only: the speaker reads the book's Gujarati translation, often word for word."""
import sys,json,re
from rapidfuzz import fuzz
items=json.load(open(sys.argv[1],encoding='utf-8'))
book='\n'.join(open(f,encoding='utf-8').read() for f in sys.argv[2].split(','))
MAP={'ી':'િ','ૂ':'ુ','ઈ':'ઇ','ઊ':'ઉ','ષ':'સ','શ':'સ','ણ':'ન','ળ':'લ','ૃ':'ર','ઋ':'ર','ં':'મ','ઁ':'મ','ૅ':'ે','ૉ':'ો'}
DROP=set('્ઃ઼ઽ')
def norm(s):
    out=[];idx=[]
    for i,c in enumerate(s):
        if c in DROP: continue
        if not ('઀'<=c<='૿') or c in '૦૧૨૩૪૫૬૭૮૯': continue
        out.append(MAP.get(c,c)); idx.append(i)
    return ''.join(out),idx
BN,BI=norm(book)
n=0
for it in items:
    ctx=it['ctx'].replace('⟪','').replace('⟫','')
    cn,_=norm(ctx)
    if len(cn)<25: continue
    r=fuzz.partial_ratio_alignment(cn,BN,score_cutoff=72)
    if not r: continue
    a=BI[r.dest_start]; b=BI[max(r.dest_start,r.dest_end-1)]+1
    while a>0 and not book[a-1].isspace(): a-=1
    while b<len(book) and not book[b].isspace(): b+=1
    snip=re.sub(r'\s+',' ',book[a:b]).strip()
    it['read']['B']=snip; it['bscore']=round(r.score); n+=1
json.dump(items,open(sys.argv[3],'w',encoding='utf-8'),ensure_ascii=False)
print('book matches',n,'of',len(items))
