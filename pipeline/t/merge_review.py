"""merge_review.py review.json new_text.txt new_items.json [made-tag] — add new ✎ items, keep old ones still locatable."""
import json,re,sys,os
p,NT,NR=sys.argv[1],sys.argv[2],sys.argv[3]; tag=sys.argv[4] if len(sys.argv)>4 else 'asr'
d=json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {'v':1,'yt':os.path.basename(p)[:-5],'items':[]}
new=open(NT,encoding='utf-8').read(); N=json.load(open(NR,encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def find(s):
    m=list(re.finditer(flex(s),new)) if s.strip() else []
    return m[0].start() if len(m)==1 else None
keep=[];lost=0
for it in d['items']:
    pos=find(it['cur'])
    if pos is None: lost+=1
    else: keep.append((pos,it))
added=0
for it in N:
    pos=find(it['cur'])
    if pos is None: print('new item not found!',it['cur'][:60]); continue
    it['src']='asr'; keep.append((pos,it)); added+=1
keep.sort(key=lambda x:x[0])
seen=set(); keep=[(q,it) for q,it in keep if not (it['id'] in seen or seen.add(it['id']))]
d['items']=[it for _,it in keep]; d['made']=__import__('time').strftime('%Y-%m-%d')+'-'+tag
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(os.path.basename(p),'old kept',len(keep)-added,'old dropped',lost,'new',added,'total',len(d['items']))
