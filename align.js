/* Sudhar Desk — follow-along alignment
   Lines up the YouTube caption words (each with a start time) with the words of
   the transcript as it is right now, so the spoken word and sentence can be lit
   up in the editor. It runs in the browser on every load / after edits, so the
   transcript can be corrected freely: the timings follow the corrected text.

   align(text, caps) -> { words:[{s,e,t,m}], sent:[{s,e}] }
     text  the transcript (string)
     caps  [[ms, word], ...] from sync/<videoId>.tsv
     s,e   character range of the word in text
     t     start time (ms) — taken from the caption when matched (m=1),
           otherwise interpolated between neighbours (m=0)
*/
(function (root) {
  'use strict';

  const TOKEN = /[઀-૿A-Za-z0-9‌‍]+/g;

  /* spelling-insensitive key: ASR and the corrected text often differ only in
     long/short vowels, anusvara, nukta or the ZWJ */
  function key(w) {
    return w
      .replace(/[‌‍ઁં઼]/g, '')
      .replace(/ી/g, 'િ')   // ી -> િ
      .replace(/ૂ/g, 'ુ')   // ૂ -> ુ
      .replace(/ઈ/g, 'ઇ')   // ઈ -> ઇ
      .replace(/ઊ/g, 'ઉ')   // ઊ -> ઉ
      .replace(/ણ/g, 'ન')   // ણ -> ન
      .replace(/ળ/g, 'લ')   // ળ -> લ
      .toLowerCase();
  }

  function lev(a, b) {
    if (a === b) return 0;
    const n = a.length, m = b.length;
    if (!n) return m; if (!m) return n;
    let prev = new Array(m + 1), cur = new Array(m + 1);
    for (let j = 0; j <= m; j++) prev[j] = j;
    for (let i = 1; i <= n; i++) {
      cur[0] = i;
      const ai = a.charCodeAt(i - 1);
      for (let j = 1; j <= m; j++) {
        const c = ai === b.charCodeAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
      }
      const t = prev; prev = cur; cur = t;
    }
    return prev[m];
  }
  function sim(a, b) {
    if (a === b) return 1;
    const L = Math.max(a.length, b.length);
    if (!L) return 0;
    // cheap reject: very different lengths
    if (Math.abs(a.length - b.length) / L > 0.6) return 0;
    return 1 - lev(a, b) / L;
  }

  const GAP = 0.6, MISS = 1.25, OK = 0.6;   // costs and the "counts as a match" threshold

  /* edit-distance alignment of doc[d0..d1) with cap[c0..c1);
     freeHead/freeTail: caption words before/after the doc may be skipped for free */
  function dp(D, C, d0, d1, c0, c1, freeHead, freeTail, out) {
    const n = d1 - d0, m = c1 - c0;
    if (!n || !m) return;
    const W = m + 1;
    const cost = new Float32Array((n + 1) * W);
    const bt = new Uint8Array((n + 1) * W);        // 1 diag, 2 up (doc gap), 3 left (cap gap)
    for (let j = 1; j <= m; j++) { cost[j] = freeHead ? 0 : j * GAP; bt[j] = 3; }
    const simCache = new Map();
    for (let i = 1; i <= n; i++) {
      const row = i * W, prow = row - W;
      cost[row] = i * GAP; bt[row] = 2;
      const dk = D[d0 + i - 1];
      for (let j = 1; j <= m; j++) {
        const ck = C[c0 + j - 1];
        let s;
        if (dk === ck) s = 1;
        else { const k = dk + '\u0001' + ck; s = simCache.get(k); if (s === undefined) { s = sim(dk, ck); simCache.set(k, s); } }
        const sub = s >= OK ? (1 - s) * 0.5 : MISS;
        let best = cost[prow + j - 1] + sub, b = 1;
        const up = cost[prow + j] + GAP; if (up < best) { best = up; b = 2; }
        const lf = cost[row + j - 1] + (freeTail && i === n ? 0 : GAP); if (lf < best) { best = lf; b = 3; }
        cost[row + j] = best; bt[row + j] = b;
      }
    }
    let i = n, j = m;
    while (i > 0 && j > 0) {
      const b = bt[i * W + j];
      if (b === 1) {
        const dk = D[d0 + i - 1], ck = C[c0 + j - 1];
        if (dk === ck || sim(dk, ck) >= OK) out[d0 + i - 1] = c0 + j - 1;
        i--; j--;
      } else if (b === 2) i--; else j--;
    }
  }

  function align(text, caps) {
    /* doc tokens */
    const words = [];
    TOKEN.lastIndex = 0;
    let mt;
    while ((mt = TOKEN.exec(text))) words.push({ s: mt.index, e: mt.index + mt[0].length, t: 0, m: 0 });
    const D = words.map(w => key(text.slice(w.s, w.e)));
    const C = caps.map(c => key(c[1]));
    const n = D.length, m = C.length;
    const match = new Int32Array(n).fill(-1);

    if (n && m) {
      /* 1. anchors: word triples that occur exactly once on both sides */
      const tri = (A, i) => A[i] + ' ' + A[i + 1] + ' ' + A[i + 2];
      const cnt = (A) => { const M = new Map(); for (let i = 0; i + 2 < A.length; i++) { const k = tri(A, i); M.set(k, M.has(k) ? -1 : i); } return M; };
      const dm = cnt(D), cm = cnt(C);
      const pairs = [];
      for (const [k, di] of dm) { if (di < 0) continue; const ci = cm.get(k); if (ci !== undefined && ci >= 0) pairs.push([di, ci]); }
      pairs.sort((a, b) => a[0] - b[0]);
      /* 2. keep the longest chain that moves forward in both texts (LIS on caption index) */
      const tails = [], prevIdx = new Int32Array(pairs.length).fill(-1), tailIdx = [];
      for (let p = 0; p < pairs.length; p++) {
        const v = pairs[p][1];
        let lo = 0, hi = tails.length;
        while (lo < hi) { const md = (lo + hi) >> 1; if (tails[md] < v) lo = md + 1; else hi = md; }
        tails[lo] = v; tailIdx[lo] = p; prevIdx[p] = lo ? tailIdx[lo - 1] : -1;
      }
      const chain = [];
      for (let p = tailIdx[tails.length - 1]; p !== undefined && p >= 0; p = prevIdx[p]) chain.push(pairs[p]);
      chain.reverse();
      /* drop anchors whose triples overlap the previous one inconsistently */
      const anchors = [];
      for (const a of chain) {
        const last = anchors[anchors.length - 1];
        if (last && (a[0] < last[0] + 3 || a[1] < last[1] + 3)) {
          if (a[0] - last[0] === a[1] - last[1]) anchors.push(a);   // same run — fine
          continue;
        }
        anchors.push(a);
      }
      /* 3. fill: each anchor fixes 3 words; align the stretches in between */
      let pd = 0, pc = 0, first = true;
      for (const [di, ci] of anchors) {
        if (di < pd || ci < pc) continue;
        dp(D, C, pd, di, pc, ci, first, false, match);
        for (let k = 0; k < 3; k++) match[di + k] = ci + k;
        pd = di + 3; pc = ci + 3; first = false;
      }
      /* tail (or everything, when no anchors were found) */
      if (n - pd > 0 && m - pc > 0) {
        if ((n - pd) * (m - pc) <= 30e6) dp(D, C, pd, n, pc, m, first, true, match);
      }
    }

    /* 4. times: matched words take the caption time; the rest are spread by
          character position between the nearest matched words */
    const known = [];
    for (let i = 0; i < n; i++) if (match[i] >= 0) { words[i].t = caps[match[i]][0]; words[i].m = 1; known.push(i); }
    if (known.length) {
      const f = known[0], l = known[known.length - 1];
      let rate = 75;   // ms per character, used only beyond the first/last match
      if (l > f) rate = Math.max(30, Math.min(200, (words[l].t - words[f].t) / Math.max(1, words[l].s - words[f].s)));
      for (let i = 0; i < f; i++) words[i].t = Math.max(0, words[f].t - (words[f].s - words[i].s) * rate);
      for (let i = l + 1; i < n; i++) words[i].t = words[l].t + (words[i].s - words[l].s) * rate;
      for (let k = 0; k + 1 < known.length; k++) {
        const a = known[k], b = known[k + 1];
        if (b - a < 2) continue;
        const ta = words[a].t, tb = words[b].t, sa = words[a].s, sb = words[b].s;
        for (let i = a + 1; i < b; i++) words[i].t = ta + (tb - ta) * (words[i].s - sa) / Math.max(1, sb - sa);
      }
      for (let i = 1; i < n; i++) if (words[i].t < words[i - 1].t) words[i].t = words[i - 1].t;   // never go backwards
    }

    /* sentences: split after . ? ! । ॥ or a blank line */
    const sent = [];
    const re = /[.?!।॥]+["'”’)\]]*|\n\s*\n/g;
    let st = 0, ms;
    while ((ms = re.exec(text))) {
      const e = ms.index + ms[0].length;
      if (text.slice(st, e).trim()) sent.push({ s: st, e });
      st = e;
    }
    if (text.slice(st).trim()) sent.push({ s: st, e: text.length });
    for (const s of sent) {   // trim leading/trailing whitespace from each sentence range
      while (s.s < s.e && /\s/.test(text[s.s])) s.s++;
      while (s.e > s.s && /\s/.test(text[s.e - 1])) s.e--;
    }

    const matched = known.length;
    return { words, sent, matched, total: n };
  }

  /* index of the word being spoken at time t (ms) */
  function wordAt(words, t) {
    let lo = 0, hi = words.length - 1, ans = -1;
    while (lo <= hi) { const md = (lo + hi) >> 1; if (words[md].t <= t) { ans = md; lo = md + 1; } else hi = md - 1; }
    return ans;
  }
  function sentAt(sent, pos) {
    let lo = 0, hi = sent.length - 1, ans = -1;
    while (lo <= hi) { const md = (lo + hi) >> 1; if (sent[md].s <= pos) { ans = md; lo = md + 1; } else hi = md - 1; }
    return ans;
  }
  function wordAtChar(words, pos) {
    let lo = 0, hi = words.length - 1, ans = 0;
    while (lo <= hi) { const md = (lo + hi) >> 1; if (words[md].s <= pos) { ans = md; lo = md + 1; } else hi = md - 1; }
    return ans;
  }
  function parseTsv(txt) {
    const out = [];
    for (const line of txt.split(/\r?\n/)) {
      if (!line || line[0] === '#') continue;
      const tab = line.indexOf('\t');
      if (tab < 0) continue;
      const t = +line.slice(0, tab);
      if (isFinite(t)) out.push([t, line.slice(tab + 1).trim()]);
    }
    return out;
  }

  const api = { align, wordAt, sentAt, wordAtChar, parseTsv, key };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SudharAlign = api;
})(this);
