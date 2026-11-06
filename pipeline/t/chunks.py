"""chunks.py text.txt [size] — split a text at line ends into chunks of about `size` chars; print each chunk's line range
(1-based, as the Read tool numbers them), length and sha16, for posting through the Sudhar Desk tab in pieces."""
import sys,hashlib
t=open(sys.argv[1],encoding='utf-8').read(); size=int(sys.argv[2]) if len(sys.argv)>2 else 2600
L=t.split('\n'); ch=[]; cur=[]; n=0
for i,l in enumerate(L,1):
    if cur and n+len(l)>size: ch.append(cur); cur=[]; n=0
    cur.append(i); n+=len(l)+1
ch.append(cur)
parts=[]
for k,c in enumerate(ch):
    s='\n'.join(L[i-1] for i in c)+('\n' if k<len(ch)-1 else '')
    parts.append(s); print(k,f'lines {c[0]}-{c[-1]}',len(s),hashlib.sha256(s.encode()).hexdigest()[:16])
assert ''.join(parts)==t; print('total',len(t),hashlib.sha256(t.encode()).hexdigest()[:16])
