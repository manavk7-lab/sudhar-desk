"""fixalt.py items.json before.txt [out.json] — give back the paragraph breaks an item's alt lost: where an item's alt
(words) occurs exactly once in the text before the change, with a line break inside, take that exact text as alt.
Works on a review list ({"items":[…]}) or a plain item list. Writes in place unless out.json is given."""
import json,re,sys
p=sys.argv[1]; before=re.sub(r'["“”]','',open(sys.argv[2],encoding='utf-8').read()); out=sys.argv[3] if len(sys.argv)>3 else p
D=json.load(open(p,encoding='utf-8')); I=D['items'] if isinstance(D,dict) else D
n=0
for it in I:
    a=it.get('alt','')
    if '\n' in a or len(a.split())<2: continue
    m=list(re.finditer(r'\s+'.join(re.escape(w) for w in a.split()),before))
    if len(m)==1 and '\n' in m[0].group(0): it['alt']=m[0].group(0); n+=1; print('fixed',repr(a[:50]))
json.dump(D,open(out,'w',encoding='utf-8'),ensure_ascii=False,**({'separators':(',',':')} if isinstance(D,dict) else {'indent':0})); print('alts fixed',n)
