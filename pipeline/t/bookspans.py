"""bookspans.py text.txt book_clean.txt out.json [min_score]
Which book sentences the speaker reads, and in which paragraph of text.txt. book_clean.txt = the typed pages
([G] lines = Gujarati translation, [S] = Sanskrit, === page headers). Output {paragraph index: [book sentences in
text order]}; used to show the proofreading agents the book's wording next to each paragraph (B: lines)."""
import sys, re, json
from rapidfuzz import fuzz
text = open(sys.argv[1], encoding='utf-8').read(); MIN = float(sys.argv[4]) if len(sys.argv) > 4 else 75
G = []
for l in open(sys.argv[2], encoding='utf-8'):
    l = l.strip()
    if l.startswith('[G]'): G.append(l[3:].strip())
gu = re.sub(r'\s+', ' ', ' '.join(G))
sents = [s.strip() for s in re.split(r'(?<=[.?!॥])\s+', gu) if len(re.findall(r'[઀-૿]+', s)) >= 5]
paras = text.split('\n\n'); starts = []; o = 0
for p in paras: starts.append(o); o += len(p) + 2
import bisect
res = {}; hit = 0
for s in sents:
    key = re.sub(r'॥[^॥]*॥', '', s).strip()
    if len(key) < 20: continue
    a = fuzz.partial_ratio_alignment(key, text, score_cutoff=MIN)
    if not a: continue
    hit += 1
    k = bisect.bisect_right(starts, a.dest_start) - 1
    res.setdefault(k, []).append((a.dest_start, s, round(a.score)))
out = {k: [s for _, s, _ in sorted(v)] for k, v in sorted(res.items())}
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('book sentences', len(sents), 'found', hit, 'in', len(out), 'paragraphs of', len(paras))
