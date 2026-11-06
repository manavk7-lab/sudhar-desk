"""revlist.py VID — one line per judge decision: id, f/m/a, →[new], context with ⟪old⟫, what each engine read, why."""
import json,sys
V=sys.argv[1]; d=f'v{V}'
doc=open(f'{d}/doc.txt',encoding='utf-8').read()
K={k['id']:k for k in json.load(open(f'{d}/all_items.json',encoding='utf-8'))}
for j in json.load(open(f'{d}/decisions.json',encoding='utf-8')):
    c=K[j['id']]; t=c.get('t'); ts=f'[{t//60000}:{t//1000%60:02d}] ' if isinstance(t,int) else ''
    ctx=(doc[max(0,c['pos']-45):c['pos']]+'⟪'+c['old']+'⟫'+doc[c['end']:c['end']+30]).replace('\n',' ')
    rd=' || '.join(f'{k}: {v}' for k,v in (c.get('read') or {}).items())
    print(f"{j['id']} {j['d'][0]} →[{j.get('text') or ''}] {ts}{ctx} || {rd} | {j.get('why','')}")
