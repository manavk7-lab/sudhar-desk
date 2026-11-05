"""agaledraft.py doc.txt out.json — draft આગળે items (place sense after અહીંયા/અહીં/ત્યાં/જ્યાં/ક્યાં), conf likely.
Skips motion (આવી/પહોંચ/વધ/જા/ગયા/ચાલ/ખેંચા…) and spots that already say આગળે. Review the list by eye."""
import re,sys,json
t=open(sys.argv[1]).read()
MOTION=re.compile(r'^(આવ|પહોં|પહોચ|વધ|જા|જઈ|ગય|ચાલ|ખેંચ|ખસ|દોડ|નીકળ|પસાર|લઈ|લા|મોકલ)')
out=[];skip=[]
for m in re.finditer(r'(અહીંયા|અહીં|અહિયાં|ત્યાં|જ્યાં|ક્યાં)\s+આગળ(?![ે઀-૿])',t):
    s,e=m.span()
    nxt=re.match(r'\s*([઀-૿]+)',t[e:]); nw=nxt.group(1) if nxt else ''
    a0=t.rfind(' ',0,max(0,s-1)); a0=0 if a0<0 else a0+1
    a1m=re.match(r'\s*\S+',t[e:]); a1=e+(a1m.end() if a1m else 0)
    alt=t[a0:a1]
    if MOTION.match(nw): skip.append(alt); continue
    if t.count(alt)!=1:
        a0b=t.rfind(' ',0,max(0,a0-1)); a0=0 if a0b<0 else a0b+1; alt=t[a0:a1]
    if t.count(alt)!=1: skip.append('NOTUNIQUE '+alt); continue
    cur=alt.replace(m.group(), m.group()+'ે',1)
    out.append({'alt':alt,'cur':cur,'why':'આગળે as the speaker usually says it after અહીંયા/ત્યાં (Manav, 29–30 Oct)','conf':'likely'})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(out),'items'); [print('  ',x['alt'],'→',x['cur']) for x in out]
print('skipped:'); [print('  ',x) for x in skip]
