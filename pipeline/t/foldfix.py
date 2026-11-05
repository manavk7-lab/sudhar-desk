"""foldfix.py VM text.txt items.json groups.json out.json — fold ✎ items that change the same words into one item.
groups.json: [[id, id, ...], ...]; ids are looked up in items.json and in the VM source files (backbone_items, rev_new,
rev_manual, rev_mantra, rev_agale, rev_punct) so items collect_items reported LOST can be folded too. For each group the
merged item covers the union of the texts, cur = the text now, alt = the text with every member undone in reverse order
(the order the members were applied). Writes items.json minus the members plus the merged items."""
import json,re,sys,hashlib,os
VM,TXT,ITEMS,GROUPS,OUT=sys.argv[1:6]
t=open(TXT,encoding='utf-8').read(); I=json.load(open(ITEMS,encoding='utf-8')); G=json.load(open(GROUPS,encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
order=[]; byid={}
for f in ['backbone_items.json','rev_new.json','rev_manual.json','rev_mantra.json','rev_agale.json','rev_punct.json']:
    p=os.path.join(VM,f)
    if os.path.exists(p):
        for it in json.load(open(p,encoding='utf-8')):
            if it.get('id') and it['id'] not in byid: byid[it['id']]=it; order.append(it['id'])
for it in I:
    if it.get('id') not in byid: byid[it['id']]=it; order.append(it['id'])
def span_of(s):
    m=list(re.finditer(flex(s),t)); return m[0].span() if len(m)==1 else None
out=[it for it in I]; drop=set(); new=[]
for g in G:
    mem=sorted([byid[i] for i in g], key=lambda it: order.index(it['id']))
    sp=[span_of(it['cur']) for it in mem]; found=[s for s in sp if s]
    a=min(s[0] for s in found); b=max(s[1] for s in found)
    ok=False
    for grow in range(0,12):
        a2=a; b2=b
        for _ in range(grow):
            j=t.rfind(' ',0,max(0,a2-1)); a2=j+1 if j>=0 else 0
            j=t.find(' ',b2+1); b2=j if j>=0 else len(t)
        seg=t[a2:b2]; good=True
        for it in reversed(mem):
            m=list(re.finditer(flex(it['cur']),seg))
            if len(m)!=1: good=False; break
            s,e=m[0].span(); seg=seg[:s]+it['alt']+seg[e:]
        if good: ok=True; break
    if not ok: print('could not fold',g); continue
    cur=t[a2:b2]; alt=seg
    confs=[it.get('conf','sure') for it in mem]
    conf='unsure' if 'unsure' in confs else ('likely' if 'likely' in confs else 'sure')
    why=' + '.join(dict.fromkeys(it.get('why','') for it in mem if it.get('why')))
    heard=' · '.join(x for x in dict.fromkeys(it.get('heard') or '' for it in mem) if x) or None
    ts=[it.get('t') for it in mem if it.get('t') is not None]
    new.append({'id':hid(cur,alt),'cur':cur,'alt':alt,'kind':'applied','conf':conf,'why':why,'heard':heard,'t':min(ts) if ts else None})
    drop.update(g); print('folded',g,'->',repr(cur[:70]))
res=[it for it in out if it.get('id') not in drop]+new
json.dump(res,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=0); print('items',len(I),'->',len(res))
