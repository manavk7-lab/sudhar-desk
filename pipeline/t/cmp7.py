import re,sys,difflib,collections
D=sys.argv[1]; cap=sys.argv[2]
TOK=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
def key(w):
    for a,b in [('‌',''),('‍',''),('ઁ',''),('ં',''),('઼',''),('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ણ','ન'),('ળ','લ')]: w=w.replace(a,b)
    return w.lower()
old=open(D+'/old.txt',encoding='utf-8-sig').read(); gem=open(D+'/gem.txt',encoding='utf-8-sig').read()
caps=[l.rstrip('\n').split('\t',1)[1].strip() for l in open(cap,encoding='utf-8') if l and l[0]!='#' and '\t' in l]
O=TOK.findall(old); G=TOK.findall(gem); C=caps
print('words: old',len(O),'gem',len(G),'captions',len(C))
for name,t in [('old',old),('gem',gem)]:
    print(name,'quotes',sum(t.count(q) for q in '"“”‘’'),"apos",t.count("'"),'parens',t.count('('),'paras',len([p for p in t.split('\n') if p.strip()]),'!',t.count('!'),'?',t.count('?'),':',t.count(':'))
def cmp(A,B,la,lb,show=0):
    sm=difflib.SequenceMatcher(None,[key(x) for x in A],[key(x) for x in B],autojunk=False)
    st=collections.Counter(); ex=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': st['same']+=i2-i1
        elif op=='replace': st['changed_'+la]+=i2-i1; st['changed_'+lb]+=j2-j1; ex.append((op,' '.join(A[i1:i2]),' '.join(B[j1:j2]),i1))
        elif op=='delete': st['only_'+la]+=i2-i1; ex.append((op,' '.join(A[i1:i2]),'',i1))
        else: st['only_'+lb]+=j2-j1; ex.append((op,'',' '.join(B[j1:j2]),i1))
    print(f'--- {la} vs {lb}:',dict(st))
    big=sorted(ex,key=lambda e:-max(len(e[1]),len(e[2])))[:show]
    for e in big: print('  ',e[0],'@',e[3],'|',la,':',e[1][:160],'|',lb,':',e[2][:160])
    return sm
cmp(O,G,'old','gem',25)
cmp(C,O,'cap','old',12)
cmp(C,G,'cap','gem',12)
# three-way: for each disagreement old vs gem, which one matches the captions?
Ck=[key(x) for x in C]
def mapping(A):
    sm=difflib.SequenceMatcher(None,Ck,[key(x) for x in A],autojunk=False)
    m={}
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal':
            for k in range(i2-i1): m[i1+k]=j1+k
    return m
mo=mapping(O); mg=mapping(G)
print('caption words found in old:',len(mo),'gem:',len(mg))
# runs of caption words present in one but missing in other
def runs(a,b,la,lb):
    s=[i for i in range(len(C)) if i in a and i not in b]
    rr=[];st=None;pv=None
    for i in s:
        if st is None: st=pv=i
        elif i<=pv+3: pv=i
        else: rr.append((st,pv)); st=pv=i
    if st is not None: rr.append((st,pv))
    rr=[r for r in rr if r[1]-r[0]>=6]
    print(f'stretches (>=7 words) spoken & in {la} but missing from {lb}:',len(rr))
    for r in rr: print('   cap',r,round(int(open(cap).read().split("\n")[r[0]+1].split("\t")[0])/1000) if False else '', ' '.join(C[r[0]:r[1]+1])[:220])
runs(mo,mg,'old','gem'); runs(mg,mo,'gem','old')
