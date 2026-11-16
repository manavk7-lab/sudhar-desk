"""bookbrackets.py final.txt book_gu.txt rows_out.json — put the BOOK's brackets back where he reads them.
Manav (16 Nov, ઉપનિષદ - 34: "you used to forget ( ) while checking from books"; RULES.md since 1 Nov): book
"હંસ (ચેતન જીવ) હંમેશાં" → transcript "હંસ (ચેતન જીવ) હંમેશા", not "હંસ, ચેતન જીવ," or "હંસ ચેતન જીવ".
For every "(…)" in the book (up to 12 words inside) the same words are looked for in final.txt right after the
book's word before the bracket; where they stand there without brackets, a row puts "(" and ")" around them and drops
a comma that stood in the bracket's place. Writes wordfix rows [old, new, why, conf]."""
import re,sys,json
F,BK,OUT=sys.argv[1:4]
t=open(F,encoding='utf-8').read()
book=' '.join(open(b,encoding='utf-8').read() for b in BK.split(','))
book=re.sub(r'\s+',' ',book)
P=',.?!;:।॥–-'
def core(w): return w.strip(P+'‘’“”"\'')
TF=[(m.start(),m.end(),m.group()) for m in re.finditer(r'\S+',t)]
words=[core(w) for _,_,w in TF]
rows=[];used=set()
for m in re.finditer(r'(\S+)\s*\(([^()]{1,120})\)(\S*)\s*(\S*)',book):
    L=core(m.group(1)); inner=[core(w) for w in m.group(2).split() if core(w)]
    Rb=core(m.group(3) or m.group(4))
    if m.group(1)[-1:] in '.?!।॥' or len(L)<2 or not Rb: continue
    if not L or not inner or len(inner)>12: continue
    k=len(inner)
    STOP={'કે','આ','એ','તે','જે','જ','પણ','પરંતુ','અને','તથા','એવો','એવી','એવું','હું','છે','આ રીતે','અર્થાત્','એટલે','કેમકે','તો'}
    if ' '.join(inner) in STOP or sum(len(w) for w in inner)<4: continue
    for i in range(1,len(TF)-k+1):
        if words[i:i+k]!=inner: continue
        lw=words[i-1]
        if not (lw==L or (len(lw)>=4 and len(L)>=4 and lw[:4]==L[:4])): continue
        if TF[i-1][2][-1:] in '.?!।' or TF[i+k-1][2][-1:] in '.?!।': continue
        rw=words[i+k] if i+k<len(words) else ''
        if not (rw==Rb or (len(rw)>=3 and len(Rb)>=3 and rw[:3]==Rb[:3]) or (m.group(3) and rw.startswith(m.group(3)[:2]))): continue
        if '(' in TF[i][2] or ')' in TF[i+k-1][2] or i in used: continue
        a,b=TF[i-1][0],TF[i+k-1][1]
        old=t[a:b]
        nxt_end=TF[i+k][1] if i+k<len(TF) else b
        # include the next word for context; uniqueness
        old=t[a:nxt_end]
        prev=TF[i-1][2].rstrip(',')
        inner_txt=t[TF[i][0]:TF[i+k-1][1]]
        last=inner_txt.rstrip(','); trail=inner_txt[len(last):]
        after=t[TF[i+k-1][1]:nxt_end]
        new=prev+' ('+last+')'+after
        if t.count(old)!=1 or old==new: continue
        used.add(i)
        rows.append([old,new,'book bracket as printed: '+m.group(0)[:80],'sure'])
json.dump(rows,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('rows',len(rows))
for r in rows[:8]: print('  ',repr(r[0][:70]),'->',repr(r[1][:70]))
