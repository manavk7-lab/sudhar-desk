"""ocrbook.py model out_dir page.png ... — OCR scanned book pages (Gujarati commentary + Devanagari Sanskrit) with Gemini."""
import sys,os,concurrent.futures as cf
from google import genai
from google.genai import types
S=os.path.dirname(os.path.abspath(__file__))+'/..'
c=genai.Client(api_key=open(S+'/gemini.key').read().strip())
model=sys.argv[1]; out=sys.argv[2]; pages=sys.argv[3:]
P=("This is one scanned page of a Gujarati book of Upanishads (Brahma Vidya Khand). Transcribe ALL printed text exactly, top to bottom, "
   "including the running header line and page number. Sanskrit mantras are printed in Devanagari: keep them in Devanagari exactly as printed "
   "(every matra, halant, anusvara, visarga, avagraha, danda । and ॥ and the verse numbers). Gujarati explanation stays in Gujarati script exactly as printed. "
   "Keep each printed line of a mantra on its own line; separate blocks/paragraphs with a blank line. Ignore handwritten pen marks, ticks and underlines. "
   "Do not translate, correct, normalise or add anything. Output only the transcription.")
def one(p):
    o=os.path.join(out,os.path.basename(p).rsplit('.',1)[0]+'.txt')
    if os.path.exists(o) and os.path.getsize(o)>200: return p,'skip'
    data=open(p,'rb').read()
    for a in range(3):
        try:
            r=c.models.generate_content(model=model,contents=[types.Part.from_bytes(data=data,mime_type='image/png'),P],config=types.GenerateContentConfig(temperature=0))
            t=r.text or ''
            if len(t)>200: open(o,'w',encoding='utf-8').write(t); return p,len(t)
        except Exception as e: err=str(e)[:200]
    return p,'FAILED'
with cf.ThreadPoolExecutor(5) as ex:
    for p,r in ex.map(one,pages): print(os.path.basename(p),r,flush=True)
