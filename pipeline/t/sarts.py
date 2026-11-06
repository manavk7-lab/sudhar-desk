"""sarts.py AUDIODIR OUTDIR KEY:START[,KEY:START...]
For a video with no YouTube captions: Sarvam was run with timestamps (SARTS=1), which come per chunk (~10-20 s, a
sentence or two). Inside each chunk the words are placed on the SPEECH of the piece's audio: the silences in the chunk
(from the audio envelope, like pauses.py) are given to word boundaries in order (a DP that prefers boundaries after
. ? ! and ,), and the speech between two silences is shared by its words by length. Writes, in video time,
  OUTDIR/sarw.json   [[start_ms, end_ms, token, pause_after_ms], ...]  (the transcript's own tokens, overlaps merged)
  OUTDIR/sar.txt     the tokens joined by spaces (one line)
  OUTDIR/seams.txt   the words around each cut between two recordings (check these by eye)
Each recording KEY started at video second START (recorder3 R.t0; R.map showed recording time = video time - START).
Pieces KEY_pNN were cut from the recording at KEY_cuts.json 'cuts' (seconds of the recording)."""
import sys, os, re, json, glob, difflib, wave
import numpy as np
A, O = sys.argv[1], sys.argv[2]
KS = [(k.split(':')[0], float(k.split(':')[1])) for k in sys.argv[3].split(',')]
PUN = re.compile(r'[\.,\?!;:।॥"\'“”‘’()\[\]…\-–—]+')
def norm(w): return PUN.sub('', w)
HOP = 0.01; MINSIL = 0.18

def silences(path):
    with wave.open(path) as f:
        sr = f.getframerate(); x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32)
    win = int(0.03 * sr); hop = int(HOP * sr); m = (len(x) - win) // hop
    if m <= 0: return []
    idx = np.arange(win)[None, :] + hop * np.arange(m)[:, None]
    db = 20 * np.log10(np.sqrt((x[idx] ** 2).mean(1) + 1e-6) + 1e-6)
    floor = np.percentile(db, 10); sp_l = np.percentile(db, 80); thr = floor + 0.35 * (sp_l - floor)
    sp = db > thr; runs = []; i = 0; n = len(sp)
    while i < n:
        if not sp[i]:
            j = i
            while j < n and not sp[j]: j += 1
            if (j - i) * HOP >= 0.12: runs.append((i * HOP, j * HOP))
            i = j
        else: i += 1
    return runs

def bonus(tok):
    if re.search(r'[\.\?!]$', tok): return 0.10
    if re.search(r'[,;:]$', tok): return 0.05
    return 0.0

def place_chunk(toks, S, E, sil):
    """toks: list of str; returns list of (start, end, pause_after) in piece seconds; pause_after of the last token
    is filled by the caller (chunk boundary)."""
    n = len(toks)
    if n == 0: return []
    # leading / trailing silence of the chunk
    s0, e0 = S, E
    for a, b in sil:
        if a <= S + 0.3 and b > S: s0 = max(s0, b)
        if b >= E - 0.3 and a < E: e0 = min(e0, a)
    if e0 - s0 < 0.2: s0, e0 = S, E
    inner = [(max(a, s0), min(b, e0)) for a, b in sil if a > s0 and b < e0 and (b - a) >= MINSIL]
    w = np.array([max(1, len(norm(t))) for t in toks], float); W = w.sum()
    F = np.cumsum(w)[:-1] / W                       # fraction at boundary k (after token k), k = 0..n-2
    B = np.array([bonus(t) for t in toks[:-1]])
    # speech-time fraction of each inner silence
    P = (e0 - s0) - sum(b - a for a, b in inner)
    G = []; acc = 0.0; last = s0
    for a, b in inner:
        acc += a - last; G.append(acc / max(P, 1e-3)); last = b
    m = len(inner); nb = n - 1
    assign = []
    if m and nb:
        strict = m <= nb
        INF = 1e9
        # dp[j][k] = best cost with silence j at boundary k
        dp = np.full((m, nb), INF); bk = np.zeros((m, nb), int)
        for k in range(nb): dp[0][k] = abs(F[k] - G[0]) - B[k] * (inner[0][1] - inner[0][0] >= 0.3)
        for j in range(1, m):
            best = INF; arg = -1
            for k in range(nb):
                # best previous boundary < k (strict) or <= k
                kk = k - 1 if strict else k
                if kk >= 0 and dp[j - 1][kk] < best: best = dp[j - 1][kk]; arg = kk
                if best < INF:
                    dp[j][k] = best + abs(F[k] - G[j]) - B[k] * (inner[j][1] - inner[j][0] >= 0.3); bk[j][k] = arg
        k = int(np.argmin(dp[m - 1])); assign = [0] * m; assign[m - 1] = k
        for j in range(m - 1, 0, -1): k = bk[j][k]; assign[j - 1] = k
    # build runs of tokens between assigned boundaries
    pause = [0.0] * n; cuts = []                       # (boundary k, silence a, b)
    for j, k in enumerate(assign):
        if cuts and cuts[-1][0] == k: cuts[-1] = (k, cuts[-1][1], inner[j][1])   # two silences on one boundary: merge
        else: cuts.append((k, inner[j][0], inner[j][1]))
    out = [None] * n; t0 = s0; first = 0
    for k, a, b in cuts + [(n - 1, e0, e0)]:
        idx = list(range(first, k + 1)); ws = w[idx]; tot = ws.sum(); c = 0.0
        for i, wi in zip(idx, ws):
            st = t0 + (a - t0) * c / tot; c += wi; en = t0 + (a - t0) * c / tot; out[i] = [st, en]
        if k < n - 1: pause[k] = b - a
        t0 = b; first = k + 1
    return [(s, e, p) for (s, e), p in zip(out, pause)]

