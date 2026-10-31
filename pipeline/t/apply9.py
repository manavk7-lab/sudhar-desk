"""apply9.py doc.txt kept.json out_text review_items.json judge1.json judge2.json ...
Applies fix/maybe decisions to the backbone, writes new text and review items (applied + check)."""
import sys,json,re,hashlib
doc=open(sys.argv[1],encoding='utf-8').read(); K={it['id']:it for it in json.load(open(sys.argv[2],encoding='utf-8'))}
out_text,out_rev=sys.argv[3],sys.argv[4]
J=[]
for p in sys.argv[5:]: J+=json.load(open(p,encoding='utf-8'))
dec={}
for j in J:
    if j.get('id') in K and j.get('d') in ('fix','maybe','ask'): dec[j['id']]=j
# build edits (pos,end,newtext)
edits=[]
for i,j in dec.items():
    it=K[i]; pos,end=it['pos'],it['end']; txt=(j.get('text') or '').strip()
    old=doc[pos:end]
    if pos==end:
        if not txt: continue
        new=' '+txt
    else:
        new=txt
    if '\n\n' in old:
        if '  ' in new: new=new.replace('  ','\n\n',1)
        else: print('paragraph break would be lost, skipped',i); continue
    if '\n\n' not in old: new=re.sub(' +',' ',new)
    if new.strip()==old.strip(): continue
    edits.append((pos,end,new,j,it))
edits.sort(key=lambda e:e[0])
# drop overlaps
clean=[];last=-1
for e in edits:
    if e[0]<last: print('overlap skip',e[3]['id']); continue
    clean.append(e); last=e[1]
# apply (only fix/maybe); remember spans in new text
apply=[e for e in clean if e[3]['d'] in ('fix','maybe')]
ask=[e for e in clean if e[3]['d']=='ask']
new=doc; shift=0; spans=[]
pieces=[];prev=0
for pos,end,txt,j,it in apply:
    seg_old=doc[pos:end]
    if txt=='' :
        # deletion: also remove one neighbouring space
        if end<len(doc) and doc[end]==' ': end2=end+1
        elif pos>0 and doc[pos-1]==' ': pos=pos-1; end2=end
        else: end2=end
        pieces.append(doc[prev:pos]); spans.append((sum(len(p) for p in pieces),0,doc[pos:end2],'',j,it)); prev=end2
    else:
        pieces.append(doc[prev:pos]); st=sum(len(p) for p in pieces); pieces.append(txt); spans.append((st,len(txt),doc[pos:end],txt,j,it)); prev=end
pieces.append(doc[prev:]); new=''.join(pieces)
open(out_text,'w',encoding='utf-8').write(new)
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def uniq(text,s,e):
    """expand [s,e) by words until the snippet is unique in text"""
    a,b=s,e
    for _ in range(12):
        snip=text[a:b]
        if snip.strip() and len(re.findall(flex(snip),text))==1 and len(snip.split())>=3: return a,b
        # grow both sides by one word
        na=text.rfind(' ',0,max(0,a-1)); a=0 if na<0 else na+1
        nb=text.find(' ',b+1); b=len(text) if nb<0 else nb
    return a,b
items=[]
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
def heard(it): return ' · '.join(f"{ {'S':'Sarvam','G':'Gemini'}[k]}: {v}" for k,v in it['read'].items() if k in ('S','G') and v is not None)
for st,ln,oldseg,txt,j,it in spans:
    a,b=uniq(new,st,st+ln)
    cur=new[a:b]; alt=new[a:st]+oldseg+new[st+ln:b]
    if txt=='' : alt=new[a:st]+oldseg+new[st:b]
    items.append({'id':hid(cur,alt),'cur':cur.strip(),'alt':re.sub(r'\s+',' ',alt).strip(),'kind':'applied','conf':'sure' if j['d']=='fix' else 'likely',
                  'why':j.get('why',''),'heard':heard(it),'t':it.get('t')})
# ask items: locate original span in new text (shifted)
def newpos(p):
    d=0
    for st,ln,oldseg,txt,j,it in spans:
        if it['pos']<p: d+=ln-len(oldseg)
    return p+d
for pos,end,txt,j,it in ask:
    s=newpos(pos); e=s+(end-pos)
    a,b=uniq(new,s,e); cur=new[a:b]; alt=new[a:s]+txt+new[e:b]
    items.append({'id':hid(cur,alt),'cur':cur.strip(),'alt':re.sub(r'\s+',' ',alt).strip(),'kind':'check','conf':'unsure','why':j.get('why',''),'heard':heard(it),'t':it.get('t')})
json.dump(items,open(out_rev,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
import collections
print('applied',len(apply),collections.Counter(e[3]['d'] for e in apply),'ask',len(ask),'chars',len(doc),'->',len(new))
