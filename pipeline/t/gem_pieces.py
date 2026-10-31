"""gem_pieces.py keyfile model out.txt piece1.ogg piece2.ogg ... (parallel, retries)"""
import sys,subprocess,os,concurrent.futures as cf,time
key,model,out=sys.argv[1:4]; P=sys.argv[4:]
def run(p):
    o=p+'.gem.txt'
    for a in range(4):
        if os.path.exists(o) and os.path.getsize(o)>2000: return o
        r=subprocess.run([sys.executable,'t/run_gemini.py',key,model,p,o],capture_output=True,text=True)
        if os.path.exists(o) and os.path.getsize(o)>2000: return o
        print('retry',p,a,(r.stderr or r.stdout)[-300:],flush=True); time.sleep(20*(a+1))
    return o
with cf.ThreadPoolExecutor(5) as ex: outs=list(ex.map(run,P))
txt='\n'.join(open(o,encoding='utf-8').read().strip() if os.path.exists(o) else '' for o in outs)
open(out,'w',encoding='utf-8').write(txt); print(out,len(txt),'chars',[os.path.getsize(o) if os.path.exists(o) else 0 for o in outs])
