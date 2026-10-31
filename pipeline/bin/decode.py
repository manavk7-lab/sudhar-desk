"""decode.py partsdir out.webm  — parts NNNN, last part of each 60s chunk starts with '|'"""
import sys,os,base64
d,out=sys.argv[1],sys.argv[2]
names=sorted(n for n in os.listdir(d) if n.isdigit())
idx=[int(n) for n in names]
assert idx==list(range(len(idx))), ('gap', sorted(set(range(max(idx)+1))-set(idx)))
buf='';bs=b'';nch=0
for n in names:
    s=open(os.path.join(d,n)).read()
    if s.startswith('|'):
        buf+=s[1:]; bs+=base64.b64decode(buf); buf=''; nch+=1
    else: buf+=s
if buf: print('trailing incomplete chunk of',len(buf),'chars (skipped)')
open(out,'wb').write(bs); print(out,len(bs),'bytes',nch,'chunks')
