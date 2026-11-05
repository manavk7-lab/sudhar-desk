"""manualgen.py text.txt spec.json out.json — build manual ✎ items on the CURRENT text.
spec: list of [pattern, replacement, why, conf, mode]; mode 'once' = literal text that must occur once (pattern = alt,
replacement = cur); mode 'all' = regex, every match becomes its own item with a unique context (no paragraph crossing).
Items are built in order on the evolving text, so mantra_apply.py applies them cleanly in the same order."""
import json,re,sys
t=open(sys.argv[1]).read(); spec=json.load(open(sys.argv[2])); out=[]; bad=[]
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
for pat,rep,why,conf,mode in spec:
    if mode=='once':
        ms=list(re.finditer('(?=('+flex(pat)+'))',t))
        if len(ms)!=1: bad.append((pat,len(ms))); continue
        s,e=ms[0].span(1); a=t[s:e]
        out.append({'alt':a,'cur':rep,'why':why,'conf':conf}); t=t[:s]+rep+t[e:]; continue
    i=0; n=0
    while True:
        m=re.compile(pat).search(t,i)
        if not m: break
        s,e=m.span(); new=m.expand(rep)
        ls=t.rfind('\n',0,s)+1; le=t.find('\n',e); le=len(t) if le<0 else le
        for k in range(1,12):
            x=s-10*k
            if x<=ls: a0=ls
            else:
                j=t.rfind(' ',ls,x); a0=j+1 if j>=0 else ls
            y=e+10*k
            if y>=le: a1=le
            else:
                j=t.find(' ',y,le); a1=j if j>=0 else le
            a=t[a0:a1]
            if len(re.findall('(?='+re.escape(a)+')',t))==1: break
        cur=re.sub(pat,rep,a)  # every match inside this context goes into the same item
        out.append({'alt':a,'cur':cur,'why':why,'conf':conf}); t=t[:a0]+cur+t[a1:]; i=a0+len(cur); n+=1
    if n==0: bad.append((pat,0))
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=0)
print('items',len(out),'not applied',bad)
