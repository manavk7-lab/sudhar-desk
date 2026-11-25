"""sadhana_book.py NAME FIRST_PARA NEXT_PARA — book files for one Upanishad from the CORRECTED સાધનાખંડ Word file
(gks/paras.json + gks/fix/edits.jsonl, the page-by-page correction against the scan, 25 Nov):
book_sk/NAME.txt (all lines, Sanskrit in Gujarati script), NAME_gu.txt (Gujarati lines only), NAME_verses.json, NAME_clean.txt ([S]/[G])."""
import json,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from deva2gu import conv
GK='/tmp/claude-0/-home-claude/bff094fd-345e-5cb3-95d4-5a521bc4ad84/scratchpad/gks'
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
P=json.load(open(GK+'/paras.json',encoding='utf-8'))
E=[json.loads(l) for l in open(GK+'/fix/edits.jsonl',encoding='utf-8') if l.strip() and not l.startswith('#')]
T=[p.get('text') for p in P]; dele=set(); ins={}; bef={}
for e in E:
    if 'old' in e:
        t=T[e['p']]
        if e.get('all'): T[e['p']]=t.replace(e['old'],e['new']); continue
        k=e.get('n',0); idx=[m.start() for m in re.finditer(re.escape(e['old']),t)]
        if len(idx)<=k: sys.exit('edit not found: '+json.dumps(e,ensure_ascii=False)[:200])
        p=idx[k]; T[e['p']]=t[:p]+e['new']+t[p+len(e['old']):]
    elif 'settext' in e: T[e['settext']]=e['text']
    elif 'ins_after' in e: ins.setdefault(e['ins_after'],[]).append(e['text'])
    elif 'ins_before' in e: bef.setdefault(e['ins_before'],[]).append(e['text'])
    elif 'del' in e: dele.add(e['del'])
seq=[]
for i in range(a,b):
    seq+=bef.get(i,[])
    if i not in dele and T[i] is not None: seq.append(T[i])
    seq+=ins.get(i,[])
paras=[]
for t in seq:
    if re.fullmatch(r'\s*પૃષ્ઠ [૦-૯–\s]+\s*',t or ''): paras.append(None); continue
    paras.append(t)
# join a paragraph that a page marker split in the middle of a sentence
out=[]; join=False
for t in paras:
    if t is None:
        join = bool(out) and not re.search(r'[.।॥?!)]\s*$',out[-1]); continue
    if join and out: out[-1]=out[-1].rstrip()+' '+t.lstrip()
    else: out.append(t)
    join=False
def deva(s): d=sum(1 for c in s if 'ऀ'<=c<='ॿ' and c not in '।॥'); g=sum(1 for c in s if '઀'<=c<='૿'); return d>g
clean=[]
for t in out:
    for l in t.split('\n'):
        l=l.strip()
        if l: clean.append(('[S] ' if deva(l) else '[G] ')+l)
os.makedirs(W+'/book_sk',exist_ok=True)
open(f'{W}/book_sk/{name}_clean.txt','w',encoding='utf-8').write('\n'.join(clean)+'\n')
full=[];gu=[];verses=[];cur=[]
for l in clean:
    if l.startswith('[S] '):
        s=l[4:].strip(); full.append(conv(s)); cur.append(s)
        if re.search(r'॥\s*[०-९\d]+[-०-९\d,]*\s*॥\s*$',s) or re.search(r'शान्तिः\s*॥\s*$',s):
            d=' '.join(cur); verses.append({'n':len(verses),'deva':d,'gu':conv(d)}); cur=[]
    else:
        g=l[4:].strip(); full.append(g); gu.append(g)
if cur: d=' '.join(cur); verses.append({'n':len(verses),'deva':d,'gu':conv(d)})
open(f'{W}/book_sk/{name}.txt','w',encoding='utf-8').write('\n'.join(full)+'\n')
open(f'{W}/book_sk/{name}_gu.txt','w',encoding='utf-8').write('\n'.join(gu)+'\n')
json.dump(verses,open(f'{W}/book_sk/{name}_verses.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(name,'paras',a,'-',b-1,'lines',len(full),'gu',len(gu),'verses',len(verses),'| first:',(full[0] if full else '')[:40],'| last:',(full[-1] if full else '')[:50])
