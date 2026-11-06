"""prepitems.py VM — give every source item file of VM an id (as collect_items.py computes it), so foldfix can find them."""
import json,re,hashlib,sys,os
d=sys.argv[1]
def norm(s): return re.sub(r'\s+',' ',s).strip()
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
for f in ['backbone_items.json','rev_new.json','rev_manual.json','rev_mantra.json','rev_agale.json']:
    p=f'{d}/{f}'
    if not os.path.exists(p): continue
    L=json.load(open(p,encoding='utf-8'))
    for it in L: it.setdefault('id',hid(norm(it['cur']),norm(it.get('alt',''))))
    json.dump(L,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('ids ok')
