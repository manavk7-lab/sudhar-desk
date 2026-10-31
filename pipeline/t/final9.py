import json,glob,re,subprocess,sys
R=json.load(open('v9/reuse_out.json',encoding='utf-8'))
for p in sorted(glob.glob('v9/n_*_out.json')): R+=json.load(open(p,encoding='utf-8'))
drop={'c1190','c995'}; to_ask={'c512','c508'}
out=[]
for j in R:
    if j['id'] in drop: continue
    if j['id'] in to_ask: j=dict(j,d='ask',why=j.get('why','')+' (order unclear — listen)')
    out.append(j)
json.dump(out,open('v9/decisions.json','w',encoding='utf-8'),ensure_ascii=False)
import collections; print(len(out),collections.Counter(j['d'] for j in out))
