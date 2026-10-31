import os
import json,re,subprocess,collections
V={'7':'D3l7ZWNJbR0','8':'xbT0_i5jYIw','9':'RMhKIMwo_Ug','10':'-ZSHmbN85HU','11':'aMW4vNKSgsQ','12':'R-JjINI9wZQ','13':'VeNDdNe_ofc'}
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
for v,yt in V.items():
    p=os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+f'/review/{yt}.json'; d=json.load(open(p,encoding='utf-8'))
    text=open(f'now/cor{v}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    c=collections.Counter(); pos={}
    for it in d['items']:
        if it['kind']=='check':
            m=list(re.finditer(flex(it['alt']),text)) if it['alt'].strip() else []
            if len(m)==1 and not re.search(flex(it['cur']),text):
                it['cur'],it['alt']=it['alt'],it['cur']; it['kind']='applied'
        m=list(re.finditer(flex(it['cur']),text))
        if len(m)==1: pos[it['id']]=m[0].start()
        c[it['kind'],len(m)==1]+=1
    open('now/_t.txt','w',encoding='utf-8').write(text)
    ids=[i for i in pos]; P=[pos[i] for i in ids]
    js=f"""const A=require(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/align.js'),fs=require('fs');const t=fs.readFileSync('now/_t.txt','utf8');
const c=A.parseTsv(fs.readFileSync(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/sync/{yt}.tsv','utf8'));const R=A.align(t,c);
console.log(JSON.stringify({json.dumps(P)}.map(p=>Math.round(R.words[A.wordAtChar(R.words,p)].t))))"""
    ts=json.loads(subprocess.run(['node','-e',js],capture_output=True,text=True).stdout); T=dict(zip(ids,ts))
    for it in d['items']:
        if it['id'] in T: it['t']=T[it['id']]
    d['items'].sort(key=lambda it:pos.get(it['id'],10**9))
    d['made']='2026-10-14b'
    json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print(v,dict(c))
