"""postedstate.py N... — for each posted Doc: read it now, find which local vN/final*.txt it equals and which items file fits."""
import sys,glob,hashlib,json,subprocess,os
ids={}
for l in open('docs.tsv',encoding='utf-8'):
    p=l.rstrip('\n').split('\t')
    if len(p)>1 and p[0].startswith('UPNISHAD -video '): ids[p[0].split('video ')[1].split('.')[0]]=(p[1],p[2])
h=lambda s:hashlib.sha256(s.encode()).hexdigest()[:16]
for n in sys.argv[1:]:
    doc,folder=ids[n]
    out=f'v{n}/now.txt'
    r=subprocess.run(['python3','bin/readdoc.py',doc,out],capture_output=True,text=True).stdout.split()
    now=open(out,encoding='utf-8').read(); hn=h(now)
    match=[f for f in sorted(glob.glob(f'v{n}/final*.txt')) if h(open(f,encoding='utf-8').read())==hn]
    its=[]
    if match:
        for f in sorted(glob.glob(f'v{n}/items_all_final*.json')):
            I=json.load(open(f,encoding='utf-8'))
            if all(now.count(x['cur'])==1 for x in I): its.append((f,len(I)))
    print(n,doc,hn,'folder-total-final' if folder=='13GCS6Z1zUmUKI7noi8MA43aYLblzqB4O' else '','MATCH' if match else 'CHANGED',match[:2],its[:3])
