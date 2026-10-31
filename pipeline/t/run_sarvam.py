import os,sys,json,glob
from sarvamai import SarvamAI
key=open(os.path.expanduser(sys.argv[1])).read().strip(); model=sys.argv[2]; audio=sys.argv[3]; out=sys.argv[4]
c=SarvamAI(api_subscription_key=key)
kw=dict(model=model,language_code='gu-IN')
if model.startswith('saaras'): kw['mode']='transcribe'
job=c.speech_to_text_job.create_job(**kw)
job.upload_files(file_paths=[audio]); job.start(); job.wait_until_complete()
d=out+'_dir'; os.makedirs(d,exist_ok=True); job.download_outputs(output_dir=d)
txt=''
for p in glob.glob(d+'/*.json'):
    j=json.load(open(p,encoding='utf-8')); txt+=j.get('transcript','')
open(out,'w',encoding='utf-8').write(txt); print(model,'chars',len(txt))
