"""finalvid.py VID — merge main-judge + candidate-judge decisions for vVID, apply to vVID/doc.txt -> vVID/new.txt + vVID/rev_new.json"""
import json,glob,sys,subprocess,os
V=sys.argv[1]; d=f'v{V}'
K=json.load(open(f'{d}/j_kept.json',encoding='utf-8'))
C=json.load(open(f'{d}/cands.json',encoding='utf-8')) if os.path.exists(f'{d}/cands.json') else []
J=[]
for p in sorted(glob.glob(f'{d}/j_*_out.json')): J+=json.load(open(p,encoding='utf-8'))
CJ=json.load(open(f'{d}/cands_out.json',encoding='utf-8')) if os.path.exists(f'{d}/cands_out.json') else []
Kid={k['id']:k for k in K}; Cid={c['id']:c for c in C}
J=[j for j in J if j.get('id') in Kid]
spans=[(Kid[j['id']]['pos'],Kid[j['id']]['end']) for j in J]
keepC=[]
for j in CJ:
    c=Cid.get(j.get('id'))
    if not c: continue
    if any(not (c['end']<=a or b<=c['pos']) for a,b in spans): print('cand overlaps main decision, dropped',j['id']); continue
    keepC.append(j)
items=K+[c for c in C]
json.dump(items,open(f'{d}/all_items.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump(J+keepC,open(f'{d}/decisions.json','w',encoding='utf-8'),ensure_ascii=False)
import collections; print('decisions',collections.Counter(j['d'] for j in J+keepC))
r=subprocess.run([sys.executable,'t/apply9.py',f'{d}/doc.txt',f'{d}/all_items.json',f'{d}/new.txt',f'{d}/rev_new.json',f'{d}/decisions.json'],capture_output=True,text=True)
print(r.stdout.strip(), r.stderr.strip()[-500:])
import re,hashlib
new=open(f'{d}/new.txt',encoding='utf-8').read(); old=open(f'{d}/doc.txt',encoding='utf-8').read()
R=json.load(open(f'{d}/rev_new.json',encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
print('newlines',old.count('\n'),new.count('\n'),'double spaces',old.count('  '),new.count('  '),'items',len(R),'not unique',sum(1 for x in R if len(re.findall(flex(x['cur']),new))!=1))
print('old sha',hashlib.sha256(old.encode()).hexdigest()[:16],'new sha',hashlib.sha256(new.encode()).hexdigest()[:16])
