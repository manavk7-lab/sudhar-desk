"""mkchecks.py final.txt asks.json out_items.json [tsv]
Turns the proofreading agents' "ask" answers into ✎ check items on the FINAL text: the Doc keeps Sarvam's words
(cur = the text as it is now) and the agent's guess is the switch-to text (alt), conf unsure. An ask whose words were
changed later (book, mantra, punctuation) is matched ignoring punctuation; if it still cannot be found once, it is
reported and dropped."""
import sys, re, json, hashlib, subprocess, os
T = open(sys.argv[1], encoding='utf-8').read(); A = json.load(open(sys.argv[2], encoding='utf-8')); out = sys.argv[3]
tsv = sys.argv[4] if len(sys.argv) > 4 else None
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def loose(s): return r'[\s,.?!;:]+'.join(re.escape(re.sub(r'[,.?!;:]', '', x)) for x in s.split() if re.sub(r'[,.?!;:]', '', x))
def hid(*x): return hashlib.md5('|'.join(x).encode()).hexdigest()[:8]
items = []; miss = []
for a in A:
    old, new = a['old'], a['new']
    ms = [m.span(1) for m in re.finditer('(?=(' + flex(old) + '))', T)]
    if len(ms) != 1:
        ms = [m.span(1) for m in re.finditer('(?=(' + loose(old) + '))', T)]
        if len(ms) == 1:
            # keep the text's own punctuation in cur; put the guess words in place of the old words in alt
            s, e = ms[0]; cur = T[s:e]
            ow = [w for w in old.split()]; nw = new.split()
            alt = new if len(ow) != len(cur.split()) else new
        else:
            miss.append((old, len(ms))); continue
    else:
        s, e = ms[0]; cur = T[s:e]; alt = new
    if any(not (e <= x or y <= s) for x, y, _ in [(i['_s'], i['_e'], 0) for i in items]): miss.append((old, 'overlap')); continue
    items.append({'id': hid(cur, alt), 'cur': cur, 'alt': alt, 'kind': 'check', 'conf': 'unsure',
                  'why': (a.get('why') or 'listen') + ' (Claude\'s guess; the Doc keeps what Sarvam heard)', 'heard': '', 't': None,
                  '_s': s, '_e': e})
for i in items: i.pop('_s'); i.pop('_e')
json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('check items', len(items), 'not found', len(miss))
for m in miss: print('  MISS', m)
