"""applypunct.py text.txt pc.json out_text out_rev.json decisions1.json [decisions2.json ...]"""
import sys,json,re,hashlib
txt=open(sys.argv[1],encoding='utf-8').read(); B=json.load(open(sys.argv[2],encoding='utf-8')); out_t,out_r=sys.argv[3],sys.argv[4]
D=[]
for p in sys.argv[5:]: D+=json.load(open(p,encoding='utf-8'))
ch=[]
for d in D:
    b=B.get(d.get('id'))
    if not b or d.get('p') not in ('.','?','',','): continue
    if d['p']==b['cur']: continue
    ch.append((b['pos'],b['end'],d['p'],b,d))
ch.sort(key=lambda x:x[0])
# build new text
pieces=[];prev=0;newpos={}
for pos,end,p,b,d in ch:
    sep=txt[pos:end]
    if '\n' in sep: continue
    core=re.sub(r'[.,?!]','',sep)
    if not re.search(r'\s',core): core=' '+core.strip()
    pieces.append(txt[prev:pos]); start=sum(len(x) for x in pieces); newsep=p+core
    pieces.append(newsep); newpos[pos]=(start,start+len(newsep)); prev=end
pieces.append(txt[prev:]); new=''.join(pieces)
assert re.sub(r'[\s.,?!]','',new)==re.sub(r'[\s.,?!]','',txt), 'words changed!'
open(out_t,'w',encoding='utf-8').write(new)
# map old char pos -> new char pos (shift)
shifts=[]  # (old_pos, delta)
delta=0
for pos,end,p,b,d in ch:
    if pos not in newpos: continue
    s,e=newpos[pos]; delta_here=(e-s)-(end-pos); shifts.append((end,delta_here))
def mp(x):
    return x+sum(dl for o,dl in shifts if o<=x)
# group changes within 60 chars
groups=[]
for c in ch:
    if c[0] not in newpos: continue
    if groups and c[0]-groups[-1][-1][0]<60: groups[-1].append(c)
    else: groups.append([c])
def wb(t,x,n,back):
    # expand x by n words
    y=x
    for _ in range(n):
        if back:
            m=re.search(r'\S+\s*$',t[:y]); y=m.start() if m else 0
        else:
            m=re.match(r'\s*\S+',t[y:]); y=y+m.end() if m else len(t)
    return y
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
items=[]
for g in groups:
    o0=wb(txt,g[0][0],3,True); o1=wb(txt,g[-1][1],3,False)
    n0=mp(o0); n1=mp(o1)
    cur=new[n0:n1].strip(); alt=txt[o0:o1].strip()
    k=0
    while len(re.findall(flex(cur),new))!=1 and k<6:
        o0=wb(txt,o0,1,True); o1=wb(txt,o1,1,False); n0=mp(o0); n1=mp(o1); cur=new[n0:n1].strip(); alt=txt[o0:o1].strip(); k+=1
    kinds=[('dot moved' if any(x[2]=='' for x in g) and any(x[2] in '.?' and x[2] for x in g) else
            ('dot added at a pause' if all(x[2] in ('.','?') for x in g) else ('dot removed (no pause)' if all(x[2]=='' for x in g) else 'punctuation by pause')))]
    pz=max((x[3]['pause'] or 0) for x in g)
    items.append({'id':hashlib.md5((cur+'|'+alt).encode()).hexdigest()[:8],'cur':re.sub(r'\s+',' ',cur),'alt':re.sub(r'\s+',' ',alt),'kind':'applied','conf':'likely',
                  't':g[0][3].get('t'),'why':f"{kinds[0]} — speaker pauses {pz:.1f}s; "+'; '.join(x[4].get('why','') for x in g)[:120]})
json.dump(items,open(out_r,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('changes',len(ch),'groups/items',len(items),'chars',len(txt),'->',len(new))
print('old sha',hashlib.sha256(txt.encode()).hexdigest()[:16],'new sha',hashlib.sha256(new.encode()).hexdigest()[:16])
