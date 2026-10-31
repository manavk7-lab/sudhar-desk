"""backbone_m.py VM doc_orig.txt out_doc.txt out_rev.json yt.tsv
ઉપનિષદ - 40/41 (Maitreya): remove quotation marks, brackets -> commas, join paragraphs that break mid-sentence (RULES 12),
section-2 spellings. Every change except the quotes becomes an 'auto' item on the ✎ list."""
import re,sys,json,hashlib,subprocess,os
S=os.path.dirname(os.path.abspath(__file__))
vm,src,out,outr,tsv=sys.argv[1:6]
t=open(src,encoding='utf-8').read()
G='઀-૿'
# per-Doc fixes: (exact old, new, why)
FIX={'vm1':[
  ('જ્ઞાન યજ્ઞ દ્વારા (આજે થાય છે તેને જ્ઞાન યજ્ઞ કીધો) યજ્ઞ રૂપ','જ્ઞાન યજ્ઞ દ્વારા, આજે થાય છે તેને જ્ઞાન યજ્ઞ કીધો, યજ્ઞ રૂપ','no brackets (aside spoken as is)'),
  ('દ્રુત ક્રીડા (ક્રીડા એટલે કે જુગાર) અને','દ્રુત ક્રીડા, ક્રીડા એટલે કે જુગાર, અને','no brackets (aside spoken as is)'),
  ('રત રહેવાથી.\n\nજ્યારે સત્,','રત રહેવાથી જ્યારે સત્,','paragraph joined: the sentence carries on'),
  ('રસ્તો એમનો.\n\nતંત્રનો છે,','રસ્તો એમનો તંત્રનો છે,','paragraph joined: the sentence carries on'),
  ('એ દેહ જ...\n\nજો આવો','એ દેહ જ જો આવો','paragraph joined: the sentence carries on'),
  ('કેવું ફીલ કરતો.\n\nહોય એનાથી','કેવું ફીલ કરતો હોય એનાથી','paragraph joined: the sentence carries on'),
 ],'vm2':[
  ('ઈચ્છાઓ (થોડી વાત કરી હતી ને કાલે) એ','ઈચ્છાઓ, થોડી વાત કરી હતી ને કાલે, એ','no brackets (aside spoken as is)'),
  ('દ્રવ્ય (એટલે કે ધનના, અન્નના, વસ્ત્રોના અથવા ખ્યાતિના) લોભમાં','દ્રવ્ય, એટલે કે ધનના, અન્નના, વસ્ત્રોના અથવા ખ્યાતિના, લોભમાં','no brackets (aside spoken as is)'),
  ('ખપ્પરમાં (ખોપરીનો અડધો ભાગ હોય ને આમ ખોલેલો તેવા ભાગની અંદર) માંગીને','ખપ્પરમાં, ખોપરીનો અડધો ભાગ હોય ને આમ ખોલેલો તેવા ભાગની અંદર, માંગીને','no brackets (aside spoken as is)'),
  ('તોડાવવા માટે સાત...\n\nઘરે રોજ','તોડાવવા માટે સાત ઘરે રોજ','paragraph joined: the sentence carries on'),
  ('સંસારમાં કોઈનો\n\nવિશ્વાસ નહીં','સંસારમાં કોઈનો વિશ્વાસ નહીં','paragraph joined: the sentence carries on'),
  ('પણ કંઈ...\n\nજુએ નહીં','પણ કંઈ જુએ નહીં','paragraph joined: the sentence carries on'),
  ('કિશોર બની.\n\nજાય છે.','કિશોર બની જાય છે.','paragraph joined: the sentence carries on'),
  ('સંવાદ વર્ણવેલો.\n\nજેમાં સન્યાસ','સંવાદ વર્ણવેલો જેમાં સન્યાસ','paragraph joined: the sentence carries on'),
  ('પર પણ વિસર્જન.\n\nકરાય, જળનું','પર પણ વિસર્જન કરાય, જળનું','paragraph joined: the sentence carries on'),
  ('રહેવું હારું.','રહેવું સારું.','spelling: સારું'),
 ]}
# 1. quotation marks (not listed: trivial)
q0=t.count('"')+t.count('“')+t.count('”')
t=re.sub(r'["“”]','',t)
t=re.sub(r"(?<![{0}])'|'(?![{0}])".format(G),'',t)   # 'પરમાત્મા હું જ છું' -> no quotes
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' +\n','\n',t); t=re.sub(r'\n +','\n',t)
t=re.sub(r' ([,.?!:;])',r'\1',t)
spans=[]
for old,new,why in FIX[vm]:
    old2=re.sub(r'["“”]','',old)
    n=t.count(old2); assert n==1,(old2,n)
    i=t.find(old2); t=t[:i]+new+t[i+len(old2):]
    spans.append((i,len(new),old2,new,why))
# shift: later replacements may move earlier spans; recompute positions by search
T=t
assert '(' not in T and ')' not in T and '"' not in T, 'leftover brackets/quotes'
open(out,'w',encoding='utf-8').write(T)
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
for _,ln,old,new,why in spans:
    st=T.find(new); assert st>=0
    a,b=uniq(T,st,st+ln); cur=T[a:b]; alt=T[a:st]+old+T[st+ln:b]
    items.append({'id':hid(cur,alt),'cur':re.sub(r'\s+',' ',cur).strip(),'alt':re.sub(r'\s+',' ',alt).strip(),'kind':'auto','conf':'sure',
                  'why':why,'heard':'','t':tm(st)})
json.dump(items,open(outr,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
src_t=open(src,encoding='utf-8').read()
print(vm,'quotes removed',q0,'fixes',len(items),'chars',len(src_t),'->',len(T),'newlines',src_t.count('\n'),T.count('\n'))
