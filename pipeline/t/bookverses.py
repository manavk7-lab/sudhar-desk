"""bookverses.py book_deva.txt out.json — Sanskrit verses (Devanagari lines) from the OCR'd book, with Gujarati-script text."""
import sys,re,json
sys.path.insert(0,__import__('os').path.dirname(__file__)); from deva2gu import conv
t=open(sys.argv[1],encoding='utf-8').read()
lines=t.split('\n')
isdev=lambda l: sum(1 for c in l if 'ऀ'<=c<='ॿ' and c not in '।॥')>max(5,0.5*sum(1 for c in l if c.strip()))
verses=[];cur=[]
for l in lines:
    if isdev(l):
        cur.append(l.strip())
        if re.search(r'॥\s*[०-९\d]+\s*॥\s*$',l.strip()) or 'इति शान्तिः' in l:
            verses.append(cur); cur=[]
    else:
        if cur and not l.strip(): continue
        if cur: verses.append(cur); cur=[]
if cur: verses.append(cur)
out=[{'n':i,'deva':'\n'.join(v),'gu':conv('\n'.join(v))} for i,v in enumerate(verses)]
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(sys.argv[1],'verses',len(out))
