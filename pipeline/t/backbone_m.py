"""backbone_m.py VM doc_orig.txt out_doc.txt out_rev.json yt.tsv
ઉપનિષદ - 40/41 (Maitreya): remove quotation marks, brackets -> commas, join paragraphs that break mid-sentence (RULES 12),
section-2 spellings. Every change except the quotes becomes an 'auto' item on the ✎ list."""
import re,sys,json,hashlib,subprocess,os
S=os.path.dirname(os.path.abspath(__file__))
vm,src,out,outr,tsv=sys.argv[1:6]
t=open(src,encoding='utf-8').read()
G='઀-૿'
# per-Doc fixes: (exact old, new, why)
FIX={'v129':[
  ('હૃદયને બાળનારી (કારણ કે પૂરી કોઈ કરે નહીં એટલે અજંપો થાય).','હૃદયને બાળનારી, કારણ કે પૂરી કોઈ કરે નહીં એટલે અજંપો થાય.','no brackets (aside spoken as is)'),
  ('વિભૂષિત થઈને (મૈત્રી એમનું આભૂષણ છે) બધાના સાથે','વિભૂષિત થઈને, મૈત્રી એમનું આભૂષણ છે, બધાના સાથે','no brackets (aside spoken as is)'),
  ('ચિંતન કરવું જોઈએ. (You must make an effort to think about it very seriously.) અકર્મમાં','ચિંતન કરવું જોઈએ. યુ મસ્ટ મેક એન એફર્ટ ટુ થિંક અબાઉટ ઇટ વેરી સિરિયસલી. અકર્મમાં','no brackets; his English sentence in Gujarati script (check by ear)'),
  ('સિંચન જેવું (પાઘડી બાંધી હતી ને આપણા ગજસુગોમાર).','સિંચન જેવું, પાઘડી બાંધી હતી ને આપણા ગજસુગોમાર.','no brackets (aside spoken as is)'),
  ('અંગારાઓ પર આળોટવું (એટલે આળોટવું) જેને','અંગારાઓ પર આળોટવું, એટલે આળોટવું, જેને','no brackets (aside spoken as is)'),
 ],'v130':[
  ('મેરુ પર્વતનું (કમળની પાંખડી કેટલી? મેરુ પર્વત કેવો?) એક ભ્રમરના','મેરુ પર્વતનું, કમળની પાંખડી કેટલી? મેરુ પર્વત કેવો? એક ભ્રમરના','no brackets (aside spoken as is)'),
  ('મુક્ત થઈ જાય (દોષ કયા છે? રાગ અને દ્વેષ, અને આ જે સંકલ્પ ઊભો થાય છે તે), એ દોષોથી','મુક્ત થઈ જાય, દોષ કયા છે? રાગ અને દ્વેષ, અને આ જે સંકલ્પ ઊભો થાય છે તે, એ દોષોથી','no brackets (aside spoken as is)'),
  ('ઇલેક્ટ્રોએન્સેફાલોગ્રાફ (EEG).','ઇલેક્ટ્રોએન્સેફાલોગ્રાફ, ઈઈજી.','no brackets; English letters in Gujarati script'),
 ],'vm1':[
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
 ],'v39':[
  ('કરદ્વય (એટલે બંને હાથની આંગળીઓથી) ષણ્મુખી મુદ્રા','કરદ્વય, એટલે બંને હાથની આંગળીઓથી, ષણ્મુખી મુદ્રા','no brackets (aside spoken as is)'),
  ('ષણ્મુખી મુદ્રા (આ મુદ્રાને સન્મુખી કહેવામાં આવે છે, પણ કુંભક કર્યા પછી આ કરવાનું છે) કરીને','ષણ્મુખી મુદ્રા, આ મુદ્રાને સન્મુખી કહેવામાં આવે છે, પણ કુંભક કર્યા પછી આ કરવાનું છે, કરીને','no brackets (aside spoken as is)'),
  ('શબ્દ અને કાળ (કારણ કે આ શબ્દ અહીંયાથી સાંભળો છો એટલે એ બંધ થઈ ગયો છે) કાળનું','શબ્દ અને કાળ, કારણ કે આ શબ્દ અહીંયાથી સાંભળો છો એટલે એ બંધ થઈ ગયો છે, કાળનું','no brackets (aside spoken as is)'),
  ('નવ ચક્ર (એટલે ષડ ચક્ર, તાળવું, આકાશ અને ભૂચક્ર), ષડ આધાર','નવ ચક્ર, એટલે ષડ ચક્ર, તાળવું, આકાશ અને ભૂચક્ર, ષડ આધાર','no brackets (aside spoken as is)'),
  ('ષડ આધાર (એટલે મૂલાધાર વગેરે ષડ આધાર), ત્રિલક્ષ','ષડ આધાર, એટલે મૂલાધાર વગેરે ષડ આધાર, ત્રિલક્ષ','no brackets (aside spoken as is)'),
  ('ત્રિલક્ષ (એટલે અંતર્લક્ષ, બહિર્લક્ષ અને મધ્ય લક્ષ), વ્યોમપંચક','ત્રિલક્ષ, એટલે અંતર્લક્ષ, બહિર્લક્ષ અને મધ્ય લક્ષ, વ્યોમપંચક','no brackets (aside spoken as is)'),
  ('વ્યોમપંચક (એટલે કે આકાશ, પરાકાશ, મહાકાશ, સૂર્યાકાશ અને પરમ આકાશ) ને સમ્યક','વ્યોમપંચક, એટલે કે આકાશ, પરાકાશ, મહાકાશ, સૂર્યાકાશ અને પરમ આકાશ, ને સમ્યક','no brackets (aside spoken as is)'),
  ('અહીં જ ઉભો છું','અહીં જ ઊભો છું','spelling: ઊભો'),
 ],'v382':[
  ('નિશ્વાસ (એટલે શ્વાસ અને પ્રશ્વાસ), ભય','નિશ્વાસ, એટલે શ્વાસ અને પ્રશ્વાસ, ભય','no brackets (aside spoken as is)'),
  ('અલ્પાહાર કરવો (આઠ કોળિયા), નિર્ભય','અલ્પાહાર કરવો, આઠ કોળિયા, નિર્ભય','no brackets (aside spoken as is; the book has no bracket here)'),
  ('જો અહીંયા આગાળે તમે તમારું\n\nધ્યાન કેન્દ્રિત','જો અહીંયા આગળે તમે તમારું ધ્યાન કેન્દ્રિત','paragraph joined: the sentence carries on; spelling આગળે'),
  ('અને નિંદ્રા પર','અને નિદ્રા પર','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('અને નિંદ્રા. એના','અને નિદ્રા. એના','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('આહાર, નિંદ્રા પર','આહાર, નિદ્રા પર','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('યોગ નિંદ્રામાં છે.','યોગ નિદ્રામાં છે.','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('અને નિંદ્રા, અજ્ઞાન','અને નિદ્રા, અજ્ઞાન','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('અજ્ઞાન નિંદ્રા, આ','અજ્ઞાન નિદ્રા, આ','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('તો નિંદ્રા આવે','તો નિદ્રા આવે','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('હવે નિંદ્રા પણ','હવે નિદ્રા પણ','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('રૂપી નિંદ્રા છે','રૂપી નિદ્રા છે','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('અજ્ઞાન નિંદ્રા જે','અજ્ઞાન નિદ્રા જે','spelling: નિદ્રા (Manav, 31 Oct)'),
  ('અજ્ઞાન નિંદ્રા અને','અજ્ઞાન નિદ્રા અને','spelling: નિદ્રા (Manav, 31 Oct)'),
 ],'v381':[
 ],'v13':[
  ('બ્રહ્મને જાણે છે. (વ્યોમ એટલે આકાશ).','બ્રહ્મને જાણે છે. વ્યોમ એટલે આકાશ.','no brackets (aside spoken as is)'),
 ],'v10':[
  ('અચિંત્ય (ચિંતા પણ ન કરાય, ચિંતન પણ ન કરી શકાય એવી રીતના) પરમાત્મા','અચિંત્ય, ચિંતા પણ ન કરાય, ચિંતન પણ ન કરી શકાય એવી રીતના, પરમાત્મા','no brackets (aside spoken as is)'),
  ('રૂપ, રસ.\n\nગંધહીન,','રૂપ, રસ, ગંધહીન,','paragraph joined: the list carries on'),
 ],'v9':[
  ('જ્યારે પરબ્રહ્મ...\n\nસાથે એકરૂપ','જ્યારે પરબ્રહ્મ સાથે એકરૂપ','paragraph joined: the sentence carries on'),
  ('અત્યારે તમને ક્યાંય\n\nપણ માયા','અત્યારે તમને ક્યાંય પણ માયા','paragraph joined: the sentence carries on'),
  ('એનું ખરેખર\n\nકોઈ મહત્વ','એનું ખરેખર કોઈ મહત્વ','paragraph joined: the sentence carries on'),
 ],'v6':[
  ('આજકાલ તો\n\nત્યાં જવાની','આજકાલ તો ત્યાં જવાની','paragraph joined: the sentence carries on'),
 ],'v3':[
  ('ધ્યાતા અને ધ્યાન (ધ્યાન કરનારો અને જે ઊભું થઈ રહ્યું છે) એ બેયને','ધ્યાતા અને ધ્યાન, ધ્યાન કરનારો અને જે ઊભું થઈ રહ્યું છે, એ બેયને','no brackets (aside spoken as is)'),
  ('આ સહિત છે અને\n\nઆ રહિત છે એમ','આ સહિત છે અને આ રહિત છે એમ','paragraph joined: the sentence carries on'),
 ],'v2':[
  ('એ પપૈયું આમ જોવે.','એ પપૈયું આમ જુએ.','જોવે written જુએ here (= sees; Manav 6 Nov: never જોવે)'),
  ('એના માટે એટલી...\n\nગ્રહણશીલતા એને','એના માટે એટલી ગ્રહણશીલતા એને','paragraph joined: the sentence carries on'),
  ('ના કરે છે કે હું...\n\nઆવો, નથી સમજાયું?','ના કરે છે કે હું આવો, નથી સમજાયું?','paragraph joined: the sentence carries on'),
 ]}
# 1. quotation marks (not listed: trivial)
q0=t.count('"')+t.count('“')+t.count('”')
t=re.sub(r'["“”]','',t)
t=re.sub(r"(?<![{0}])'|'(?![{0}])".format(G),'',t)   # 'પરમાત્મા હું જ છું' -> no quotes
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r' +\n','\n',t); t=re.sub(r'\n +','\n',t)
t=re.sub(r' ([,.?!:;])',r'\1',t)
spans=[]
for old,new,why in FIX.get(vm,[]):
    old2=re.sub(r'["“”]','',old)
    n=t.count(old2); assert n==1,(old2,n)
    i=t.find(old2); t=t[:i]+new+t[i+len(old2):]
    spans.append((i,len(new),old2,new,why))
# shift: later replacements may move earlier spans; recompute positions by search
T=t
# brackets printed in the book stay where he reads them (RULES 5): list them per video
KEEP={'v12':['ઉદર (પેટ)નો']}
_T=T
for k in KEEP.get(vm,[]): _T=_T.replace(k,'')
assert '(' not in _T and ')' not in _T and '"' not in _T, 'leftover brackets/quotes'
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
