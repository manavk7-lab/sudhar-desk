"""backbone_u1.py doc0.txt out_doc.txt out_rev.json yt.tsv
Upanishad 1: remove quotation marks (Manav's standing request), brackets, and apply the RULES.md section 2 spellings.
Spelling/bracket fixes become 'auto' items on the check list (quotes are not listed: 231 of them, all trivial)."""
import re,sys,json,hashlib,subprocess,os
S=os.path.dirname(os.path.abspath(__file__))
src,out,outr,tsv=sys.argv[1:5]
t=open(src,encoding='utf-8').read()
G='઀-૿'
# 1. quotation marks
t=t.replace('"','')
t=re.sub(r"(?<=[{0}])'(?=તી|તું|તા|તો)".format(G),' ',t)          # કીધી'તી -> કીધી તી
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' +\n','\n',t); t=re.sub(r'\n +','\n',t)
t=re.sub(r' ([,.?!:;])',r'\1',t)
# 2. rule edits, recorded so they can be listed
rules=[]   # (pattern, replacement, why)
def W(w): return r'(?<![{0}]){1}(?![{0}])'.format(G,re.escape(w))
rules+= [(W('અહિયા'),'અહીંયા','spelling: અહીંયા'),(W('કાઈ'),'કંઈ','spelling: કંઈ'),(W('કઈક'),'કંઈક','spelling: કંઈક'),
         (r'(?<![{0}])કઈ કઈ આવતું'.format(G),'કંઈ કંઈ આવતું','spelling: કંઈ (something), not કઈ (which)'),
         (W('હારું'),'સારું','spelling: સારું')]
# brackets: the speaker's asides, keep the words, drop the brackets
rules+= [(r'હવિશ્યતી \((હવી એટલે [^)]*?)\),','હવિશ્યતી, \\1,','no brackets (aside spoken as is)'),
         (r'કરું છું \((આપણામાં [^)]*?)\)\.','કરું છું. \\1.','no brackets (aside spoken as is)'),
         (r'કરીને \((સમસ્ત ભાવો એટલે [^)]*?)\),','કરીને, \\1,','no brackets (aside spoken as is)'),
         (r'મથવાથી \((એ આપ એટલે [^)]*?)\) ','મથવાથી, \\1, ','no brackets (aside spoken as is)')]
edits=[]
for pat,rep,why in rules:
    for m in re.finditer(pat,t):
        edits.append((m.start(),m.end(),m.expand(rep),why))
edits.sort()
for a,b in zip(edits,edits[1:]): assert a[1]<=b[0],(a,b)
pieces=[];prev=0;spans=[]
for s,e,new,why in edits:
    pieces.append(t[prev:s]); st=sum(len(p) for p in pieces); pieces.append(new); spans.append((st,len(new),t[s:e],new,why)); prev=e
pieces.append(t[prev:]); T=''.join(pieces)
assert '(' not in T and ')' not in T and '"' not in T, 'leftover brackets/quotes'
open(out,'w',encoding='utf-8').write(T)
# times from the captions
subprocess.run(['node',S+'/wordtimes.js',out,tsv,out+'.words'],check=True,capture_output=True)
Wd=json.load(open(out+'.words'))
def tm(pos):
    best=None
    for s,e,ms,m in Wd:
        if s<=pos: best=ms
        else: break
    return best
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def uniq(text,s,e):
    a,b=s,e
    for _ in range(12):
        snip=text[a:b]
        if snip.strip() and len(re.findall(flex(snip),text))==1 and len(snip.split())>=3: return a,b
        na=text.rfind(' ',0,max(0,a-1)); a=0 if na<0 else na+1
        nb=text.find(' ',b+1); b=len(text) if nb<0 else nb
    return a,b
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
items=[]
for st,ln,old,new,why in spans:
    a,b=uniq(T,st,st+ln); cur=T[a:b]; alt=T[a:st]+old+T[st+ln:b]
    items.append({'id':hid(cur,alt),'cur':re.sub(r'\s+',' ',cur).strip(),'alt':re.sub(r'\s+',' ',alt).strip(),'kind':'auto','conf':'sure',
                  'why':why,'heard':'','t':tm(st)})
json.dump(items,open(outr,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
src_t=open(src,encoding='utf-8').read()
print('quotes removed',src_t.count('"'),'apostrophes',src_t.count("'")-T.count("'"),'rule edits',len(items),'chars',len(src_t),'->',len(T),
      'newlines',src_t.count('\n'),T.count('\n'))
for it in items: print(' ',it['t'],it['why'],'|',it['alt'][:70],'=>',it['cur'][:70])
