"""wordfix1.py final.txt items.json rows.json sync.tsv — apply wordfix rows one at a time (a row that breaks the ✎ list is left out), then add video times."""
import json,sys,os,shutil,subprocess
F,I,RW,TS=sys.argv[1:5]; here=os.path.dirname(os.path.abspath(__file__))
rows=json.load(open(RW,encoding='utf-8')); out=[]
for row in rows:
    shutil.copy(F,F+'.b1'); shutil.copy(I,I+'.b1')
    json.dump([row],open(RW+'.1','w',encoding='utf-8'),ensure_ascii=False)
    r=subprocess.run(['python3',os.path.join(here,'wordfix.py'),F,I,RW+'.1',TS],capture_output=True,text=True,env=dict(os.environ,NOTIMES='1'))
    if r.returncode or open(F,encoding='utf-8').read()==open(F+'.b1',encoding='utf-8').read():
        shutil.copy(F+'.b1',F); shutil.copy(I+'.b1',I); out.append(row); print('LEFT OUT',repr(row[0][:70]),(r.stderr.strip().splitlines() or [''])[-1][:120])
it=json.load(open(I,encoding='utf-8')); nt=[x for x in it if not x.get('t')]
if nt:
    json.dump(nt,open(I+'.nt','w',encoding='utf-8'),ensure_ascii=False)
    subprocess.run(['python3',os.path.join(here,'addtimes.py'),F,TS,I+'.nt'],capture_output=True)
    tt={x['id']:x for x in json.load(open(I+'.nt',encoding='utf-8'))}
    it=[tt.get(x['id'],x) for x in it]; json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for f in [F+'.b1',I+'.b1',RW+'.1',I+'.nt']:
    if os.path.exists(f): os.remove(f)
print('applied',len(rows)-len(out),'left out',len(out))
