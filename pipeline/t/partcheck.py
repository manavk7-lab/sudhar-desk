# For particles Manav added (raw->fin), does each engine's transcript contain them?
import re,sys,difflib,collections
sys.path.insert(0,'t')
def toks(s):
    s=re.sub(r'[\[\]().,!?;:"“”‘’\'।…\-–—]',' ',s); return s.split()
raw,fin=sys.argv[1],sys.argv[2]; engines=sys.argv[3:]
R=toks(open(raw,encoding='utf-8').read()); F=toks(open(fin,encoding='utf-8').read())
P={'છે','કે','ય','એ','છું','છો','નથી','જ','તો','છીએ','કહે'}
added=[]  # (fin index, word, kind)
sm=difflib.SequenceMatcher(None,R,F,autojunk=False)
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=='insert':
        for j in range(j1,j2):
            if F[j] in P: added.append((j,F[j]))
    elif op=='replace' and i2-i1==j2-j1:
        for k,(x,y) in enumerate(zip(R[i1:i2],F[j1:j2])):
            if y.startswith(x) and y[len(x):]=='ય': added.append((j1+k,'+ય'))
print('particles added by Manav:',len(added),collections.Counter(w for _,w in added).most_common())
for e in engines:
    name,path=e.split('=')
    E=toks(open(path,encoding='utf-8').read())
    m=difflib.SequenceMatcher(None,F,E,autojunk=False)
    eq=set()
    for op,i1,i2,j1,j2 in m.get_opcodes():
        if op=='equal': eq.update(range(i1,i2))
    hit=collections.Counter(); tot=collections.Counter()
    for j,w in added:
        tot[w]+=1
        if j in eq: hit[w]+=1
    print(name, 'caught', sum(hit.values()),'/',len(added), {w:f'{hit[w]}/{tot[w]}' for w in tot})
