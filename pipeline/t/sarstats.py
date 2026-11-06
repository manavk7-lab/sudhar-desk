# sarstats.py OUT.json SAR1:REF1[:W] SAR2:REF2[:W] ...
# Aligns a Sarvam transcript with a finished/corrected text of the same video, word by word, and counts for every
# Sarvam word (and short phrase) what the reference has instead. W = weight (e.g. 2 for a text Manav finished himself).
# Output: {"subs": {sar_form: {ref_form: weighted count}}, "keep": {sar_form: weighted count}, "videos": {...}}
# Used to find systematic Sarvam habits worth correcting in a video that has only Sarvam (no Doc, no captions).
import sys, re, json, difflib, collections
PUN = re.compile(r'[\.,\?!;:।॥"\'“”‘’()\[\]…\-–—]+')
def toks(t):
    return [w for w in (PUN.sub(' ', x) for x in t.split()) for w in w.split() if w]
out = sys.argv[1]
subs = collections.defaultdict(collections.Counter); keep = collections.Counter(); vids = {}
for spec in sys.argv[2:]:
    parts = spec.split(':'); sar, ref = parts[0], parts[1]; W = float(parts[2]) if len(parts) > 2 else 1.0
    a = toks(open(sar, encoding='utf-8').read()); b = toks(open(ref, encoding='utf-8').read())
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    nsub = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for w in a[i1:i2]: keep[w] += W
            # also count 2-word phrases kept (so phrase subs get a precision)
            for k in range(i1, i2 - 1): keep[a[k] + ' ' + a[k + 1]] += W
            continue
        A = ' '.join(a[i1:i2]); B = ' '.join(b[j1:j2])
        if op == 'replace' and (i2 - i1) == (j2 - j1) and (i2 - i1) <= 3:
            for x, y in zip(a[i1:i2], b[j1:j2]): subs[x][y] += W; nsub += 1
        elif (i2 - i1) <= 3 and (j2 - j1) <= 3:
            # insertion/deletion/uneven replace: record with one word of left context so it can be applied safely
            L = a[i1 - 1] if i1 > 0 else '^'
            subs[(L + ' ' + A).strip()][(L + ' ' + B).strip() if L != '^' else B] += W; nsub += 1
    vids[spec] = {'sar_words': len(a), 'ref_words': len(b), 'ratio': round(sm.ratio(), 4), 'subs': nsub}
    print(spec, vids[spec], flush=True)
json.dump({'subs': {k: dict(v) for k, v in subs.items()}, 'keep': dict(keep), 'videos': vids},
          open(out, 'w', encoding='utf-8'), ensure_ascii=False)
