"""collect_items.py VM — gather every ✎ item (backbone, judges, my fixes, mantras, આગળે) for VM/new_a.txt -> VM/items_pre.json"""
import json,re,sys,hashlib,os
d=sys.argv[1]
text=open(f'{d}/new_a.txt',encoding='utf-8').read()
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def norm(s): return re.sub(r'\s+',' ',s).strip()
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
src=[('backbone_items.json',None),('rev_new.json',None),('rev_manual.json','manual'),('rev_mantra.json','mantra'),('rev_agale.json','agale')]
out=[];lost=[];same=0
for f,tag in src:
    p=f'{d}/{f}'
    if not os.path.exists(p): continue
    for it in json.load(open(p,encoding='utf-8')):
        it=dict(it)
        it.setdefault('kind','applied'); it.setdefault('conf','sure'); it.setdefault('heard',None)
        if norm(it['cur'])==norm(it.get('alt','')): same+=1; continue
        it.setdefault('id',hid(norm(it['cur']),norm(it.get('alt',''))))
        m=list(re.finditer(flex(it['cur']),text)) if it['cur'].strip() else []
        if len(m)!=1: lost.append((f,it['cur'][:70],len(m))); continue
        out.append(it)
json.dump(out,open(f'{d}/items_pre.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(d,'items',len(out),'same-text skipped',same,'not found',len(lost))
for l in lost: print('  LOST',l)
