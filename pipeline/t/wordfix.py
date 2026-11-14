"""wordfix.py text.txt items.json spec.json sync.tsv — late word fixes (book spellings, a typo) on the final text.
spec.json: [[old, new, why, conf], ...]; every occurrence of `old` (plain text, not regex) becomes `new`.
Each change gets its own ✎ item (two words of context each side). If the change falls inside an existing item's cur,
that item is updated instead (cur changes, alt stays the Doc text), so no two items overlap.
Writes text.txt and items.json in place; prints what it did. Run overlapcheck/revertcheck afterwards."""
import json,re,sys,hashlib,subprocess,os
T,I,SP,SY=sys.argv[1:5]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8')); spec=json.load(open(SP,encoding='utf-8'))
def span(x,txt):
    p=txt.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 else None
new_items=[]
for old,new,why,conf in spec:
    while True:
        m=re.search(re.escape(old),t)
        if not m: break
        s,e=m.start(),m.end()
        host=None
        for x in it+new_items:
            sp=span(x,t)
            if sp and sp[0]<e and sp[1]>s: host=x; break
        if host:
            sp=span(host,t)
            host['cur']=t[sp[0]:s]+new+t[e:sp[1]]
            host['why']=(host.get('why','')+'; '+why).strip('; ')
            t=t[:s]+new+t[e:]
            print('in item',host['id'],'|',host['cur'][:90])
            continue
        # two words of context, stopping at a line break
        L=s
        for _ in range(2):
            j=t.rfind(' ',0,L-1) if L>0 else -1
            nl=t.rfind('\n',0,L-1) if L>0 else -1
            if nl>j: L=nl+1; break
            L=j+1 if j>=0 else 0
            if j<0: break
        R=e
        for _ in range(2):
            j=t.find(' ',R+1); nl=t.find('\n',R+1)
            if j<0: j=len(t)
            if 0<=nl<j: R=nl; break
            R=j
        alt=t[L:R]; cur=t[L:s]+new+t[e:R]
        t=t[:s]+new+t[e:]
        x={'id':hashlib.md5(('wf'+cur+str(s)).encode()).hexdigest()[:8],'cur':cur,'alt':alt,'kind':'applied','conf':conf,'why':why,'heard':''}
        new_items.append(x); print('new',repr(alt),'->',repr(cur))
for x in new_items: assert t.count(x['cur'])==1,('not unique',x['cur'])
open(T,'w',encoding='utf-8').write(t)
tmp=I+'.wf.json'; json.dump(new_items,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
here=os.path.dirname(os.path.abspath(__file__))
subprocess.run(['python3',os.path.join(here,'addtimes.py'),T,SY,tmp],check=True)
it+=json.load(open(tmp,encoding='utf-8')); os.remove(tmp)
json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('items',len(it))
