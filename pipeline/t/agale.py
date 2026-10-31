import sys,re,json,difflib,collections; sys.path.insert(0,'t')
from learn import rd
TOKR=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
DOCS={l.split('\t')[0]:l.split('\t')[1].strip() for l in open('learn/docs.tsv')}
HEARD=re.compile(r'^અ?ગા?[ળડ]ે$|^આગા?[ળડ]ે$|^ગાળે$')
out={}
for n in ['fin1','fin2','fin3','fin4','fin5','fin6','cor7','cor8','cor9','cor10','cor11','cor12','cor13']:
    v=n[3:]; text=open(f'today/{n}.txt',encoding='utf-8-sig').read().replace('\r\n','\n')
    W=[(m.start(),m.end(),m.group()) for m in TOKR.finditer(text)]; D=[w[2] for w in W]
    R=TOKR.findall(rd('raw'+v))
    sm=difflib.SequenceMatcher(None,R,D,autojunk=False); eds=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='replace' and i2-i1==j2-j1:
            for k in range(i2-i1):
                r,d=R[i1+k],D[j1+k]
                if d=='આગળ' and HEARD.match(r):
                    j=j1+k; s=W[max(0,j-2)][0]; e=W[min(len(W)-1,j+1)][1]
                    find=text[s:e]
                    if text.count(find)==1: eds.append([find,find[:W[j][0]-s]+'આગળે'+find[W[j][1]-s:],r])
    out[DOCS[n]]=eds; print(n,len(eds),[e[0]+' ← '+e[2] for e in eds])
json.dump({k:[e[:2] for e in v] for k,v in out.items() if v},open('proof/agale.json','w',encoding='utf-8'),ensure_ascii=False)
