"""mkproof.py text.txt doc_orig.txt sarw.json OUTPREFIX N [book.json]
Splits the current text into N files OUTPREFIX_1.txt … for the proofreading agents (PROOF1.md): one line per paragraph,
'p0001 [mm:ss] text'. The time comes from doc_orig.txt (Sarvam's tokens, same paragraphs) and sarw.json.
With book.json (bookspans.py) every paragraph is followed by '  B: …' lines: the book sentences he reads in it.
Also writes OUTPREFIX_paras.json {pid: paragraph index}."""
import sys, json
text, orig, W, pre, N = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
BK = {int(k): v for k, v in json.load(open(sys.argv[6], encoding='utf-8')).items()} if len(sys.argv) > 6 else {}
P = open(text, encoding='utf-8').read().split('\n\n'); Po = open(orig, encoding='utf-8').read().split('\n\n')
W = json.load(open(W, encoding='utf-8'))
assert len(P) == len(Po), (len(P), len(Po))
times = []; k = 0
for p in Po:
    times.append(W[min(k, len(W) - 1)][0]); k += len(p.split())
def mmss(ms): s = ms // 1000; return f'{s//3600}:{s%3600//60:02d}:{s%60:02d}' if s >= 3600 else f'{s//60:02d}:{s%60:02d}'
words = [len(p.split()) for p in P]; tot = sum(words); per = tot / N
groups = [[] for _ in range(N)]; acc = 0
for i, p in enumerate(P):
    g = min(N - 1, int(acc / per)); groups[g].append(i); acc += words[i]
ids = {}
for g, idx in enumerate(groups, 1):
    with open(f'{pre}_{g}.txt', 'w', encoding='utf-8') as f:
        for i in idx:
            pid = f'p{i+1:04d}'; ids[pid] = i
            f.write(f'{pid} [{mmss(times[i])}] {P[i].strip()}\n')
            for b in BK.get(i, []): f.write(f'  B: {b}\n')
    print(f'{pre}_{g}.txt', len(idx), 'paragraphs', sum(words[i] for i in idx), 'words')
json.dump(ids, open(f'{pre}_paras.json', 'w'), indent=0)
