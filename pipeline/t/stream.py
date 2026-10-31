"""Process recorded parts as they arrive: decode, cut stable ~10-min pieces at silences, run Gemini + Sarvam per piece."""
import os,sys,re,subprocess,time,json,concurrent.futures as cf,base64
B='audio/a9'; PARTS=['a9a','a9b','a9c']; TG=600
ex=cf.ThreadPoolExecutor(6); jobs={}
def decode(k):
    d=f'{B}/{k}'; names=sorted(n for n in os.listdir(d) if n.isdigit())
    buf='';bs=b'';done=0
    for i,n in enumerate(names):
        if int(n)!=i: break
        s=open(f'{d}/{n}').read()
        if s.startswith('|'): buf+=s[1:]; bs+=base64.b64decode(buf); buf=''
        else: buf+=s
    open(f'{B}/{k}.webm','wb').write(bs)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{B}/{k}.webm','-ac','1','-ar','16000',f'{B}/{k}.wav'],capture_output=True)
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{B}/{k}.wav'],capture_output=True,text=True).stdout or 0)
def sils(k):
    log=subprocess.run(['ffmpeg','-i',f'{B}/{k}.wav','-af','silencedetect=n=-40dB:d=0.4','-f','null','-'],capture_output=True,text=True).stderr
    out=[];st=None
    for l in log.splitlines():
        m=re.search(r'silence_start: ([\d.]+)',l)
        if m: st=float(m.group(1))
        m=re.search(r'silence_end: ([\d.]+)',l)
        if m and st is not None: out.append((st+float(m.group(1)))/2); st=None
    return out
def gem(p):
    o=p+'.gem.txt'
    for a in range(4):
        if os.path.exists(o) and os.path.getsize(o)>1500: return 'ok'
        r=subprocess.run([sys.executable,'t/run_gemini.py','gemini.key','gemini-3.8-flash',p+'.ogg',o],capture_output=True,text=True)
        if os.path.exists(o) and os.path.getsize(o)>1500: return 'ok'
        print('gem retry',p,(r.stderr or r.stdout)[-200:],flush=True); time.sleep(30*(a+1))
    return 'fail'
def sar(p):
    o=p+'.sar.txt'
    for a in range(3):
        if os.path.exists(o) and os.path.getsize(o)>1500: return 'ok'
        r=subprocess.run([sys.executable,'t/run_sarvam.py','sarvam.key','saaras:v4',p+'.wav',o],capture_output=True,text=True)
        if os.path.exists(o) and os.path.getsize(o)>1500: return 'ok'
        print('sar retry',p,(r.stderr or r.stdout)[-300:],flush=True); time.sleep(30)
    return 'fail'
final=set()
while True:
    alldone='ALLDONE' in open(f'{B}/collect.log').read()
    for k in PARTS:
        if k in final: continue
        dur=decode(k); S=sils(k)
        cuts=[0.0]
        while True:
            want=cuts[-1]+TG
            if want+60>dur and not alldone: break
            if dur-cuts[-1]<TG*1.3 and alldone: break
            near=[s for s in S if want-90<s<want+60]
            cuts.append(min(near,key=lambda s:abs(s-want)) if near else want)
        if alldone: cuts.append(dur); final.add(k)
        for i in range(len(cuts)-1):
            p=f'{B}/{k}_p{i:02d}'
            if p in jobs: continue
            subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{cuts[i]:.2f}','-to',f'{cuts[i+1]:.2f}','-i',f'{B}/{k}.wav','-ac','1','-ar','16000',p+'.wav'],check=True)
            subprocess.run(['ffmpeg','-v','error','-y','-i',p+'.wav','-c:a','libopus','-b:a','32k',p+'.ogg'],check=True)
            jobs[p]=(ex.submit(gem,p),ex.submit(sar,p))
            json.dump({'cuts':cuts},open(f'{B}/{k}_cuts.json','w'))
            print(time.strftime('%H:%M:%S'),'piece',p,f'{cuts[i]:.0f}-{cuts[i+1]:.0f}',flush=True)
    st={p:(g.done() and g.result(), s.done() and s.result()) for p,(g,s) in jobs.items()}
    if len(final)==len(PARTS) and all(g and s for g,s in st.values()):
        print('ALLPIECES',json.dumps(st),flush=True); break
    time.sleep(120)
