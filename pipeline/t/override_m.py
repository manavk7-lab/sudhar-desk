"""override_m.py VM — my own review of the judges' decisions (spec in VM/override.json), then re-apply.
spec: {"DROP":{id:why}, "ASK":{id:why}, "TEXT":{id:[text,why]}, "MAYBE":{id:why}}
Edits VM/decisions.json in place and re-runs apply9 exactly as finalvid does."""
import json,subprocess,sys,re,hashlib,collections
d=sys.argv[1]
SP=json.load(open(f'{d}/override.json',encoding='utf-8'))
D=json.load(open(f'{d}/decisions.json',encoding='utf-8'))
ids={j['id'] for j in D}
for k in ['DROP','ASK','TEXT','MAYBE']:
    for i in SP.get(k,{}):
        if i not in ids: print('WARNING unknown id in',k,i)
out=[];n=collections.Counter()
for j in D:
    i=j['id']
    if i in SP.get('DROP',{}): n['drop']+=1; continue
    if i in SP.get('ASK',{}): j['d']='ask'; j['why']=SP['ASK'][i]; n['ask']+=1
    if i in SP.get('MAYBE',{}): j['d']='maybe'; j['why']=SP['MAYBE'][i]; n['maybe']+=1
    if i in SP.get('TEXT',{}): j['text'],j['why']=SP['TEXT'][i]; n['text']+=1
    out.append(j)
json.dump(out,open(f'{d}/decisions.json','w',encoding='utf-8'),ensure_ascii=False)
print('overrides',dict(n))
r=subprocess.run([sys.executable,'t/apply9.py',f'{d}/doc.txt',f'{d}/all_items.json',f'{d}/new.txt',f'{d}/rev_new.json',f'{d}/decisions.json'],capture_output=True,text=True)
print(r.stdout.strip(), r.stderr.strip()[-500:])
new=open(f'{d}/new.txt',encoding='utf-8').read(); old=open(f'{d}/doc.txt',encoding='utf-8').read()
R=json.load(open(f'{d}/rev_new.json',encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
print('newlines',old.count('\n'),new.count('\n'),'double spaces',new.count('  '),'items',len(R),'not unique',sum(1 for x in R if len(re.findall(flex(x['cur']),new))!=1))
