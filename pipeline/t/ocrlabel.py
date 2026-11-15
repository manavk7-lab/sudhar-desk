"""ocrlabel.py OCRDIR FIRST LAST OFFSET out.txt — label OCR page lines [S] (Devanagari) / [G] (Gujarati) for t/bookbuild.py.
Pages OCRDIR/tFIRST.txt .. tLAST.txt; OFFSET = file number minus printed page number (ocr3: 13). Strips the margin junk
(| ` _ ' and leading । , .), keeps a line's final full stop, drops running heads (page number + title) and short scraps.
Fix obvious OCR misreads by hand afterwards (they only matter as reference text and for book punctuation)."""
import re,sys
D,a,b,off,OUT=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
out=[]
for p in range(a,b+1):
    out.append(f'=== p{p-off} (OCR)')
    for i,l in enumerate(open(f'{D}/t{p}.txt',encoding='utf-8').read().splitlines()):
        s=re.sub(r'^[\s|,_.\'`।1~-]+','',l)
        s=re.sub(r'[\s|`_\'~-]+$','',s).replace(' | ',' ').replace('|','').strip()
        s=re.sub(r'(\S)\s*\.(\s*\.)+$',r'\1.',s); s=re.sub(r'\s+\.$','.',s)
        dev=len(re.findall(r'[ऀ-ॿ]',s)); gu=len(re.findall(r'[઀-૿]',s))
        if dev+gu<4: continue
        if i<2 and re.match(r'^\S{0,4}\s*[૦-૯०-९\d]*\s*\S+ોપનિષદ્',s) and len(s)<40: continue   # running head
        if i<2 and re.match(r'^(ખંડ|મંત્ર|અધ્યાય)\s',s) and len(s)<40: continue
        if gu and not dev: s=re.sub(r'\s*।$','',s)
        out.append(('[S] ' if dev>gu else '[G] ')+s)
open(OUT,'w',encoding='utf-8').write('\n'.join(out)+'\n'); print(len(out),'lines ->',OUT)
