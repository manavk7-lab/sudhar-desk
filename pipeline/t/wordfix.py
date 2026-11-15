"""wordfix.py text.txt items.json spec.json sync.tsv — late word fixes (book spellings, a typo) on the final text.
spec.json: [[old, new, why, conf], ...]; every occurrence of `old` (plain text, not regex) becomes `new`.
Each change gets its own ✎ item (two words of context each side). If the change falls inside an existing item's cur,
that item is updated instead (cur changes, alt stays the Doc text), so no two items overlap.
Writes text.txt and items.json in place; prints what it did. Run overlapcheck/revertcheck afterwards."""
import json,re,sys,hashlib,subprocess,os
T,I,SP,SY=sys.argv[1:5]
t=open(T,encoding='utf-8').read(); it=json.load(open(I,encoding='utf-8')); spec=json.load(open(SP,encoding='utf-8'))
def span(x,txt):
    if '_p' in x: return (x['_p'],x['_q'])
    p=txt.find(x['cur']); return (p,p+len(x['cur'])) if p>=0 else None
new_items=[]
for old,new,why,conf in spec:
    pos=0
    while True:                                     # search after the last change: new may contain old
        m=re.compile(re.escape(old)).search(t,pos)
        if not m: break
        pos=m.start()+len(new)
        s,e=m.start(),m.end()
        host=None
        for x in it+new_items:
            sp=span(x,t)
            if sp and sp[0]<e and sp[1]>s: host=x; break
        if host:
            sp=span(host,t)
            # the change may stick out of the item on either side: the item grows to cover both
            U0,U1=min(s,sp[0]),max(e,sp[1])
            if host.get('kind')=='check':     # a listen-note: its alt is a suggestion, so the item becomes an applied one
                host['alt']=t[U0:U1]; host['kind']='applied'
            else:
                host['alt']=t[U0:sp[0]]+host['alt']+t[sp[1]:U1]
            t=t[:s]+new+t[e:]; [x.update(_p=x['_p']+len(new)-(e-s) if x['_p']>=e else x['_p'],_q=x['_q']+len(new)-(e-s) if x['_q']>=e else x['_q']) for x in new_items]
            host['cur']=t[U0:U1+len(new)-(e-s)]
            V0,V1=U0,U1+len(new)-(e-s)
            for _ in range(6):                      # widen the host until its cur is unique again
                if t.count(host['cur'])==1: break
                j=t.rfind(' ',0,V0-1); nV0=j+1 if j>=0 else 0
                j=t.find(' ',V1+1); nV1=len(t) if j<0 else j
                host['alt']=t[nV0:V0]+host['alt']+t[V1:nV1]; V0,V1=nV0,nV1; host['cur']=t[V0:V1]
            if '_p' in host: host['_p'],host['_q']=V0,V1
            host['why']=(host.get('why','')+'; '+why).strip('; ')
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
        for x in it+new_items:                      # the context must not run into another item
            sp=span(x,t)
            if not sp: continue
            if sp[1]<=s and sp[1]>L: L=sp[1]+(1 if t[sp[1]:sp[1]+1]==' ' else 0)
            if sp[0]>=e and sp[0]<R: R=sp[0]-(1 if t[sp[0]-1:sp[0]]==' ' else 0)
        t2=t[:s]+new+t[e:]; d=len(new)-(e-s)
        for _ in range(6):                          # widen until the new cur is unique in the changed text
            if t2.count(t2[L:R+d])==1: break
            j=t.rfind(' ',0,L-1); L=j+1 if j>=0 else 0
            j=t.find(' ',R+1); R=len(t) if j<0 else j
        alt=t[L:R]; cur=t[L:s]+new+t[e:R]
        [x.update(_p=x['_p']+d if x['_p']>=e else x['_p'],_q=x['_q']+d if x['_q']>=e else x['_q']) for x in new_items]; t=t2
        x={'id':hashlib.md5(('wf'+cur+str(s)).encode()).hexdigest()[:8],'cur':cur,'alt':alt,'kind':'applied','conf':conf,'why':why,'heard':''}
        x['_p']=L; x['_q']=L+len(cur); new_items.append(x); print('new',repr(alt),'->',repr(cur))
for x in new_items:                                 # widen any new item whose cur a later change made non-unique
    p,q=x['_p'],x['_q']; assert t[p:q]==x['cur'],('lost',x['cur'])
    k=0
    while t.count(t[p:q])>1 and k<8:
        j=t.rfind(' ',0,p-1); np_=j+1 if j>=0 else 0
        j=t.find(' ',q+1); nq=len(t) if j<0 else j
        x['alt']=t[np_:p]+x['alt']+t[q:nq]; p,q=np_,nq; k+=1
    x['cur']=t[p:q]; del x['_p'],x['_q']
    assert t.count(x['cur'])==1,('not unique',x['cur'])
open(T,'w',encoding='utf-8').write(t)
tmp=I+'.wf.json'; json.dump(new_items,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
here=os.path.dirname(os.path.abspath(__file__))
if not os.environ.get('NOTIMES'): subprocess.run(['python3',os.path.join(here,'addtimes.py'),T,SY,tmp],check=True)
it+=json.load(open(tmp,encoding='utf-8')); os.remove(tmp)
json.dump(it,open(I,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('items',len(it))
