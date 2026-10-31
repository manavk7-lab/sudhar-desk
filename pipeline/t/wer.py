import re,sys,difflib
TOK=re.compile(r'[઀-૿A-Za-z0-9‌‍]+')
FILL={'ઓમ','ૐ','હેને','હને','હેં','હેંને','હ','હાસ્ય','હમ્મ'}
def key(w):
    for a,b in [('‌',''),('‍',''),('ઁ',''),('ં',''),('઼',''),('્',''),('ી','િ'),('ૂ','ુ'),('ઈ','ઇ'),('ઊ','ઉ'),('ણ','ન'),('ળ','લ'),('શ','સ'),('ષ','સ')]: w=w.replace(a,b)
    return w
def wer(ref,hyp,loose=False):
    R=TOK.findall(ref); H=TOK.findall(hyp)
    if loose:
        R=[key(x) for x in R if x not in FILL]; H=[key(x) for x in H if x not in FILL]
        # join-insensitive: compare at character stream level too
    sm=difflib.SequenceMatcher(None,R,H,autojunk=False); e=0
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': e+=max(i2-i1,j2-j1)
    return e/len(R), len(R), len(H)
def cer(ref,hyp):
    r=''.join(key(x) for x in TOK.findall(ref) if x not in FILL); h=''.join(key(x) for x in TOK.findall(hyp) if x not in FILL)
    sm=difflib.SequenceMatcher(None,r,h,autojunk=False); e=0
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': e+=max(i2-i1,j2-j1)
    return e/len(r)
if __name__=='__main__':
    ref=open(sys.argv[1],encoding='utf-8-sig').read()
    for f in sys.argv[2:]:
        h=open(f,encoding='utf-8-sig').read()
        a=wer(ref,h); b=wer(ref,h,True)
        print(f'{f:40s} words wrong: exact {a[0]:.1%}  ignoring spelling {b[0]:.1%}  letters wrong {cer(ref,h):.1%}  (ref {a[1]} words, hyp {a[2]})')
