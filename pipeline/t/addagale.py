import os
import json,re,hashlib,subprocess
V={'7':'D3l7ZWNJbR0','8':'xbT0_i5jYIw','9':'RMhKIMwo_Ug','10':'-ZSHmbN85HU','11':'aMW4vNKSgsQ','12':'R-JjINI9wZQ','13':'VeNDdNe_ofc'}
DOCS={l.split('\t')[0]:l.split('\t')[1].strip() for l in open('learn/docs.tsv')}
AG=json.load(open('proof/agale.json',encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
for v,yt in V.items():
    p=os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+f'/review/{yt}.json'; d=json.load(open(p,encoding='utf-8'))
    text=open(f'today/cor{v}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    have={it['id'] for it in d['items']}; new=[]
    for f,r in AG.get(DOCS['cor'+v],[]):
        it={'id':hashlib.md5((f+'|'+r).encode()).hexdigest()[:8],'cur':r,'alt':f,'kind':'applied','conf':'likely','why':'YouTube heard આગળે','heard':'આગળે'}
        new.append(it)
    for m in re.finditer(r'(\S+\s+ત્યાં\s+)આગળ(?![઀-૿])(\S*\s+\S+)',text):
        cur=m.group(0); 
        if len(re.findall(flex(cur),text))!=1: continue
        alt=m.group(1)+'આગળે'+m.group(2)
        new.append({'id':hashlib.md5((cur+'|'+alt).encode()).hexdigest()[:8],'cur':cur,'alt':alt,'kind':'check','conf':'unsure','why':'listen: આગળ or આગળે?'})
    new=[n for n in new if n['id'] not in have]
    d['items']+=new
    pos={}
    for it in d['items']:
        mm=list(re.finditer(flex(it['cur']),text))
        if len(mm)==1: pos[it['id']]=mm[0].start()
    open('now/_t.txt','w',encoding='utf-8').write(text)
    ids=list(pos); P=[pos[i] for i in ids]
    js=f"""const A=require(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/align.js'),fs=require('fs');const t=fs.readFileSync('now/_t.txt','utf8');
const c=A.parseTsv(fs.readFileSync(os.environ.get('SD_REPO',os.path.expanduser('~/sudhar-desk'))+'/sync/{yt}.tsv','utf8'));const R=A.align(t,c);
console.log(JSON.stringify({json.dumps(P)}.map(p=>Math.round(R.words[A.wordAtChar(R.words,p)].t))))"""
    T=dict(zip(ids,json.loads(subprocess.run(['node','-e',js],capture_output=True,text=True).stdout)))
    for it in d['items']:
        if it['id'] in T: it['t']=T[it['id']]
    d['items'].sort(key=lambda it:pos.get(it['id'],10**9))
    json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    print(v,'added',len(new),[ (n['kind'],n['cur']) for n in new])
