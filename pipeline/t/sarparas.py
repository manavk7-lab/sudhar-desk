"""sarparas.py sarw.json out_doc.txt out.tsv VIDEOID [target_words]
Makes the starting transcript of a video that has no Doc: Sarvam's tokens (sarw.json from sarts.py), with a paragraph
break after a sentence end (. ? !) where the speaker pauses long, aiming at paragraphs of about target_words (90, like
the Docs). Never breaks inside a sentence. Also writes the word-time file for Sudhar Desk (sync/VIDEOID.tsv)."""
import sys, re, json, statistics
W = json.load(open(sys.argv[1], encoding='utf-8')); out, tsv, vid = sys.argv[2], sys.argv[3], sys.argv[4]
TARGET = int(sys.argv[5]) if len(sys.argv) > 5 else 90
PUN = re.compile(r'[\.,\?!;:।॥"\'“”‘’()\[\]…\-–—]+')
END = re.compile(r'[\.\?!]$')
n = len(W)
gap = [w[3] if len(w) > 3 else ((W[i + 1][0] - W[i][1]) if i + 1 < n else 99999) for i, w in enumerate(W)]
paras = []; cur = []; cnt = 0
for i, w in enumerate(W):
    s, e, t = w[0], w[1], w[2]
    cur.append(t); cnt += 1
    if i + 1 == n: break
    if not END.search(t): continue
    if re.match(r'(થી|માં|માંથી|નું|નો|ની|નાં)[\s,.?!]*$', W[i + 1][2]): continue   # Sarvam split a word here (stageA joins it)
    g = gap[i]
    # the longer the paragraph already is, the shorter the pause needed
    need = 4500 if cnt < TARGET * 0.4 else 2600 if cnt < TARGET * 0.8 else 1600 if cnt < TARGET * 1.3 else 900 if cnt < TARGET * 2 else 0
    if cnt >= 30 and g >= need:
        paras.append(' '.join(cur)); cur = []; cnt = 0
if cur: paras.append(' '.join(cur))
open(out, 'w', encoding='utf-8').write('\n\n'.join(paras) + '\n')
L = [len(p.split()) for p in paras]
print('paragraphs', len(paras), 'median words', statistics.median(L), 'max', max(L), 'min', min(L))
with open(tsv, 'w', encoding='utf-8') as f:
    f.write(f'# Sudhar Desk sync — Sarvam word times for {vid} (no YouTube captions for this video) (ms<TAB>word)\n')
    k = 0
    for w in W:
        s, t = w[0], w[2]
        w = PUN.sub('', t)
        if w: f.write(f'{s}\t{w}\n'); k += 1
print('tsv words', k)
