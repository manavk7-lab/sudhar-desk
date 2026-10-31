"""gemsplit.py piece_prefix [piece_prefix ...] — for pieces where Gemini refused the whole 10 minutes (block_reason OTHER),
transcribe ~150 s sub-pieces cut at silences; a sub-piece that is still refused is halved once; what stays refused becomes
ZZGAPZZ (fuse2 treats it as 'no Gemini here'). Writes PREFIX.gem2.txt."""
import sys,os,re,subprocess,concurrent.futures as cf
S=os.path.dirname(os.path.abspath(__file__))+'/..'
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout or 0)
def sils(p):
    log=subprocess.run(['ffmpeg','-i',p,'-af','silencedetect=n=-40dB:d=0.4','-f','null','-'],capture_output=True,text=True).stderr
    out=[];st=None
    for l in log.splitlines():
        m=re.search(r'silence_start: ([\d.]+)',l)
        if m: st=float(m.group(1))
        m=re.search(r'silence_end: ([\d.]+)',l)
        if m and st is not None: out.append((st+float(m.group(1)))/2); st=None
    return out
def cuts(p,a,b,target):
    s=[x for x in sils(p) if a<x<b]; c=[a]
    while b-c[-1]>target*1.4:
        want=c[-1]+target; near=[x for x in s if want-30<x<want+30]
        c.append(min(near,key=lambda x:abs(x-want)) if near else want)
    return c+[b]
def gem(src,a,b,tag):
    w=f'{tag}.wav'; o=f'{tag}.ogg'; t=f'{tag}.gem.txt'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.2f}','-to',f'{b:.2f}','-i',src,'-ac','1','-ar','16000',w],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',w,'-c:a','libopus','-b:a','32k',o],check=True)
    for k in range(2):
        subprocess.run([sys.executable,S+'/t/run_gemini.py',S+'/gemini.key','gemini-3.8-flash',o,t],capture_output=True,text=True)
        if os.path.exists(t) and os.path.getsize(t)>50: return open(t,encoding='utf-8').read().strip()
    return None
def piece(prefix):
    src=prefix+'.wav'; D=dur(src); C=cuts(src,0,D,150)
    out=[];refused=0
    with cf.ThreadPoolExecutor(6) as ex:
        res=list(ex.map(lambda i:gem(src,C[i],C[i+1],f'{prefix}_s{i:02d}'),range(len(C)-1)))
    for i,r in enumerate(res):
        if r is not None: out.append(r); continue
        # halve once
        a,b=C[i],C[i+1]; m=(a+b)/2
        h=[gem(src,a,m,f'{prefix}_s{i:02d}a'),gem(src,m,b,f'{prefix}_s{i:02d}b')]
        for x in h:
            if x is None: out.append('ZZGAPZZ'); refused+=1
            else: out.append(x)
    open(prefix+'.gem2.txt','w',encoding='utf-8').write(' '.join(out))
    print(prefix,'sub-pieces',len(C)-1,'refused halves',refused,'words',len(' '.join(out).split()),flush=True)
for p in sys.argv[1:]: piece(p)
