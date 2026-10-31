import sys,json,os,urllib.request,urllib.parse
U=open(os.environ.get('SD_WORK','.')+'/gasurl.txt').read().strip()
CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip(); key,d=sys.argv[1],sys.argv[2]; os.makedirs(d,exist_ok=True)
def get(part):
    q=urllib.parse.urlencode({'action':'getcap','ck':CK,'key':key,'part':part})
    return json.load(urllib.request.urlopen(U+'?'+q,timeout=60)).get('data')
i=0;got=0
while True:
    f=f'{d}/{i:04d}'
    if not os.path.exists(f):
        x=get(i)
        if x is None: break
        open(f,'w').write(x); got+=1
    i+=1
n=get('n'); print('have up to part',i-1,'new',got,'final count',n)
