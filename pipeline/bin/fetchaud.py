import os
import sys,json,base64,urllib.request,urllib.parse
U=open(os.environ.get('SD_WORK','.')+'/gasurl.txt').read().strip()
CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip(); key,out=sys.argv[1],sys.argv[2]
def get(part):
    q=urllib.parse.urlencode({'action':'getcap','ck':CK,'key':key,'part':part})
    return json.load(urllib.request.urlopen(U+'?'+q,timeout=60)).get('data')
n=int(get('n')); s=''
for i in range(n):
    d=get(i)
    if d is None: print('MISSING part',i); sys.exit(1)
    s+=d
open(out,'wb').write(base64.b64decode(s)); print('parts',n,'bytes',len(base64.b64decode(s)))
