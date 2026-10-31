"""addtimes.py text.txt yt.tsv items.json [--all] — fill in 't' (ms) for ✎ items from the caption word times aligned to text."""
import sys,json,re,subprocess,os
S=os.path.dirname(os.path.abspath(__file__))
tf,cf,jf=sys.argv[1:4]; allt='--all' in sys.argv
text=open(tf,encoding='utf-8').read(); items=json.load(open(jf,encoding='utf-8'))
subprocess.run(['node',S+'/wordtimes.js',tf,cf,tf+'.words'],check=True,capture_output=True)
W=json.load(open(tf+'.words'))
def tm(pos):
    best=None
    for s,e,ms,m in W:
        if s<=pos: best=ms
        else: break
    return best
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
n=0
for it in items:
    if it.get('t') is not None and not allt: continue
    m=list(re.finditer(flex(it['cur']),text))
    if len(m)==1: it['t']=tm(m[0].start()); n+=1
json.dump(items,open(jf,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('times set',n,'of',len(items))
