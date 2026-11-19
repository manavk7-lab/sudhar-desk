"""finishdoc.py N YT DOCID 'TITLE' 'PROCESS note' VERSION — the last steps for one Doc, in order:
1. post vN/final.txt with the hash check (OLD = sha256[:16] of vN/doc_orig.txt); stop unless the post says OK;
2. write review/YT.json from vN/items_all_final.json (merge_review, tag claude-DATE);
3. add {yt,doc,title} after the last BUILTIN_PAIRS entry (if missing), set APP_VERSION + version.txt to VERSION;
4. add the PROCESS row after the last '| ઉપનિષદ - ' row (if missing);
5. key check on the staged diff, commit, push.
Check the Doc's folder (not "total final") BEFORE running this."""
import sys,os,hashlib,subprocess,datetime,re
n,yt,doc,title,note,ver=sys.argv[1:7]
S=os.environ['SD_WORK']; R=os.environ['SD_REPO']; V=f'{S}/v{n}'
def run(cmd,**k): return subprocess.run(cmd,shell=isinstance(cmd,str),capture_output=True,text=True,**k)
old=hashlib.sha256(open(f'{V}/doc_orig.txt','rb').read()).hexdigest()[:16]
# Manav 16 + 19 Nov ("still ( ) is missed … this type of mistakes not happen again"): no post while a book bracket
# he reads stands bare. vN/book.txt (written by fusem.sh; 'none' = no book) names the book files.
bf=f'{V}/book.txt'
if not os.path.exists(bf): print('NO vN/book.txt — write the book files (or none) there first'); sys.exit(1)
bk=open(bf).read().strip()
if bk!='none':
    p=run(['python3',f'{S}/t/bookbrackets.py',f'{V}/final.txt',bk,f'{V}/bb_rows.json','--report'],cwd=S)
    rep=p.stdout+p.stderr; open(f'{V}/bb_report.txt','w',encoding='utf-8').write(rep)
    nrow=len(__import__('json').load(open(f'{V}/bb_rows.json',encoding='utf-8'))) if os.path.exists(f'{V}/bb_rows.json') else -1
    if nrow!=0: print(f'BOOK BRACKETS: {nrow} bare (see {V}/bb_report.txt) — apply bb_rows.json with t/wordfix1.py first'); sys.exit(1)
    if '  ? book' in rep and not os.path.exists(f'{V}/bb_ok'):
        print(f'BOOK BRACKETS: one-side places in {V}/bb_report.txt — look at each, fix by hand, then touch {V}/bb_ok'); sys.exit(1)
p=run(['python3',f'{S}/bin/postdoc.py',doc,old,f'{V}/final.txt'],cwd=S)
out=(p.stdout+p.stderr).strip(); print(out[-300:])
if ' OK' not in out: print('NOT POSTED — stopping'); sys.exit(1)
rv=f'{R}/review/{yt}.json'
if os.path.exists(rv): os.remove(rv)
tag='claude-'+datetime.date.today().isoformat()
p=run(['python3',f'{S}/t/merge_review.py',rv,f'{V}/final.txt',f'{V}/items_all_final.json',tag],cwd=S); print((p.stdout+p.stderr).strip()[-200:])
h=f'{R}/index.html'; t=open(h,encoding='utf-8').read()
if f"yt:'{yt}'" not in t:
    m=list(re.finditer(r"  \{yt:'[^']+',doc:'[^']+',title:'[^']*'\},\n",t))
    last=m[-1]; t=t[:last.end()]+f"  {{yt:'{yt}',doc:'{doc}',title:'{title}'}},\n"+t[last.end():]
t=re.sub(r"const APP_VERSION='[^']*';",f"const APP_VERSION='{ver}';",t,count=1)
open(h,'w',encoding='utf-8').write(t); open(f'{R}/version.txt','w').write(ver+'\n')
pp=f'{R}/pipeline/PROCESS.md'; L=open(pp,encoding='utf-8').read().split('\n')
if not any(l.startswith(f'| ઉપનિષદ - {n} |') for l in L):
    i=max(k for k,l in enumerate(L) if l.startswith('| ઉપનિષદ - '))
    L.insert(i+1,f'| ઉપનિષદ - {n} | {yt} | {title.split(" · ")[-1]} | {note} |')
    open(pp,'w',encoding='utf-8').write('\n'.join(L))
files=['index.html','version.txt','pipeline/PROCESS.md',f'review/{yt}.json',f'sync/{yt}.tsv']
run(['git','add']+[f for f in files if os.path.exists(f'{R}/{f}')],cwd=R)
diff=run(['git','diff','--cached'],cwd=R).stdout
import glob
for k in glob.glob(f'{S}/*.key')+[f'{S}/{x}' for x in ('capkey.txt','secret.txt','gasurl.txt')]:
    if os.path.exists(k):
        v=open(k).read().strip()
        if v and v in diff: print('LEAK in staged diff:',k,'— not committing'); sys.exit(2)
n_items=len(__import__('json').load(open(rv)).get('items',[])) if os.path.exists(rv) else 0
msg=f"{title}: corrected Doc posted\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BqwzUN3pa6NduV51YfZwQo"
p=run(['git','commit','-q','-m',msg],cwd=R); print(p.stdout+p.stderr)
p=run(['git','push','-q'],cwd=R); print((p.stdout+p.stderr).strip()[-200:])
print(run(['git','log','--oneline','-1'],cwd=R).stdout.strip())
