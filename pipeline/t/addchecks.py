"""addchecks.py VM checks.json — add listen-only ✎ items (kind check): [{"cur": text as it stands in final.txt,
"alt": the suggestion, "why": ...}]. cur must occur once in VM/final.txt."""
import json,re,hashlib,sys
d=sys.argv[1]; C=json.load(open(sys.argv[2],encoding='utf-8'))
def norm(s): return re.sub(r'\s+',' ',s).strip()
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
t=open(f'{d}/final.txt',encoding='utf-8').read()
I=json.load(open(f'{d}/items_all_final.json',encoding='utf-8')); n=0
for c in C:
    if len(re.findall(flex(c['cur']),t))!=1: print('NOT ONCE:',c['cur']); continue
    I.append({'id':hid(norm(c['cur']),norm(c['alt'])),'cur':c['cur'],'alt':c['alt'],'kind':'check','conf':'unsure','why':c['why'],'heard':c.get('heard',''),'t':None}); n+=1
json.dump(I,open(f'{d}/items_all_final.json','w',encoding='utf-8'),ensure_ascii=False,indent=0); print('checks added',n)
