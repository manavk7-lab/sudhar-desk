"""parabreaks.py doc.txt sar.txt — paragraph breaks in the Doc where Sarvam reads the words across the break as one
sentence (no . ? ! between them): candidates for RULES 12 joins (check each by reading)."""
import re,sys,difflib
doc=open(sys.argv[1],encoding='utf-8').read(); sar=open(sys.argv[2],encoding='utf-8').read()
def toks(s): return re.findall(r'[^\s]+',s)
def clean(w): return re.sub(r'[.,?!:;।॥…"\'“”‘’()\-–—]','',w)
ST=toks(sar); SC=[clean(w) for w in ST]
paras=[p for p in re.split(r'\n\s*\n',doc)]
pos=0
for i in range(len(paras)-1):
    a=toks(paras[i]); b=toks(paras[i+1])
    if len(a)<2 or len(b)<2: continue
    key=[clean(w) for w in a[-3:]+b[:3]]
    # find best match of the 6-word window in S
    best=None
    for j in range(len(SC)-6):
        win=SC[j:j+6]
        r=difflib.SequenceMatcher(None,key,win).ratio()
        if best is None or r>best[0]: best=(r,j)
    if not best or best[0]<0.6: continue
    j=best[1]; seg=ST[j:j+6]
    # is there a sentence end in S between word 3 and 4 of the window (allow ±1 shift)?
    mid=' '.join(ST[j+1:j+4])
    stop=bool(re.search(r'[.?!।]',' '.join(ST[j+1:j+4])))
    if not stop:
        print(f'{i:3d} ratio={best[0]:.2f} DOC: …{" ".join(a[-5:])} ¶ {" ".join(b[:5])}…')
        print('      S: …'+' '.join(ST[max(0,j-3):j+9])+'…')
