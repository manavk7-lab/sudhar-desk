import os
import sys
S=os.environ.get('SD_WORK','.')+''
key,start,end=sys.argv[1],sys.argv[2],sys.argv[3]
js=open(S+'/t/recorder2.js').read()
U=open(S+'/gasurl.txt').read().strip(); CK=open(os.environ.get('SD_WORK','.')+'/capkey.txt').read().strip()
print(js.replace('__KEY__',key).replace('__START__',start).replace('__END__',end).replace('__URL__',U).replace('__CK__',CK))
