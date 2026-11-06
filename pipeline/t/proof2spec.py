"""proof2spec.py text.txt paras.json out_spec.json out_ask.json pr_1_out.json [pr_2_out.json ...]
Turns the proofreading agents' answers (PROOF1.md format: {p, cur, alt, d, why}) into manualgen 'once' rows on the
CURRENT text: the agent's cur is found inside its paragraph and widened word by word until it occurs once in the whole
text. fix -> conf sure, maybe -> conf likely. ask entries go to out_ask.json (made into check items at the very end).
paras.json = {"p0001": paragraph index (0-based) in text.txt, ...} as written by mkproof.py."""
import sys, re, json
text = open(sys.argv[1], encoding='utf-8').read(); P = json.load(open(sys.argv[2], encoding='utf-8'))
spec_out, ask_out = sys.argv[3], sys.argv[4]
paras = text.split('\n\n'); starts = []; o = 0
for p in paras: starts.append(o); o += len(p) + 2
def flex(s): return r'\s+'.join(re.escape(x) for x in s.split())
def count(s): return len(re.findall('(?=' + flex(s) + ')', text))
rows = []; asks = []; bad = []; seen = []
import os
OV = json.load(open(os.path.join(os.path.dirname(sys.argv[2]), 'proof_override.json'), encoding='utf-8')) if os.path.exists(os.path.join(os.path.dirname(sys.argv[2]), 'proof_override.json')) else {'drop': [], 'd': {}}
DROP = {(a, b) for a, b, *_ in OV.get('drop', [])}; DCH = OV.get('d', {}); ALT = OV.get('alt', {})   # d: {"pid|cur": "ask"|"maybe"|"fix"}
dropped = 0
for f in sys.argv[5:]:
    for d in json.load(open(f, encoding='utf-8')):
        pid = d.get('p'); cur = (d.get('cur') or '').strip(); alt = (d.get('alt') or '').strip()
        if pid not in P or not cur or d.get('d') not in ('fix', 'maybe', 'ask'): bad.append((f, pid, cur, 'bad entry')); continue
        if cur == alt: bad.append((f, pid, cur, 'no change')); continue
        if (pid, cur) in DROP: dropped += 1; continue
        if pid + '|' + cur in DCH: d = dict(d); d['d'] = DCH[pid + '|' + cur]
        if pid + '|' + cur in ALT: alt = ALT[pid + '|' + cur]
        k = P[pid]; para = paras[k]

        ms = [m.span(1) for m in re.finditer('(?=(' + flex(cur) + '))', para)]
        if len(ms) != 1: bad.append((f, pid, cur, f'{len(ms)} times in its paragraph')); continue
        a, b = ms[0]; A, Bb = starts[k] + a, starts[k] + b
        # widen until unique in the whole text (stay inside the paragraph)
        lo, hi = starts[k], starts[k] + len(para); pre = ''; post = ''
        a0, b0 = A, Bb
        def ok(A, Bb, pre, post):   # the old text must occur once now, and the new text once after the change
            if count(text[A:Bb]) != 1: return False
            t2 = text[:A] + pre + alt + post + text[Bb:]
            return len(re.findall('(?=' + flex(pre + alt + post) + ')', t2)) == 1
        while not ok(A, Bb, pre, post):
            na = text.rfind(' ', lo, A - 1); nb = text.find(' ', Bb + 1, hi)
            if na < 0 and nb < 0: break
            if na >= 0: pre = text[na + 1:A] + pre; A = na + 1
            if nb >= 0: post = post + text[Bb:nb]; Bb = nb
        if not ok(A, Bb, pre, post): bad.append((f, pid, cur, 'not unique')); continue
        if any(not (Bb <= x or y <= A) for x, y in seen): bad.append((f, pid, cur, 'overlaps another entry')); continue
        seen.append((A, Bb))
        old = text[A:Bb]; new = pre + alt + post
        assert old == pre + text[a0:b0] + post, (old, pre, post)
        if d['d'] == 'ask':
            asks.append({'old': old, 'new': new, 'why': d.get('why', ''), 'p': pid})
        else:
            rows.append([old, new, d.get('why', ''), 'sure' if d['d'] == 'fix' else 'likely', 'once', A])
rows.sort(key=lambda r: r[5])
json.dump([r[:5] for r in rows], open(spec_out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(asks, open(ask_out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
import collections
print('dropped by review', dropped, 'rows', len(rows), collections.Counter(r[3] for r in rows), 'asks', len(asks), 'bad', len(bad))
for x in bad: print('  BAD', x)
