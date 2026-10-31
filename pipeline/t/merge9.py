import os
import json,re,sys
NT=sys.argv[1] if len(sys.argv)>1 else 'v9/new.txt'; NR=sys.argv[2] if len(sys.argv)>2 else 'v9/rev_new.json'
p=os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/review/RMhKIMwo_Ug.json'
d=json.load(open(p,encoding='utf-8')); new=open(NT,encoding='utf-8').read()
N=json.load(open(NR,encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def find(s):
    m=list(re.finditer(flex(s),new)) if s.strip() else []
    return m[0].start() if len(m)==1 else None
keep=[];lost=[]
for it in d['items']:
    pos=find(it['cur'])
    if pos is None: lost.append(it)
    else: keep.append((pos,it))
for it in N:
    pos=find(it['cur'])
    if pos is None: print('new item not found!',it); continue
    it['src']='asr'; keep.append((pos,it))
keep.sort(key=lambda x:x[0])
seen=set();keep=[(p_,it) for p_,it in keep if not (it['id'] in seen or seen.add(it['id']))]
d['items']=[it for _,it in keep]; d['made']='2026-10-15-asr'
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('old kept',len(keep)-len(N),'old lost',len(lost),'new',len(N),'total',len(d['items']))
for it in lost[:10]: print('  lost:',it['kind'],it['cur'][:60])
