import os,sys,time
from google import genai
from google.genai import types
key=open(os.path.expanduser(sys.argv[1])).read().strip(); model=sys.argv[2]; audio=sys.argv[3]; out=sys.argv[4]
c=genai.Client(api_key=key)
f=c.files.upload(file=audio)
while f.state and f.state.name=='PROCESSING': time.sleep(3); f=c.files.get(name=f.name)
prompt=("આ ઓડિયો ગુજરાતી આધ્યાત્મિક પ્રવચન છે. બોલાયેલા દરેક શબ્દને ગુજરાતી લિપિમાં શબ્દશઃ (verbatim) લખો — "
 "કોઈ શબ્દ છોડશો નહીં, ઉમેરશો નહીં, સુધારશો નહીં કે સારાંશ આપશો નહીં. બોલનાર જેમ બોલે તેમ જ (બોલીના શબ્દો પણ) લખો. "
 "સંસ્કૃત શ્લોકો જેમ બોલાય તેમ ગુજરાતી લિપિમાં લખો. ફક્ત લખાણ આપો, ટાઈમસ્ટેમ્પ કે નોંધ નહીં.")
r=c.models.generate_content(model=model,contents=[f,prompt],config=types.GenerateContentConfig(temperature=0))
open(out,'w',encoding='utf-8').write(r.text or '')
print(model,'chars',len(r.text or ''),'usage',r.usage_metadata)
