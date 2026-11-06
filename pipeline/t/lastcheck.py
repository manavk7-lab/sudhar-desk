"""lastcheck.py final.txt items.json — PROCESS C9.5 last checks before posting: quotes/brackets, paragraph ends,
mantra layout (single line breaks), double spaces, and that every ✎ item's cur occurs exactly once."""
import json,re,sys,hashlib
t=open(sys.argv[1],encoding='utf-8').read(); P=json.load(open(sys.argv[2],encoding='utf-8')) if len(sys.argv)>2 else []
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
bad=0
for ch in '"“”‘’()[]{}':
    n=t.count(ch)
    if n: bad+=1; print('CHAR',repr(ch),n, [t[max(0,m.start()-30):m.start()+30] for m in re.finditer(re.escape(ch),t)][:3])
if '  ' in t: bad+=1; print('double spaces',t.count('  '))
# words Manav always corrects (RULES 1): never post them
FORBIDDEN={'જોવે':'write જોઈએ (or જુએ = sees) — Manav 6 Nov'}
for w,why in FORBIDDEN.items():
    ms=[m for m in re.finditer(r'(?<![\u0A80-\u0AFF])'+w+r'(?![\u0A80-\u0AFF])',t)]
    if ms: bad+=1; print('FORBIDDEN',w,len(ms),why,[t[max(0,m.start()-30):m.start()+20] for m in ms][:5])
lines=t.split('\n')
for i,l in enumerate(lines):
    s=l.strip()
    if not s: continue
    nxt=next((x.strip() for x in lines[i+1:] if x.strip()),'')
    ends=s[-1] in '.?!।॥:'
    if not ends and not s.endswith('જય સચ્ચિદાનંદ') and not nxt.startswith('ૐ'):
        bad+=1; print('NO STOP at paragraph end:',repr(s[-60:]))
for m in re.finditer(r'[।॥] *\n\n',t):
    ctx=t[m.end():m.end()+40]
    print('note: empty line after a mantra line ->',repr(t[m.start()-20:m.end()+20]))
for m in re.finditer(r'\n\n *ૐ',t): print('note: empty line before ૐ ->',repr(t[m.start()-30:m.end()+10]))
lost=[it['cur'][:60] for it in P if it.get('cur','').strip() and len(re.findall('(?='+flex(it['cur'])+')',t))!=1]
if lost: bad+=1; print('ITEMS not found once:',len(lost),lost[:10])
print('paragraphs',sum(1 for l in lines if l.strip()),'items',len(P),'problems',bad,'sha',hashlib.sha256(t.encode()).hexdigest()[:16])
