import os
import json,urllib.request,urllib.parse,base64,sys
U=open('gasurl.txt').read().strip(); CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip(); key=sys.argv[1]; out=sys.argv[2]
def get(p): return json.load(urllib.request.urlopen(U+'?'+urllib.parse.urlencode({'action':'getcap','ck':CK,'key':key,'part':p}),timeout=60)).get('data')
n=int(get('n')); t=base64.b64decode(''.join(get(i) for i in range(n))).decode('utf-8')
open(out,'w',encoding='utf-8').write(t); print(out,len(t),'chars')
