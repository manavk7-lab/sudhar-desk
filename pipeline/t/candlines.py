import json,sys
C=json.load(open(sys.argv[1],encoding='utf-8')); out=sys.argv[2]
def ts(t):
    if t is None: return ''
    s=t//1000; return f'[{s//3600}:{s%3600//60:02d}:{s%60:02d}] ' if s>=3600 else f'[{s//60}:{s%60:02d}] '
with open(out,'w',encoding='utf-8') as f:
    for c in C:
        r=' || '.join(f'{e}: {v}' if v is not None else f'{e}: (n/a)' for e,v in c['read'].items() if e in ('S','G'))
        f.write(f"{c['id']} {c['kind']} {ts(c['t'])}{c['ctx']} || {r}\n")
print(len(C),'lines ->',out)