def piece_tokens(js, wavpath):
    tr = js.get('transcript') or ''
    ts = js.get('timestamps') or {}
    Wc = ts.get('words') or []; St = ts.get('start_time_seconds') or []; Et = ts.get('end_time_seconds') or []
    sil = silences(wavpath)
    chunks = [(c.split(), s, e) for c, s, e in zip(Wc, St, Et) if c.split()]
    placed = []                                       # (tok, s, e, pause)
    for ci, (toks, s, e) in enumerate(chunks):
        P = place_chunk(toks, s, e, sil)
        for t, (a, b, p) in zip(toks, P): placed.append([t, a, b, p])
        if placed:   # pause after the chunk's last token = silence around the chunk boundary
            bt = e; best = 0.0
            for a, b in sil:
                if a - 0.3 <= bt <= b + 0.3: best = max(best, b - a)
            placed[-1][3] = best
    # the transcript's tokens should be the chunks' tokens; align in case they differ
    toks = tr.split(); a = [norm(t) for t in toks]; b = [norm(x[0]) for x in placed]
    if a == b: return [(t, x[1], x[2], x[3]) for t, x in zip(toks, placed)]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False); out = [None] * len(toks)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal' or (op == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): out[i1 + k] = tuple(placed[j1 + k][1:])
        elif op == 'replace':
            s0, e0 = placed[j1][1], placed[j2 - 1][2]; nn = i2 - i1
            for k in range(nn): out[i1 + k] = (s0 + (e0 - s0) * k / nn, s0 + (e0 - s0) * (k + 1) / nn, 0.0)
    for i in range(len(out)):
        if out[i] is None:
            prev = next((out[j][1] for j in range(i - 1, -1, -1) if out[j]), 0.0)
            nxt = next((out[j][0] for j in range(i + 1, len(out)) if out[j]), prev)
            out[i] = (prev, max(prev, nxt), 0.0)
    print('  transcript and chunks differ; aligned', sum(1 for o in sm.get_opcodes() if o[0] != 'equal'), 'spots')
    return [(t,) + o for t, o in zip(toks, out)]

recs = []
for k, start in KS:
    cuts = json.load(open(f'{A}/{k}_cuts.json'))['cuts']
    pcs = sorted(glob.glob(f'{A}/{k}_p[0-9][0-9].wav'))
    R = []
    for i, p in enumerate(pcs):
        js_files = sorted(glob.glob(p[:-4] + '.sar.txt_dir/*.json'))
        if not js_files: print('NO JSON for', p); continue
        js = json.load(open(js_files[0], encoding='utf-8'))
        if not js.get('timestamps'): print('no timestamps in', js_files[0])
        off = start + cuts[i]
        for t, s, e, pz in piece_tokens(js, p):
            R.append([round((off + s) * 1000), round((off + e) * 1000), t, round(pz * 1000)])
        if R: R[-1][3] = 1000   # end of a piece: it was cut at a silence
    recs.append((k, start, R))
    print(k, 'tokens', len(R), 'first', R[0][:3] if R else None, 'last', R[-1][:3] if R else None)

allw = recs[0][2]; seams = []
for (k1, s1, R1), (k2, s2, R2) in zip(recs, recs[1:]):
    if not R1 or not R2: continue
    end1 = R1[-1][1]
    lo, hi = s2 * 1000 + 2500, end1 - 2500
    best = None
    for i, a in enumerate(allw[:-1]):
        if lo <= a[1] <= hi and (best is None or a[3] > best[0]): best = (a[3], a[1] + a[3] / 2)
    T = best[1] if best else (s2 * 1000 + end1) / 2
    left = [w for w in allw if w[0] < T]; right = [w for w in R2 if w[0] >= T]
    seams.append(f'{k1}|{k2} cut at {T/1000:.1f}s (pause {best[0] if best else "?"} ms)\n  A: ' +
                 ' '.join(w[2] for w in allw if T - 9000 <= w[0] < T + 9000) + '\n  B: ' +
                 ' '.join(w[2] for w in R2 if T - 9000 <= w[0] < T + 9000) + '\n  joined: ' +
                 ' '.join(w[2] for w in left[-10:]) + ' ‖ ' + ' '.join(w[2] for w in right[:10]))
    allw = left + right
os.makedirs(O, exist_ok=True)
json.dump(allw, open(f'{O}/sarw.json', 'w', encoding='utf-8'), ensure_ascii=False)
open(f'{O}/sar.txt', 'w', encoding='utf-8').write(' '.join(w[2] for w in allw))
open(f'{O}/seams.txt', 'w', encoding='utf-8').write('\n\n'.join(seams) + '\n')
print('total tokens', len(allw), 'seams', len(seams))
