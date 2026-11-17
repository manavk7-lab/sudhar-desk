"""addrp.py VM YT — add the punctuation items (VM/rev_punct.json) to VM/items_all_final.json with ids and video times."""
import json,sys,os,hashlib,subprocess
V,YT=sys.argv[1:3]; R=os.environ.get('SD_REPO','/home/claude/sudhar-desk')
rp=json.load(open(f'{V}/rev_punct.json',encoding='utf-8'))
out=[]
for x in rp:
    out.append({'id':hashlib.md5((x['alt']+'|'+x['cur']).encode()).hexdigest()[:8],'cur':x['cur'],'alt':x['alt'],'kind':'applied',
                'conf':x.get('conf','likely'),'why':x.get('why','punctuation by pause and meaning')})
json.dump(out,open(f'{V}/rp_tmp.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
subprocess.run(['python3',os.path.join(os.path.dirname(os.path.abspath(__file__)),'addtimes.py'),f'{V}/final.txt',f'{R}/sync/{YT}.tsv',f'{V}/rp_tmp.json'])
it=json.load(open(f'{V}/items_all_final.json',encoding='utf-8'))
ids={x['id'] for x in it}
add=[x for x in json.load(open(f'{V}/rp_tmp.json',encoding='utf-8')) if x['id'] not in ids]
json.dump(it+add,open(f'{V}/items_all_final.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('added',len(add),'items now',len(it)+len(add))
