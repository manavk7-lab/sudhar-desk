# Sudhar Desk — notes for Claude

Manav (CA, Surat) corrects Gujarati transcripts of Divyangsaheb's discourses (Vigyan Sankul YouTube: the Upanishad
series, શાશ્વત સંવાદ, યથાર્થ ગીતા સાર) in this app: YouTube video + his Google Doc side by side, every edit saved into
the Doc. Claude corrects each Doc first (speech recognisers + rules learnt from Manav's own edits), then Manav listens.

**When asked to correct a video, read `pipeline/PROCESS.md` first** (the whole process, step by step, with the
commands), then `proofreading/RULES.md` (what to write) and `proofreading/JUDGE.md` (how to decide).

## Map
- `index.html` — the app (one file). `BUILTIN_PAIRS` = the video ↔ Doc list. Bump `APP_VERSION` + `version.txt` on changes.
- `sync/<videoId>.tsv` — caption word times (follow-along highlight, and video times for ✎ items).
- `review/<videoId>.json` — the ✎ list of every change Claude made (Manav checks / undoes them in the app).
- `proofreading/` — RULES.md, JUDGE.md, CANDS.md, PUNCT.md, NOGEM.md, GUIDE.md (judge instructions and Manav's rules).
- `pipeline/` — PROCESS.md and the scripts (`t/`, `bin/`, `browser/`); they run from a work folder outside the repo.
- `apps-script/doc-sync.gs` — the Google Apps Script bridge that reads/writes the Docs (deployed by Manav).

## Never
- Never put the Apps Script `SECRET`, the `CAP_KEY`, or any API key (Sarvam, Gemini) in chat, in a file in this repo,
  or in a commit. They live only in Manav's Apps Script, his browser, and the work folder (`*.key`, `capkey.txt`).
- Never write a Doc except through the hash-checked post (PROCESS.md C10): stop if the Doc changed since it was read.
- Never change the speaker's words to "better Gujarati"; no quotation marks or brackets in transcripts.
- Never try to get around YouTube's bot checks (other yt-dlp clients etc.); use Manav's own browser.
- Ask Manav before anything that cannot be undone.
