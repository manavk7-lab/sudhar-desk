"""mkjs.py TEMPLATE.js NAME=value ... > out.js — fill a browser template's __NAME__ placeholders.
__URL__ and __CK__ are filled from $SD_WORK/gasurl.txt and $SD_WORK/capkey.txt unless given. Keep out.js out of the repo."""
import os,sys
W=os.environ.get('SD_WORK','.')
js=open(sys.argv[1],encoding='utf-8').read()
v={'URL':open(W+'/gasurl.txt').read().strip(),'CK':open(W+'/capkey.txt').read().strip()}
for a in sys.argv[2:]:
    k,_,x=a.partition('='); v[k]=x
for k,x in v.items(): js=js.replace('__'+k+'__',x)
left=[p for p in ('__KEY__','__START__','__END__','__DOC__','__OLD__','__NEW__') if p in js]
if left: sys.exit('unfilled: '+' '.join(left))
sys.stdout.write(js)
