"""showdec2.py VID — list judge decisions, flagging the kinds Manav has undone before (RULES.md 11)."""
import json,sys,re
V=sys.argv[1]; d=f'v{V}'
doc=open(f'{d}/doc.txt',encoding='utf-8').read()
K={k['id']:k for k in json.load(open(f'{d}/all_items.json',encoding='utf-8'))}
D=json.load(open(f'{d}/decisions.json',encoding='utf-8'))
FILL={'હા','સો','હેને','હને','હ','હેં','હેંને','હમ્મ','શું'}
risky=[];rest=[]
for j in D:
    c=K[j['id']]; old=c['old']; new=j.get('text') or ''
    before=doc[max(0,c['pos']-60):c['pos']].split()[-1:] ; after=doc[c['end']:c['end']+60].split()[:1]
    nb=[re.sub(r'[^\w઀-૿]','',w) for w in before+after]
    added=[w for w in re.sub(r'[^\w઀-૿ ]','',new).split() if w not in re.sub(r'[^\w઀-૿ ]','',old).split()]
    flag=''
    if not new.strip(): flag='DELETE'
    elif any(w in nb for w in added): flag='REPEAT?'
    elif any(w in FILL for w in added): flag='FILLER?'
    elif re.search(r'(^|\s)હ',old) and re.search(r'(^|\s)સ',new) and old.replace('હ','સ')==new: flag='SURTI?'
    elif any(w in new.split() for w in ['હતું','હતી','હતા','કહે','અને','રહે','કોઈ']) and not any(w in old.split() for w in ['હતું','હતી','હતા','કહે','અને','રહે','કોઈ']): flag='NORM?'
    elif re.search(r'[0-9]',old) and not re.search(r'[0-9]',new): flag='DIGIT?'
    ctx=(doc[max(0,c['pos']-45):c['pos']]+'⟪'+old+'→'+new+'⟫'+doc[c['end']:c['end']+35]).replace('\n',' ')
    line=f"{j['id']} {j['d']} {ctx} | S:{c['read'].get('S')} G:{c['read'].get('G')} | {j.get('why','')}"
    (risky if flag else rest).append((flag,line))
for f,l in risky: print('!!',f,l)
print('--- others:',len(rest))
if '--all' in sys.argv:
    for f,l in rest: print('  ',l)
