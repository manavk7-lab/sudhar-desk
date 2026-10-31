"""splitsil.py in.wav outprefix [target_sec=600] -> outprefix_pNN.ogg pieces cut at silences"""
import sys,subprocess,re
src,pre=sys.argv[1],sys.argv[2]; tg=float(sys.argv[3]) if len(sys.argv)>3 else 600
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout)
log=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=n=-40dB:d=0.4','-f','null','-'],capture_output=True,text=True).stderr
sil=[]; st=None
for l in log.splitlines():
    m=re.search(r'silence_start: ([\d.]+)',l)
    if m: st=float(m.group(1))
    m=re.search(r'silence_end: ([\d.]+)',l)
    if m and st is not None: sil.append((st+float(m.group(1)))/2); st=None
cuts=[0.0]
while dur-cuts[-1]>tg*1.3:
    want=cuts[-1]+tg
    near=[s for s in sil if want-90<s<want+60]
    cuts.append(min(near,key=lambda s:abs(s-want)) if near else want)
cuts.append(dur)
for k in range(len(cuts)-1):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{cuts[k]:.2f}','-to',f'{cuts[k+1]:.2f}','-i',src,'-ac','1','-c:a','libopus','-b:a','32k',f'{pre}_p{k:02d}.ogg'],check=True)
print(' '.join(f'{c:.1f}' for c in cuts))
