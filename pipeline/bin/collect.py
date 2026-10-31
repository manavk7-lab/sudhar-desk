import json,os,time,urllib.request,urllib.parse,sys
U=open(os.environ.get('SD_WORK','.')+'/gasurl.txt').read().strip(); CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip()
keys=sys.argv[1].split(','); base=sys.argv[2]
def get(k,p):
    for a in range(3):
        try: return json.load(urllib.request.urlopen(U+'?'+urllib.parse.urlencode({'action':'getcap','ck':CK,'key':k,'part':p}),timeout=60)).get('data')
        except Exception as e: time.sleep(5)
    return None
st={k:{'n':None} for k in keys}
t0=time.time()
while time.time()-t0<6000:
    alldone=True
    for k in keys:
        d=f'{base}/{k}'; os.makedirs(d,exist_ok=True)
        if st[k]['n'] is None:
            n=get(k,'n'); st[k]['n']=int(n) if n else None
        have=set(int(f) for f in os.listdir(d))
        hi=max(have)+1 if have else 0
        # fetch new parts until a None beyond the end
        p=0; misses=0
        upto=st[k]['n'] if st[k]['n'] is not None else hi+12
        for p in range(upto):
            if p in have: continue
            x=get(k,p)
            if x is not None: open(f'{d}/{p:04d}','w').write(x); have.add(p)
        missing=[p for p in range(max(have)+1 if have else 0) if p not in have]
        if st[k]['n'] is not None: missing=[p for p in range(st[k]['n']) if p not in have]
        done = st[k]['n'] is not None and not missing
        alldone &= done
        print(time.strftime('%H:%M:%S'),k,'have',len(have),'n',st[k]['n'],'missing',missing[:20],flush=True)
    if alldone: print('ALLDONE',flush=True); break
    time.sleep(60)
