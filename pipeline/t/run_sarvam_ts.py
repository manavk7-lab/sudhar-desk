import os,sys,json,glob
from sarvamai import SarvamAI
key=open(os.path.expanduser(sys.argv[1])).read().strip(); audio=sys.argv[2]; out=sys.argv[3]
c=SarvamAI(api_subscription_key=key)
job=c.speech_to_text_job.create_job(model='saaras:v4',mode='transcribe',language_code='gu-IN',with_timestamps=True)
job.upload_files(file_paths=[audio]); job.start(); job.wait_until_complete()
d=out+'_dir'; os.makedirs(d,exist_ok=True); job.download_outputs(output_dir=d)
for p in glob.glob(d+'/*.json'):
    j=json.load(open(p,encoding='utf-8'))
    json.dump(j,open(out,'w',encoding='utf-8'),ensure_ascii=False)
    ts=j.get('timestamps') or {}
    print('keys',list(j.keys()),'ts keys',list(ts.keys()) if isinstance(ts,dict) else type(ts))
