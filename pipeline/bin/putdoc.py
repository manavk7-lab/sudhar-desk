import os
import json,urllib.request,base64,sys,hashlib
U=open('gasurl.txt').read().strip(); CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip(); key=sys.argv[1]; t=open(sys.argv[2],encoding='utf-8').read()
b=base64.b64encode(t.encode('utf-8')).decode(); P=[b[i:i+90000] for i in range(0,len(b),90000)]
def put(part,data):
    req=urllib.request.Request(U,data=json.dumps({'action':'putcap','ck':CK,'key':key,'part':part,'data':data}).encode(),headers={'Content-Type':'text/plain;charset=utf-8'})
    return json.load(urllib.request.urlopen(req,timeout=60))
r=[put(i,p).get('ok') for i,p in enumerate(P)]; r.append(put('n',str(len(P))).get('ok'))
print(key,len(t),'chars',len(P),'parts',r)
