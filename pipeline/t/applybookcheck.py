"""applybookcheck.py N YT [--dry] — apply the BOOKCHECK rows (bcN/bookcheck_out*.json) and the book-bracket comma rows
(bcN/unbr.json) to a POSTED Doc whose current text is bcN/final.txt and whose ✎ list is $SD_REPO/review/YT.json.
Writes bcN/new.txt and bcN/items.json (the whole ✎ list after the changes); prints what it did and the checks.
Rows with conf "listen" change nothing and are only reported. Run from the work folder."""
import json,sys,os,glob,subprocess,shutil,re
N,YT=sys.argv[1],sys.argv[2]; DRY='--dry' in sys.argv
R=os.environ.get('SD_REPO','/home/claude/sudhar-desk'); D=f'bc{N}'
t=open(f'{D}/final.txt',encoding='utf-8').read()
rev=json.load(open(f'{R}/review/{YT}.json',encoding='utf-8'))['items']
rows=[]
RF=[a.split('=',1)[1] for a in sys.argv if a.startswith('--rows=')]
for f in (RF or sorted(glob.glob(f'{D}/bookcheck_out*.json'))+[f'{D}/unbr.json']):
    if os.path.exists(f): rows+=json.load(open(f,encoding='utf-8'))
listen=[r for r in rows if len(r)>3 and r[3]=='listen']
rows=[r for r in rows if not(len(r)>3 and r[3]=='listen') and r[0]!=r[1]]
ok=[];bad=[]
for r in rows:
    old,new=r[0],r[1]
    if '"' in new: bad.append(('quote in new',r)); continue
    if t.count(old)!=1: bad.append((f'old occurs {t.count(old)}x',r)); continue
    ok.append([old,new,r[2] if len(r)>2 else 'as in the book',r[3] if len(r)>3 else 'likely'])
# overlapping rows: keep the first, report the rest
spans=[];keep=[]
for r in ok:
    p=t.find(r[0]); q=p+len(r[0])
    if any(p<b and q>a for a,b in spans): bad.append(('overlaps another row',r)); continue
    spans.append((p,q)); keep.append(r)
print(f'rows {len(rows)} usable {len(keep)} skipped {len(bad)} listen {len(listen)}')
for why,r in bad: print('  SKIP',why,'|',repr(r[0][:70]),'->',repr(r[1][:70]))
for r in listen: print('  LISTEN',repr(r[0][:60]),'|',r[2][:90])
for r in keep: print('  ',repr(r[0][:80]),'->',repr(r[1][:80]),'|',r[2][:60])
if DRY: sys.exit()
shutil.copy(f'{D}/final.txt',f'{D}/new.txt')
json.dump(rev,open(f'{D}/items.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump(keep,open(f'{D}/rows_apply.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
here=os.path.dirname(os.path.abspath(__file__))
r=subprocess.run(['python3',os.path.join(here,'wordfix.py'),f'{D}/new.txt',f'{D}/items.json',f'{D}/rows_apply.json',f'{R}/sync/{YT}.tsv'],capture_output=True,text=True)
if r.returncode:                                    # one row at a time; a row that breaks the ✎ list is left out
    print('wordfix failed as a batch; applying rows one by one')
    shutil.copy(f'{D}/final.txt',f'{D}/new.txt'); json.dump(rev,open(f'{D}/items.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    for row in keep:
        shutil.copy(f'{D}/new.txt',f'{D}/new.bak'); shutil.copy(f'{D}/items.json',f'{D}/items.bak')
        json.dump([row],open(f'{D}/row1.json','w',encoding='utf-8'),ensure_ascii=False)
        r=subprocess.run(['python3',os.path.join(here,'wordfix.py'),f'{D}/new.txt',f'{D}/items.json',f'{D}/row1.json',f'{R}/sync/{YT}.tsv'],capture_output=True,text=True,env=dict(os.environ,NOTIMES='1'))
        if r.returncode:
            shutil.copy(f'{D}/new.bak',f'{D}/new.txt'); shutil.copy(f'{D}/items.bak',f'{D}/items.json'); print('  LEFT OUT',repr(row[0][:70]))
if os.path.exists(f'{D}/row1.json'):                 # times for the items made one by one
    it=json.load(open(f'{D}/items.json',encoding='utf-8')); nt=[x for x in it if not x.get('t')]
    if nt:
        json.dump(nt,open(f'{D}/nt.json','w',encoding='utf-8'),ensure_ascii=False)
        subprocess.run(['python3',os.path.join(here,'addtimes.py'),f'{D}/new.txt',f'{R}/sync/{YT}.tsv',f'{D}/nt.json'],capture_output=True)
        tt={x['id']:x for x in json.load(open(f'{D}/nt.json',encoding='utf-8'))}
        it=[tt.get(x['id'],x) for x in it]; json.dump(it,open(f'{D}/items.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    os.remove(f'{D}/row1.json')
for c in [['overlapcheck.py',f'{D}/new.txt',f'{D}/items.json'],['revertcheck.py',f'{D}/final.txt',f'{D}/items_rev_before.json',f'v{N}/doc_orig.txt'],['revertcheck.py',f'{D}/new.txt',f'{D}/items.json',f'v{N}/doc_orig.txt'],['lastcheck.py',f'{D}/new.txt',f'{D}/items.json']]:
    if c[0]=='revertcheck.py' and 'items_rev_before' in c[2]: json.dump(rev,open(c[2],'w',encoding='utf-8'),ensure_ascii=False)
    o=subprocess.run(['python3',os.path.join(here,c[0])]+c[1:],capture_output=True,text=True)
    print(c[0],c[1].split('/')[-1],'|',(o.stdout.strip().splitlines() or [''])[-1][:160],o.stderr[-200:] if o.returncode else '')
