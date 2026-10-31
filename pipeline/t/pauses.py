"""pauses.py text.txt yt.tsv out.json part.wav:START_SEC [part2.wav:START ...]
For every word boundary in the text, measure the silence (pause) in the recorded audio.
Recording time is mapped to video time by matching caption word starts to speech onsets (handles ads at the start
and in the middle). Output: list of {i, pos (char after word i), pause (s), conf}"""
import os
import sys,json,wave,subprocess,numpy as np
tf,cf,of=sys.argv[1],sys.argv[2],sys.argv[3]; parts=[(a.split(':')[0],float(a.split(':')[1]),(float(a.split(':')[2]) if len(a.split(':'))>2 else None)) for a in sys.argv[4:]]
S=os.environ.get('SD_WORK','.')+''
subprocess.run(['node',S+'/t/wordtimes.js',tf,cf,of+'.words'],check=True,capture_output=True)
W=json.load(open(of+'.words'))
caps=[]
for l in open(cf,encoding='utf-8'):
    if l[0]=='#' or '\t' not in l: continue
    t,w=l.rstrip('\n').split('\t',1); caps.append((int(t)/1000.0,w))
capt=np.array([c[0] for c in caps])
HOP=0.01
def envelope(path):
    with wave.open(path) as f:
        sr=f.getframerate(); n=f.getnframes(); x=np.frombuffer(f.readframes(n),dtype=np.int16).astype(np.float32)
    win=int(0.03*sr); hop=int(HOP*sr); m=(len(x)-win)//hop
    idx=np.arange(win)[None,:]+hop*np.arange(m)[:,None]
    e=np.sqrt((x[idx]**2).mean(1)+1e-6); db=20*np.log10(e+1e-6)
    return db
res=[]
for path,START,O0 in parts:
    db=envelope(path); T=len(db)*HOP
    floor=np.percentile(db,10); speech_lvl=np.percentile(db,80)
    thr=floor+0.35*(speech_lvl-floor)
    sp=db>thr
    # silence runs >= 0.12 s
    runs=[];i=0;n=len(sp)
    while i<n:
        if not sp[i]:
            j=i
            while j<n and not sp[j]: j+=1
            if (j-i)*HOP>=0.12: runs.append((i*HOP,j*HOP))
            i=j
        else: i+=1
    onsets=np.array([e for s,e in runs])          # speech starts after a silence
    # anchor caption words: those preceded by a caption gap >= 0.6 s
    gaps=np.diff(capt,prepend=-10)
    anchors=capt[(gaps>=0.6)]
    # offset per window of video time
    vstart=START; vend=START+T
    offs=[]; prev=O0   # known starting offset (recorder seeked to START before recording) or None
    for w0 in np.arange(vstart,vend,30.0):
        a=anchors[(anchors>=w0)&(anchors<w0+150)]
        if len(a)<5: offs.append((w0,prev)); continue
        lo,hi=(-5,180) if prev is None else ((prev-2,prev+2) if O0 is not None else (prev-3,prev+150))   # known start: no ads, small drift only
        best=None
        for o in np.arange(lo,hi,0.02):
            r=a-START+o
            k=np.searchsorted(onsets,r)
            d=np.minimum(np.abs(onsets[np.clip(k,0,len(onsets)-1)]-r),np.abs(onsets[np.clip(k-1,0,len(onsets)-1)]-r))
            sc=(d<0.15).sum()
            if best is None or sc>best[0]+0 or (sc==best[0] and prev is not None and abs(o-prev)<abs(best[1]-prev)): best=(sc,o)
        # only accept if clearly matched
        if best[0]>=0.35*len(a): prev=float(best[1])
        offs.append((float(w0),prev))
    print(path,'offsets',[(int(w),None if o is None else round(o,2)) for w,o in offs][:40],file=sys.stderr)
    def off_at(tv):
        o=None
        for w0,oo in offs:
            if w0<=tv and oo is not None: o=oo
        if o is None:
            for w0,oo in offs:
                if oo is not None: return oo
        return o
    rs=np.array([s for s,e in runs]); re_=np.array([e for s,e in runs])
    for i in range(len(W)-1):
        t1=W[i][2]/1000.0; t2=W[i+1][2]/1000.0
        if t1<START or t2>START+T-1: continue
        o=off_at(t1)
        if o is None: continue
        r1=t1-START+o; r2=t2-START+o
        # silence runs whose middle lies in (r1+0.08, r2+0.12)
        mid=(rs+re_)/2
        sel=(mid>r1+0.08)&(mid<r2+0.12)
        p=float((re_[sel]-rs[sel]).max()) if sel.any() else 0.0
        conf=1 if (W[i][3] and W[i+1][3]) else 0
        res.append({'i':i,'pos':W[i][1],'pause':round(p,3),'conf':conf,'gap':round(t2-t1,3)})
best={}
for r in res:
    if r['i'] not in best or r['conf']>best[r['i']]['conf']: best[r['i']]=r
out=sorted(best.values(),key=lambda r:r['i'])
json.dump(out,open(of,'w'))
print('boundaries',len(out),file=sys.stderr)
