import sys, json, urllib.request, urllib.parse, os
S=os.environ.get('SD_WORK','.')+''
U=open(S+'/gasurl.txt').read().strip(); CK=open(S+'/capkey.txt').read().strip()
def get(key,part):
    q=urllib.parse.urlencode({'action':'getcap','ck':CK,'key':key,'part':part})
    return json.loads(urllib.request.urlopen(U+'?'+q,timeout=60).read().decode())['data']
key=sys.argv[1]; out=sys.argv[2]
n=get(key,'n')
if not n: sys.exit('no data for '+key)
data=''.join(get(key,k) or '' for k in range(int(n)))
open(out,'w',encoding='utf-8').write(data)
lines=[l for l in data.splitlines() if l and not l.startswith('#')]
t=[int(l.split('\t')[0]) for l in lines]
print(key,'parts',n,'words',len(lines),'mono',all(t[i]>=t[i-1] for i in range(1,len(t))),'last',lines[-1] if lines else None)
