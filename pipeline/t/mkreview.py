import json,re,hashlib,subprocess,collections,os
E=json.load(open('proof/all_edits.json',encoding='utf-8'))
meta={}
import glob
for mf in glob.glob('proof/v*_meta.json'):
    m=json.load(open(mf,encoding='utf-8')); name=mf.split('/')[-1][:-10]
    meta[name]=m
# heard per (video, aid) — need chunk name; edits don't record chunk name, recover by pos range
def heard_for(e):
    if 'aid' not in e: return None
    for name,m in meta.items():
        if m['video']==e['video'] and m['offset']<=e['pos']<m['end']:
            i=int(re.sub(r'\D','',e['aid'].split(',')[0].split('/')[0]) or 0)-1
            if 0<=i<len(m['ai']): return m['ai'][i]['heard']
    return None
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
out=collections.defaultdict(list); miss=0
for e in E:
    v=e['video']; text=open(f'now/cor{v}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    if e['conf']=='sure': cur,alt,kind=e['replace'],e['find'],'auto'
    else: cur,alt,kind=e['find'],e['replace'],'check'
    ms=list(re.finditer(flex(cur),text))
    if len(ms)!=1: miss+=1; continue
    item={'id':hashlib.md5((cur+'|'+alt).encode()).hexdigest()[:8],'cur':cur.replace('\n\n\n',' ') if kind=='auto' else cur,'alt':alt,'kind':kind,'conf':e['conf'],'why':e.get('why',''),'pos':ms[0].start()}
    h=heard_for(e)
    if h is not None: item['heard']=h
    out[(v,e['yt'])].append(item)
print('not located',miss)
# times via align.js
for (v,yt),items in out.items():
    text=open(f'now/cor{v}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    open(os.environ.get('SD_WORK','.')+'/now/_t.txt','w',encoding='utf-8').write(text)
    pos=json.dumps([i['pos'] for i in items])
    js=f"""const A=require(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/align.js'),fs=require('fs');const t=fs.readFileSync(os.environ.get('SD_WORK','.')+'/now/_t.txt','utf8');
const c=A.parseTsv(fs.readFileSync(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/sync/{yt}.tsv','utf8'));const R=A.align(t,c);
console.log(JSON.stringify({pos}.map(p=>Math.round(R.words[A.wordAtChar(R.words,p)].t))))"""
    ts=json.loads(subprocess.run(['node','-e',js],capture_output=True,text=True).stdout)
    for i,t in zip(items,ts): i['t']=t
    items.sort(key=lambda i:i['pos'])
    for i in items: del i['pos']
    os.makedirs(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/review',exist_ok=True)
    json.dump({'v':1,'yt':yt,'made':'2026-10-14','items':items},open(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+f'/review/{yt}.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    c=collections.Counter(i['kind'] for i in items)
    print('video',v,yt,dict(c))
