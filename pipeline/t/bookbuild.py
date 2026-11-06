"""bookbuild.py NAME clean1.txt[,clean2.txt] [START_MARK] [END_MARK] — book files from typed pages ([S]/[G] lines, BRIEF.md):
book/NAME.txt (all lines, Sanskrit in Gujarati script), book/NAME_gu.txt ([G] lines only), book/NAME_verses.json.
START_MARK / END_MARK: text of the [G] heading line where this Upanishad starts / the next one starts (optional)."""
import re,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from deva2gu import conv
B='/tmp/claude-0/-home-claude/bff094fd-345e-5cb3-95d4-5a521bc4ad84/scratchpad'
name=sys.argv[1]; files=sys.argv[2].split(','); st=sys.argv[3] if len(sys.argv)>3 else ''; en=sys.argv[4] if len(sys.argv)>4 else ''
L=[]
for f in files: L+=open(f if f.startswith('/') else B+'/'+f,encoding='utf-8').read().splitlines()
L=[l for l in L if not l.startswith('===')]
if st: i=next(i for i,l in enumerate(L) if st in l); L=L[i:]
if en: i=next((i for i,l in enumerate(L) if en in l and i>0),len(L)); L=L[:i]
full=[];gu=[];verses=[];cur=[]
for l in L:
    if l.startswith('[S] '):
        s=l[4:].strip(); full.append(conv(s)); cur.append(s)
        if re.search(r'॥\s*[०-९\d]+[-०-९\d]*\s*॥\s*$',s) or re.search(r'शान्तिः\s*॥\s*$',s):
            d=' '.join(cur); verses.append({'n':len(verses),'deva':d,'gu':conv(d)}); cur=[]
    elif l.startswith('[G] '):
        g=l[4:].strip(); full.append(g); gu.append(g)
if cur: d=' '.join(cur); verses.append({'n':len(verses),'deva':d,'gu':conv(d)})
open(f'{B}/book/{name}.txt','w',encoding='utf-8').write('\n'.join(full)+'\n')
open(f'{B}/book/{name}_gu.txt','w',encoding='utf-8').write('\n'.join(gu)+'\n')
json.dump(verses,open(f'{B}/book/{name}_verses.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(name,'lines',len(full),'gu',len(gu),'verses',len(verses),'| first:',(gu[0] if gu else '')[:40],'| last:',(gu[-1] if gu else '')[:40])
