"""amendbrackets.py N YT DOCID BOOKS [--post] — put the book's brackets into a Doc that was posted before (Manav 19 Nov,
ઉપનિષદ - 43: "still ( ) is missed"). Reads the Doc as it is NOW (his own edits stay), runs t/bookbrackets.py on it,
applies the rows (each old unique), makes a ✎ item per row (src book, conf sure) with its video time.
Without --post: writes amend/N/{now,new}.txt + items.json and prints the rows (dry run).
With --post: hash-checked post (the hash of what was just read: stops if he edited the Doc meanwhile), then adds the
items to review/YT.json with merge_review.py (his ticks on older items stay). Check the Doc's folder first."""
import sys,os,json,hashlib,subprocess,re
n,yt,doc,books=sys.argv[1:5]; POST='--post' in sys.argv
S=os.environ['SD_WORK']; R=os.environ['SD_REPO']; A=f'{S}/amend/{n}'; os.makedirs(A,exist_ok=True)
def run(c): p=subprocess.run(c,cwd=S,capture_output=True,text=True); return (p.stdout+p.stderr).strip()
print(run(['python3','bin/readdoc.py',doc,f'{A}/now.txt']).split('\n')[-1])
now=open(f'{A}/now.txt',encoding='utf-8').read(); H=hashlib.sha256(now.encode()).hexdigest()[:16]
print(run(['python3','t/bookbrackets.py',f'{A}/now.txt',books,f'{A}/rows.json']).split('\n')[0])
rows=json.load(open(f'{A}/rows.json',encoding='utf-8')); t=now; items=[]
for old,new,why,conf in rows:
    if t.count(old)!=1: continue
    t=t.replace(old,new)
    items.append({'id':hashlib.sha1(new.encode()).hexdigest()[:8],'cur':new,'alt':old,'kind':'applied','conf':'sure','why':why,'src':'book'})
items=[x for x in items if t.count(x['cur'])==1]
open(f'{A}/new.txt','w',encoding='utf-8').write(t); json.dump(items,open(f'{A}/items.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
sy=f'{R}/sync/{yt}.tsv'
if os.path.exists(sy): run(['python3','t/addtimes.py',f'{A}/new.txt',sy,f'{A}/items.json'])
print(f'{n}: {len(items)} brackets')
for x in items: print('   ',x['alt'],' → ',x['cur'])
if POST and items:
    out=run(['python3','bin/postdoc.py',doc,H,f'{A}/new.txt']); print(out.split('\n')[-1])
    if ' OK' not in out: sys.exit('NOT POSTED')
    print(run(['python3','t/merge_review.py',f'{R}/review/{yt}.json',f'{A}/new.txt',f'{A}/items.json','claude-book-brackets']).split('\n')[-1])
