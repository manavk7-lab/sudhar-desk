"""mantra_apply.py current_doc.txt items.json out.txt applied.json [sep]
Replace each item's alt (old text) with cur (standard mantra text) where alt occurs exactly once in the current Doc.
sep = what joins mantra lines ('\n' by default; pass 'nn' for a blank line between lines, to match the Doc's style)."""
import sys,json,re,hashlib
doc=open(sys.argv[1],encoding='utf-8').read(); items=json.load(open(sys.argv[2],encoding='utf-8'))
sep='\n\n' if len(sys.argv)>5 and sys.argv[5]=='nn' else '\n'
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
done=[];skip=[]
for it in items:
    m=list(re.finditer(flex(it['alt']),doc))
    if len(m)!=1: skip.append(it['why']); continue
    cur=it['cur'].replace('\n',sep)
    a,b=m[0].span(); doc=doc[:a]+cur+doc[b:]
    it=dict(it); it['cur']=cur; done.append(it)
open(sys.argv[3],'w',encoding='utf-8').write(doc)
json.dump(done,open(sys.argv[4],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print('applied',len(done),'skipped',skip,'sha',hashlib.sha256(doc.encode()).hexdigest()[:16])
