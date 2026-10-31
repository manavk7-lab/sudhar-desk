import json,glob,re,collections,sys
sys.path.insert(0,'t')
TOKR=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
DIAL={('જાઓ','જાવ'),('થાઓ','થાવ'),('પણ','બી'),('ભાઈ','ભઈ'),('કોઈક','કોક'),('કોઈ','કોક'),('હતું','તું'),('તહીં','તઈ'),('ત્યાં','તઈ'),('કહે','કે'),('રહે','રે'),('આવ્યા','આયા'),('આવ્યો','આયો'),('હતી','તી'),('હતા','તા'),('કહેવું','કેવું')}
def wdiff(a,b):
    A=TOKR.findall(a);B=TOKR.findall(b)
    import difflib
    out=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,B,autojunk=False).get_opcodes():
        if op!='equal': out.append((' '.join(A[i1:i2]),' '.join(B[j1:j2])))
    return out
allE=[];st=collections.Counter()
for mf in sorted(glob.glob('proof/v*_meta.json')):
    name=mf.split('/')[-1][:-10]; meta=json.load(open(mf,encoding='utf-8'))
    try: E=json.load(open(f'proof/{name}_edits.json',encoding='utf-8'))
    except Exception as e: print('MISSING',name,e); continue
    chunk=open(f'proof/{name}.txt',encoding='utf-8').read()
    full=open(f"learn/cor{meta['video']}.txt",encoding='utf-8-sig').read().replace('\r\n','\n')
    for e in E:
        f=e.get('find','');r=e.get('replace','')
        if f==r or chunk.count(f)!=1: st['bad_find']+=1; continue
        d=wdiff(f,r)
        if not d: st['punct_only']+=1; continue
        if all((x,y) in DIAL for x,y in d): st['dialect_revert_dropped']+=1; continue
        pos=meta['offset']+chunk.index(f)
        assert full[pos:pos+len(f)]==f
        e2=dict(e,video=meta['video'],yt=meta['yt'],pos=pos,uniq=full.count(f)==1,changes=d)
        allE.append(e2); st[e['conf']]+=1
print(st, len(allE))
json.dump(allE,open('proof/all_edits.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(collections.Counter((e['video'],e['conf']) for e in allE))
print('non-unique in full doc:',sum(1 for e in allE if not e['uniq']))
