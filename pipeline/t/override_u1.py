"""override_u1.py — my own review of the judges' decisions for Upanishad 1 (RULES.md 1, 11), then re-apply.
Edits vu1/decisions.json in place and re-runs apply9 exactly as finalvid does."""
import json,subprocess,sys,re,hashlib
d='vu1'
D=json.load(open(f'{d}/decisions.json',encoding='utf-8'))
DROP={'c473':'self-correction repeat (he removes these)','c1144':'no engine heard હ'}
ASK={'c492':'S, G, Y heard અને but એ fits the sentence','c741':'ઓમ may be what he said (matras of Om)',
     'c750':'આગળે? no engine heard it','c769':'આગળે? no engine heard it','c772':'આગળે? no engine heard it',
     'c497':'both heard બૃહત્યા; બૃહદતા is the word'}
TEXT={'c259':('પડતી તી','engines write હતી for spoken તી'),'c1259':('શું છો? રુદ્ર. તમે રુદ્ર','both engines; question then answer')}
out=[];n=dict(drop=0,ask=0,text=0)
for j in D:
    i=j['id']
    if i in DROP: n['drop']+=1; continue
    if i in ASK: j['d']='ask'; j['why']=ASK[i]; n['ask']+=1
    if i in TEXT: j['text'],j['why']=TEXT[i]; n['text']+=1
    out.append(j)
json.dump(out,open(f'{d}/decisions.json','w',encoding='utf-8'),ensure_ascii=False)
print('overrides',n)
r=subprocess.run([sys.executable,'t/apply9.py',f'{d}/doc.txt',f'{d}/all_items.json',f'{d}/new.txt',f'{d}/rev_new.json',f'{d}/decisions.json'],capture_output=True,text=True)
print(r.stdout.strip(), r.stderr.strip()[-500:])
new=open(f'{d}/new.txt',encoding='utf-8').read(); old=open(f'{d}/doc.txt',encoding='utf-8').read()
R=json.load(open(f'{d}/rev_new.json',encoding='utf-8'))
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
print('newlines',old.count('\n'),new.count('\n'),'double spaces',new.count('  '),'items',len(R),'not unique',sum(1 for x in R if len(re.findall(flex(x['cur']),new))!=1))
