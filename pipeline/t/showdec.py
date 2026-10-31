import json,sys,re
V=sys.argv[1]; d=f'v{V}'
K={k['id']:k for k in json.load(open(f'{d}/all_items.json',encoding='utf-8'))}
D=json.load(open(f'{d}/decisions.json',encoding='utf-8'))
risky=[];rest=[]
for j in D:
    c=K[j['id']]; old=c['old']; new=j['text']
    flag=''
    if not new.strip(): flag='DELETE'
    elif re.search(r'(^|\s)હ',old) and re.search(r'(^|\s)સ',new) and old.replace('હ','સ')==new: flag='SURTI?'
    elif any(w in new.split() for w in ['હતું','હતી','હતા','કહે','અને','રહે']) and not any(w in old.split() for w in ['હતું','હતી','હતા','કહે','અને','રહે']): flag='NORM?'
    elif re.search(r'[0-9]',old) and not re.search(r'[0-9]',new): flag='DIGIT?'
    line=f"{j['id']} {j['d']} [{old}]→[{new}] S:{c['read'].get('S')} G:{c['read'].get('G')} | {j.get('why','')}"
    (risky if flag else rest).append((flag,line))
for f,l in risky: print('!!',f,l)
print('--- sample of others:')
for f,l in rest[:: max(1,len(rest)//25)]: print('  ',l)
