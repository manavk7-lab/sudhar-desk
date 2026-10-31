"""prepjudge.py items.json outprefix chunksize  -> outprefix_N.txt files for judges, and outprefix_kept.json"""
import sys,json,re
sys.path.insert(0,'t')
from fuse import key
NORM={'કે':'કહે','રે':'રહે','તું':'હતું','તી':'હતી','તા':'હતા','તો':'હતો','જાવ':'જાઓ','થાવ':'થાઓ','આવો':'આવો','ને':'અને','બી':'પણ','કોક':'કોઈ','કોકને':'કોઈને',
      'આઈને':'આવીને','આયા':'આવ્યા','આયો':'આવ્યો','આઈ':'આવી','આય':'આવે','ગ્યા':'ગયા','ગ્યો':'ગયો','ડાયા':'ડાહ્યા','હું':'હું'}
NORM={key(a):key(b) for a,b in NORM.items()}
def nw(w):
    w=key(w); w=NORM.get(w,w)
    if w.startswith('હ') and len(w)>2: w='સ'+w[1:]
    return w
def ns(s): return ' '.join(nw(x) for x in s.split())
def nospace(s): return ''.join(key(x) for x in s.split())
items=json.load(open(sys.argv[1],encoding='utf-8')); pre=sys.argv[2]; cs=int(sys.argv[3])
keep=[];skip={'space':0,'norm':0,'digit':0}
for it in items:
    trig=[n for n in it['by']]
    reads=[it['read'][n] for n in trig]
    if all(nospace(r)==nospace(it['old']) for r in reads): skip['space']+=1; continue
    if all(ns(r)==ns(it['old']) for r in reads): skip['norm']+=1; continue
    if re.search(r'[0-9૦-૯]',it['old']) and not any(re.search(r'[0-9૦-૯]',r) for r in reads): skip['digit']+=1; continue
    keep.append(it)
print(len(items),'->',len(keep),skip)
json.dump(keep,open(pre+'_kept.json','w',encoding='utf-8'),ensure_ascii=False)
def ts(t):
    if t is None: return ''
    s=t//1000; return f'[{s//3600}:{s%3600//60:02d}:{s%60:02d}] ' if s>=3600 else f'[{s//60}:{s%60:02d}] '
n=0
for k in range(0,len(keep),cs):
    n+=1
    with open(f'{pre}_{n}.txt','w',encoding='utf-8') as f:
        for it in keep[k:k+cs]:
            r=' || '.join(f'{e}: {v}' if v is not None else f"{e}: (no {dict(S='Sarvam',G='Gemini',Y='YouTube').get(e,e)} for this stretch)" for e,v in it['read'].items())
            f.write(f"{it['id']} {ts(it['t'])}{it['ctx']} || {r}\n")
print(n,'chunks')
