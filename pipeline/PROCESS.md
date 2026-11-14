# How a video gets corrected — the full process

Written 31 Oct 2026 after ઉપનિષદ - 1, 40 and 41. It is for Manav, and for any new Claude session that has to carry on
the work (Claude Code, or a claude.ai session with this repo attached). Read it top to bottom once, then follow
**Part C** step by step.

---------------------------------------------------------------------------------------------------------------

## Part A — What we are doing and why

**The goal.** Divyangsaheb's Gujarati discourses (Vigyan Sankul YouTube, the Upanishad series and શાશ્વત સંવાદ) already
have rough transcripts in Google Docs (made from YouTube's auto-captions and partly cleaned by an AI). Manav corrects
them by listening in **Sudhar Desk** (this repo, https://manavk7-lab.github.io/sudhar-desk/): video on one side, the
Doc on the other, every edit saved straight into the Doc. Before he listens, Claude corrects as much as it safely can,
so that his own pass is mostly confirming.

**The one principle.** The speaker's exact words, not "better Gujarati". Spoken forms stay (કે છે, તું, આયા, જાવ …).
Over-correcting is the main failure. Every change Claude makes goes on the **✎ list** in Sudhar Desk, so Manav can see
it, jump to that moment in the video, and undo it with one key.

**How Claude decides a word.** No single machine is trusted. For every spot, Claude compares:

| Source | What it is | Weight |
|---|---|---|
| **Doc** | the existing transcript | the starting point; kept unless clearly wrong |
| **S** — Sarvam (`saaras:v4`, gu-IN) | best Gujarati speech recogniser, from the real audio | strong |
| **G** — Gemini (`gemini-3.8-flash`) | second independent recogniser from the audio; sometimes "tidies" speech | strong |
| **Y** — YouTube auto-captions | weak; the Doc was usually made from these, so Y agreeing with the Doc proves nothing | info |
| **B** — the book બ્રહ્મ વિદ્યા ખંડ | the Gujarati translation the speaker reads aloud, often word for word | info for names, terms, verses |

Where S and/or G hear something different from the Doc, a **judge** (a Claude sub-agent with the written rules) decides
**fix / maybe / ask / keep**. Claude then reviews the judges' decisions itself, adds the mantras in standard text, the
આગળે spots, and the punctuation, and posts the whole corrected text into the Doc in one go.

**How well it works (from Manav's own checking).**
- Videos 9 (rest)–13: he undid 19 of 1,159 changes.
- ઉપનિષદ - 1: he kept 277 of 288 traceable changes (96%). Agreement of all engines is NOT proof when the Doc's word fits.
- Most common remaining misses: dropped small words (છે, એ, ને, આમ, એમ, આ, અને, જ), and આગળે.

All of Manav's corrections are turned into written rules: **`proofreading/RULES.md`** (what to write) and
**`proofreading/JUDGE.md`** (how judges decide). Those two files are the "findings"; read them before judging anything.

---------------------------------------------------------------------------------------------------------------

## Part B — What you need before starting (one-time setup)

### B1. Accounts, files, access
- **Docs** live in Google Drive, folder `vigyan_sankul_transcripts › Upanishad_Series_corrected`
  (find it with the Drive connector's search), named `UPNISHAD -video NN.corrected`. Owner: upnishad321@gmail.com
  (Manav's second account). Earlier series (શાશ્વત સંવાદ) are in other folders; their Doc ids are in `index.html`.
- **The Apps Script must be able to edit the Doc** before Claude (or Sudhar Desk) can save into it. The script runs
  as Manav's manavk7@gmail.com account, not as the Docs' owner, so each Doc needs either "Anyone with the link: Editor"
  (what Docs 1, 40, 41 have) or — safer, because the Doc ids are visible in this public repo — manavk7@gmail.com added
  as Editor. Docs 40 and 41 were "Viewer" at first; saving then fails with `TypeError: Failed to fetch` (the script
  throws and the browser hides the reason). Check with the Drive connector's get_file_permissions.
- **The book** બ્રહ્મ વિદ્યા ખંડ (PDF Manav uploaded, ~270+ pages, scanned: Sanskrit in Devanagari + Gujarati
  translation/commentary). PDF pages: મંડલબ્રાહ્મણ 238–247 (2nd ખંડ from 242), Mahavakya, Maitreya, Yajnavalkya 248–271. The speaker reads from it but not
  always exactly ("speaker might have changed, but it can be a reference" — Manav). If a new session does not have the
  PDF, ask Manav to attach it again.

### B2. The Apps Script bridge (`apps-script/doc-sync.gs`)
Sudhar Desk reads and writes Docs through Manav's Apps Script web app ("sudhar-desk doc sync"). It has two secrets
that must NEVER go into chat, commits, or files in this repo:
- `SECRET` — the token Sudhar Desk sends with every read/write. It lives only in the deployed script and in the
  Sudhar Desk settings of Manav's browser. Claude never needs to see it: it writes through the Sudhar Desk tab,
  which already has it (`gasGetText(docId)`, `gasPost({...})` are functions of the page).
- `CAP_KEY` — a temporary hand-off key that lets the cloud session put/get data (audio parts, caption files, a new Doc
  text) in the script's 6-hour cache (`action: putcap / getcap`). Set it to a long random string in the deployed
  script while a series is being processed; set it back to `''` (and deploy) when the series is done.
  **It is ON at the moment (30–31 Oct).** Its value is on the `const CAP_KEY` line of the deployed script;
  Manav can copy it from script.google.com into the work folder's `capkey.txt`.
- The script's /exec URL goes into the work folder's `gasurl.txt`.

### B3. Keys and tools in the work folder (never in the repo)
Make a work folder outside the repo (in a cloud session: the session scratchpad) and:
```
export SD_WORK=/path/to/work        # all scripts run from here
export SD_REPO=/path/to/sudhar-desk # this repo
cp -r $SD_REPO/pipeline/t $SD_REPO/pipeline/bin $SD_WORK/
mkdir -p $SD_WORK/proof && cp $SD_REPO/proofreading/*.md $SD_WORK/proof/
# put these four files in $SD_WORK (ask Manav; never print them, never commit them):
#   sarvam.key   Sarvam API subscription key        gemini.key   Google AI Studio (Gemini) key
#   gasurl.txt   the Apps Script /exec URL          capkey.txt   the current CAP_KEY
pip install sarvamai google-genai rapidfuzz numpy   # (+ --break-system-packages in the cloud container)
# ffmpeg, ffprobe and node must exist
```
**Costs.** Sarvam ≈ ₹30 per hour of audio (2.77 h for videos 40+41 cost ≈ ₹83; ≈ ₹65 was left on 30 Oct).
Gemini is prepaid credit; it ran out on 30 Oct (error 402 RESOURCE_EXHAUSTED), so 40/41 were done with Sarvam only.
Check both before starting a long video, and tell Manav if the credit will not cover it.

### B4. The browser
Claude in Chrome must be connected to Manav's Chrome. Two kinds of tabs are used:
- a **Sudhar Desk tab** (https://manavk7-lab.github.io/sudhar-desk/ with his settings loaded) — for reading/writing Docs;
- **YouTube watch tabs** — for recording the audio and reading the captions (his own logged-in browser, so YouTube
  works normally). Close them when done.
Never return URLs with query strings from javascript_tool (keys would show). Do not use keyboard shortcuts inside
Google Docs. Do not try other YouTube "player clients" or tricks to get around YouTube's bot checks — that is not
allowed; captions and audio are taken in Manav's own browser instead.

---------------------------------------------------------------------------------------------------------------

## Part C — Step by step for one video

Names used below: `VM` = a working folder for this video inside `$SD_WORK` (e.g. `v39`), `YT` = YouTube id,
`DOC` = Google Doc id. All commands run in `$SD_WORK`.

### C1. Find the video and its Doc
1. Manav gives a **video number** NN. It is the number in the Drive index PDF **"108 Upnishad video series"**
   (find it with the Drive search; it lists `UPNISHAD -video NN https://youtu.be/<id>` for every video, including
   38-1/38-2 style splits). The Doc has the same number: **`UPNISHAD -video NN.corrected`** (Drive search
   `title contains 'UPNISHAD -video NN'`; the `.txt` with the same name is an older raw file — ignore it).
   (The YouTube playlist position is different: video 40 is the 37th in the playlist. Don't use playlist positions.)
1b. **Check the Doc's Drive folder** (get_file_metadata → parentId): Docs to correct are in "Upanishad_Series_corrected";
   a Doc in **"total final"** is finished by Manav — never change it (Manav, 4 Nov: 40 and 41 "finished so not to touch").
2. Read the Doc's first paragraphs to know which Upanishad and which part (it usually says what was done "ગઈકાલે").
3. Check that the Apps Script can edit the Doc (B1).
4. Save the Doc's current text: in the Sudhar Desk tab `await gasGetText(DOC)` → keep its sha256 (first 16 hex
   chars) — this is the **OLD** hash that protects Manav's edits later. (Or Drive's read_file_content to read.)
   Write it to `VM/doc_orig.txt` (stage it through `bin/getdoc.py` if the text has to come through the cache).

### C2. Add the video to Sudhar Desk, with caption word times (follow-along)
0. **The relay (set up once per YouTube tab).** The YouTube tab must not be given the Apps Script URL or keys, so data
   leaves it through a small relay page on Sudhar Desk's own site, which reads the saved settings itself:
   inject `pipeline/browser/relay_yt.js` into the YouTube tab, then make a real click (computer tool) on the yellow
   "open relay" button it adds — a window can only be opened by a click. A new tab on manavk7-lab.github.io opens
   (sometimes the full Sudhar Desk app instead of version.txt; that works too). Inject `browser/relay_page.js` there
   with `__CK__` filled. Test from the YouTube tab: `await window.__sdput('test',0,'hi')` → `true`.
   (Opening YouTube *from* Sudhar Desk does not work: YouTube's opener policy cuts the link in that direction.)
1. In the YouTube tab run `pipeline/browser/captions.js` (`__KEY__` = e.g. `cap39`). It takes the player's own
   caption request (or turns CC on for a moment), fetches it as json3, makes word lines `ms<TAB>word` and sends them
   through the relay. Then in the work folder: `python3 bin/fetchcap.py cap39 $SD_REPO/sync/YT.tsv`.
2. Add `{yt:'YT',doc:'DOC',title:'ઉપનિષદ - NN · <Upanishad names>'}` at the top of `BUILTIN_PAIRS` in `index.html`,
   bump `APP_VERSION` in index.html and `version.txt` (format `2026-10-31a`), commit, push, check the live site.

### C3. Record the audio (in Manav's Chrome, real time)
- `pipeline/browser/recorder3.js` is a template (fill `__KEY__`, `__START__`, `__END__`); it needs the relay (C2.0) in
  that YouTube tab. Inject it into a YouTube watch tab with javascript_tool. It waits out ads, seeks with the
  player's own `seekTo` (setting `video.currentTime` does not work), records the tab's audio with MediaRecorder
  (opus 24 kb/s, 60 s chunks; the tab stays silent) and sends each chunk through the relay to the cache as base64
  parts. Check progress with `window.__R` (`t` = video time, `part`, `failed`). (`t/recorder2.js` is the older version
  that called the script directly.)
- Real time: a 2-hour video takes 2 hours. To go faster, split the video into 2–3 ranges and record them at the same
  time in separate tabs (each with its own relay), keys `p1a`, `p1b`, `p1c` (ranges overlapping by ~20 s).
- In the cloud session, start a **collector** for the keys with the Bash tool's run_in_background (not `&`, which gets
  killed): `python3 bin/collect.py p1a,p1b,p1c audio/m39 > audio/m39/collect.log`. It saves every part as it arrives.

### C4. Transcribe (Sarvam + Gemini) while recording continues
`python3 t/stream2.py audio/m39 p1a,p1b,p1c audio/m39/collect.log` (run_in_background). It decodes the parts as they
arrive, cuts ~10-minute pieces at silences, and sends every piece to Sarvam and Gemini in parallel
(`KEY_pNN.sar.txt`, `KEY_pNN.gem.txt`). `NOGEM=1 python3 t/stream2.py …` = Sarvam only (when Gemini has no credit).
If Gemini refuses a piece (block_reason OTHER), `python3 t/gemsplit.py audio/m39/p1a_p03` re-does it in ~150 s pieces.

### C5. Clean the Doc ("backbone") and find the mantras
1. `python3 t/backbone_m.py VM VM/doc_orig.txt VM/doc.txt VM/backbone_items.json $SD_REPO/sync/YT.tsv`
   — removes quotation marks, brackets → commas (no brackets in transcripts), joins paragraphs that break in the middle
   of a sentence (RULES 12), applies the section-2 spellings (નહી→નહીં …). Every change except removing quotes becomes
   an `auto` ✎ item. (Edit the FIX lists in the script for the new video if needed.)
2. **Book pages** for this Upanishad: render the PDF pages (`pdftoppm -r 150 -f P -l Q book.pdf p`), OCR them
   (`python3 t/ocrbook.py gemini-3.8-flash book/ocr p-*.png` — needs Gemini; without credit use Tesseract with the
   Gujarati + Sanskrit models from github.com/tesseract-ocr/tessdata_best (`guj`, `san`; download from
   raw.githubusercontent.com, set TESSDATA_PREFIX): `pdftoppm -r 300 -gray`, then `tesseract page.pgm out -l guj+san
   --psm 6` — good enough for the B reference; check verses by eye or online), save the Gujarati text as `book/NAME_gu.txt` and the Devanagari verses via
   `python3 t/bookverses.py book/NAME.txt book/NAME_verses.json` (Gujarati script via `t/deva2gu.py`).
3. `python3 t/findmantras.py VM/doc.txt book/NAME_verses.json > VM/mantra_report.txt` — where the speaker recites the
   book's Sanskrit. Also look for shanti paths, Gita verses, stotras, Gayatri etc. by reading the Doc.
4. For each recited mantra write an item in `VM/mantra_draft.json`:
   `{"alt": "<the Doc's text exactly>", "cur": "<standard text, lines separated by \n>", "why": "...", "conf": "likely"}`.
   Standard text = from the book, checked against a reliable online source (RULES section 5): Gujarati script, ં ઃ ્,
   words joined as printed, one printed line per line, "।" at line ends, "॥" at verse end, ONLY the part he recites,
   his Gujarati in between stays.

### C6. Fuse the recognisers with the Doc and prepare the judges
`bash t/fusem.sh VM audio/m39 YT book/NAME_gu.txt p1a p1b p1c`
- assembles `VM/sar.txt` (and `VM/gem.txt` if every piece has Gemini), merging the overlaps;
- `t/fuse2.py` aligns S, G (and Y) to the Doc word by word and makes one item per disagreement (`VM/items_all.json`);
- `t/dropmantra.py` drops items inside recited mantras (they are replaced whole in C8);
- `t/bookref.py` adds the book's matching sentence (B) to each item;
- `t/prepjudge.py` writes judge files `VM/j_1.txt, j_2.txt …` (150 items each) and `VM/j_kept.json`;
- `t/cands2.py` + `t/candlines.py` write `VM/cands.txt`: rule-based spots from Manav's lessons (એને→એણે doer,
  lone શું?, Sanskrit endings, એ→ય …) for a second kind of judge.

### C7. Judges, then Claude's own review
1. Run one sub-agent per `j_N.txt`, in parallel, with this brief:
   "Read `proof/JUDGE.md` and `proof/RULES.md` (and `proof/NOGEM.md` if there is no G). Judge every line of
   `VM/j_N.txt` as JUDGE.md says. Write `VM/j_N_out.json` exactly in JUDGE.md's format. Reply with only the counts of
   fix / maybe / ask." One more sub-agent for `VM/cands.txt` with `proof/CANDS.md` → `VM/cands_out.json`
   (merge several outputs into one `cands_out.json`).
2. `python3 t/finalvid.py m39` (folder name `v` + argument) applies the decisions → `VM/new.txt`, `VM/rev_new.json`.
3. **Claude's own review** — never skip: `python3 t/showdec2.py m39` lists every decision and flags the kinds Manav
   has undone before (RULES 11 and 13). Correct the judges in `VM/override.json`
   `{"DROP":{"c12":"why"}, "ASK":{…}, "MAYBE":{…}, "TEXT":{"c40":["new text","why"]}}` and run
   `python3 t/override_m.py VM`. Typical overrides: a fix that changes a meaningful word all engines merely
   "standardise"; a closing કે/છે put after a full stop; a fix that copies book words he did not say.
4. Fixes a judge cannot express (a word moved across a full stop, a restatement) go in `VM/manual.json` as
   `{"alt","cur","why","conf"}` and are applied with `python3 t/mantra_apply.py VM/new.txt VM/manual.json VM/new_o.txt VM/rev_manual.json`.
   Easier: write the fixes as rows `[pattern, replacement, why, conf, mode]` in `VM/manual_spec.json` (mode `once` = the
   exact text, which must occur once; `all` = a regex, every match its own item) and build the items on the current text:
   `python3 t/manualgen.py VM/new.txt VM/manual_spec.json VM/manual.json`. DROP a judge decision that the manual row
   replaces (two items changing the same words break each other in the app).
   **Paragraph breaks inside a sentence** (RULES 12): `python3 t/parabreaks.py VM/doc.txt VM/sar.txt` lists every
   paragraph break where Sarvam reads the words across it as one sentence. Read each: join the real ones (the next
   paragraph starts with a fragment: "…તેને તારે પ્રગટ.⏎⏎કરવી પડશે …") with a manual row; a new sentence of the book
   stays. Maha part 3 had 17 such breaks.

### C8. Mantras and આગળે
1. `python3 t/mantra_apply.py VM/new_o.txt VM/mantra_draft.json VM/new_m.txt VM/rev_mantra.json`
   — single line breaks between the mantra lines and around the mantra (RULES 5: Manav removed the empty lines in
   ઉપનિષદ - 39 and 41, 3–4 Nov). Do not pass `nn` (the old layout with an empty line between the lines). Put the text just
   before the mantra into `alt`/`cur` too, so `cur` can start "…થાય છે:\nૐ …".
2. **આગળે** (RULES 1, JUDGE 14): after અહીંયા / અહીં / ત્યાં / જ્યાં / ક્યાં meaning "at that place", the speaker almost
   always says આગળે though every engine writes આગળ. Find every such spot by reading, write `VM/agale_draft.json`
   items (conf `likely`) and apply: `python3 t/mantra_apply.py VM/new_m.txt VM/agale_draft.json VM/new_a.txt VM/rev_agale.json`.
   Keep આગળ for "forward / further / next" (આગળ વધે, આગળ કહે છે, એનાથી આગળ).

### C9. ✎ items and punctuation
1. `python3 t/collect_items.py VM` → `VM/items_pre.json` (all items: backbone, judges, overrides, manual, mantras,
   આગળે), then `python3 t/addtimes.py VM/new_a.txt $SD_REPO/sync/YT.tsv VM/items_pre.json` (video time of each item).
2. **Pauses**: `python3 t/pauses.py VM/new_a.txt $SD_REPO/sync/YT.tsv VM/pauses.json audio/m39/p1a.wav:START[:OFFSET] …`
   measures the silence at every word boundary in the recorded audio (START = where that recording began in the
   video; give OFFSET when the automatic match goes wrong — it once picked a 65 s offset for p1b). Read the printed
   offsets: a jump that comes back later (v19b: 0.16 → 1.16 → 0.12) is a false lock — rerun that part with
   `part.wav:START:OFFSET:fix` (one offset for the whole part). Meditation videos with music give no reliable offsets.
   A recording made in another audio folder: COPY its `_pNN.sar.txt` files (assemble3.sh checks sizes; a symlink looks empty).
3. `python3 t/punctcands.py VM/new_a.txt VM/pauses.json VM/pc` → `VM/pc.txt`: full stops where he does not pause,
   and long pauses without a stop. Judge it with sub-agents using `proof/PUNCT.md` (→ `VM/pc_N_out.json`).
   Rule: a full stop needs BOTH a pause and a finished meaning; never a paragraph break inside a sentence.
4. `python3 t/applypunct.py VM/new_a.txt VM/pc.json VM/final.txt VM/rev_punct.json VM/pc_1_out.json …`
   and carry the items over: `python3 t/fixitems.py VM/new_a.txt VM/final.txt VM/items_pre.json VM/items_all_final.json`
   **Overlaps:** `python3 t/overlapcheck.py VM/final.txt VM/items_all_final.json` lists ✎ items whose CHANGED text overlaps
   another item (a manual or punctuation fix made on top of a judge fix). Fold each such pair into one item (alt = the
   oldest text, cur = the text now), otherwise undoing one in the app breaks the other. Items that only share
   unchanged context words are harmless. collect_items.py reports items it cannot find ("LOST") — fold those the same way.
   (add the punctuation items from rev_punct.json). Check: every item's `cur` occurs exactly once in final.txt.
5. Last checks on final.txt: no quotation marks or brackets; every paragraph ends in a stop (except the closing
   "જય સચ્ચિદાનંદ" and the line just before a mantra); mantras laid out as in C5.4; sha256 of the text = **NEW**.
   `python3 t/lastcheck.py VM/final.txt VM/items_all_final.json` does these checks, and
   `python3 t/revertcheck.py VM/final.txt VM/items_all_final.json VM/doc_orig.txt` undoes every ✎ item and compares with
   the Doc as read: it must print 0 unexplained diffs (then every change is on the ✎ list and can be undone).
   Watch applypunct next to a ":" — it once wrote "છે.:"; and fold a punctuation item into a check item or a join it
   touches (or drop the punctuation change).

### C9b. Book wording (when the speaker reads from the book) — Manav, 1 Nov: "always see what is written in book"
`python3 t/bookalign.py VM/final.txt VM/bookalign.json book/NAME.txt[,book/OTHER.txt] 80` lists every place inside a
read sentence where the Doc has different words than the book (`sub`), extra words (`extra`, his own additions — keep)
and book words not in the Doc (`skip`). For each `sub`: if he is reading that sentence, write the book's words and
spelling, brackets included (his own example: "મંત્રો અને ચિંતન સાધનાના અધમ" → "મંત્રોનું ચિંતન (સાધના) અધમ"), even
when Sarvam agrees with the Doc. Skip alignment mistakes (a clause matched in the wrong place) and OCR noise — with
Tesseract OCR, check each word on the page image. Apply with mantra_apply.py as "book" ✎ items (conf likely).
(`t/bookcheck.py` is the older side-by-side listing with Sarvam.)
**Refined 4 Nov from Manav's own passes (RULES 5, JUDGE 15):** take the book's word only where the Doc MISHEARD it (a
wrong or garbled word that sounds like the book's: પ્રણવવિધ→પ્રણવવિદ, ઉપયુક્ત→ઉપર્યુક્ત, અંતરલક્ષ→અંતર્લક્ષ્ય). Leave
words he really said (રહેલા/રહેલ, બંને/બંનેય, પર/ઉપર, કહેવામાં આવે છે/કહે છે) and pure spelling (anusvara, halant,
દ્રષ્ટિ/દૃષ્ટિ, મંડળ/મંડલ, digits/words) — in ઉપનિષદ - 39 he changed none of 40 such spots. A clear difference in a
content word that Sarvam confirms becomes a `check` item (cur = his words, alt = the book's) so one key switches it.
Better: write a clean book text by reading the page images (`book/NAME_gu_clean.txt`, one verse per line) — the
Tesseract text is too noisy for word-level alignment — and run bookalign.py on the Doc before the judges (it shows
which sentences are read), then again on new.txt after them.

### C10. Post into the Doc (with the hash check)
1. Stage the text: `python3 bin/putdoc.py post39 VM/final.txt` (cache key `post39`, 6 hours).
2. Fill the template: `python3 t/mkjs.py t/postjob.js KEY=post39 DOC=<doc id> OLD=<old sha16> NEW=<new sha16> > post39.js`
   (the script URL and CAP key are filled from the work folder) and inject post39.js into the Sudhar Desk tab. It downloads the staged text, checks its hash is NEW, reads the Doc and **stops if the Doc is no
   longer OLD** (Manav has edited it — then rebuild from his version, never overwrite), writes the full text, reads
   it back and checks it is NEW. Poll `window.__jobPost` until `st:'done'` (`changed` / `verify-mismatch` / `err` =
   stop and look). A javascript_tool call times out after 45 s, so never wait longer than ~30 s in one call.
3. Any posted version can be undone from the Doc's version history (File › Version history).
4. **Without the cache key in the browser (6 Nov, from ઉપનિષદ - 12 on).** Claude must never read the cache key into its
   own context, so a post no longer goes through getcap. Instead inject `browser/posttext.js` into the Sudhar Desk tab (it
   needs no key: it uses the app's own `gasGetText`/`gasPost`), split the text with `python3 t/chunks.py VM/final.txt 3000`
   (line ranges + sha16 per piece), pass each piece with `await __putChunk(KEY, i, \`…\`, sha16)` (refused unless the hash
   matches — so a copying slip can never reach the Doc), then `await __postText(KEY, n, DOC, OLD, NEW)`: the same hash
   check as above (stops with st 'changed' if the Doc is no longer OLD), write, read back, check = NEW.
5. **Reading a Doc without the key** (`__fwdDoc` in the Sudhar Desk tab): the text goes app tab → BroadcastChannel
   'sd-fwd' → a relay tab (bridge: forwards to its opener) → that YouTube tab (`__sdput`, the recorders' own upload path)
   → cache → `bin/getdoc.py KEY VM/doc_orig.txt`. The bridge and the YouTube-tab listener are small injections, no key.
6. The app reloads itself after every push that changes APP_VERSION — everything injected into the Sudhar Desk tab is
   gone then: inject posttext.js / __fwdDoc again (wait until `typeof gasGetText==='function'`).

### C11. The ✎ list and the report
1. `python3 t/merge_review.py $SD_REPO/review/YT.json VM/final.txt VM/items_all_final.json <tag>` — items have
   `id, cur (text now), alt (text before), kind (applied / check / auto), conf, why, heard, t (ms)`.
2. Commit `review/YT.json` (+ rule changes) with the attribution lines, push, and check the live site serves it.
3. Tell Manav per Doc: words fixed, mantras, આગળે (likely), how many spots to listen to, what was not possible,
   credit used. Then learn from his finished pass (C12).

### C12. After Manav finishes his own pass — learn
Compare his finished Doc with what Claude posted (word diff): which changes he undid, what he still had to fix. Turn
every repeated pattern into a rule in RULES.md (what) and JUDGE.md (how to decide), with his own examples, and note the
numbers in "Results so far". This is where all the rules came from (videos 9–13, ઉપનિષદ - 1).

---------------------------------------------------------------------------------------------------------------

## Part D — Problems already met (so you do not repeat them)
- Saving fails with "Failed to fetch" → the Doc is not editable by link (B1), or the Apps Script threw. Nothing is changed.
- Gemini 402 RESOURCE_EXHAUSTED → no credit: use `NOGEM=1` and `proof/NOGEM.md` (stricter: one engine alone was right
  only 2–4% of the time), tell Manav, offer a Gemini pass later. Its retries also clog the pool — restart stream2 with NOGEM.
- Recorder did not move to START → it must use `movie_player.seekTo`, then wait until the video plays near START.
- 31 Oct: YouTube **muted** the recording tabs after ~30 s, so the recordings were digital silence while the video
  kept playing — and the silent pieces were still sent to Sarvam (charged by duration, ~₹20 lost). Now recorder3.js
  unmutes on every volume change and every tick, and stream2.py refuses pieces that are more than 20% silence
  ("SILENT piece, not sent"). Still: one minute after starting, decode the first parts and check they are not silent.
- An automatic safety check refuses to put the Apps Script URL or keys into a YouTube tab → use the relay (C2.0).
- Background jobs started with `&` are killed after a few minutes → always the Bash tool's run_in_background.
  Its default time limit is 30 minutes: give the collector and stream2.py `timeout` 7200000 (2 h), or they are stopped
  in the middle of a long recording (5 Nov, Maha part 3). Both resume when restarted (saved parts and finished
  `.sar.txt` pieces are skipped), so restart them between Sarvam pieces.
- yt-dlp from the cloud is blocked by YouTube's bot check; do NOT try other player clients. Use the browser (C2, C3).
- `finalvid.py` ignores candidate decisions unless they are merged into `VM/cands_out.json`.
- A judge sometimes puts a word on the wrong side of a full stop (a closing કે/છે, or તો કે / અને that open the next
  sentence: "છે તો કે." instead of "છે. તો કે"), or "fixes" a restatement → DROP it and do it in manual.json.
- `dropmantra.py` hides every spot inside a mantra item's `alt` from the judges — keep mantra `alt`s tight, and check
  the dropped spots yourself (video 39: સાક્ષી ગોપાલ તો સુંદર → અંદર was hidden that way).
- When items are changed by later steps (mantra replaced around a fix, punctuation), re-check that every ✎ item still
  finds its text; fold lost ones into the item that replaced them.
- `pauses.py` can match the wrong offset when a recording starts in the middle → pass the known offset.
- RULES.md sections were once lost in an edit — after editing the rule files, `git diff` before committing.
- **Work folders from an earlier series** (6 Nov): `v9`, `v10`, `v12`, `v13` already held October files of the શાશ્વત
  સંવાદ videos 9–13 (old `j_*_out.json`, `decisions.json`). `finalvid.py` globs `VM/j_*_out.json`, so an old judge file would
  have been applied to the new video. Before starting video NN, check that `vNN/` is new or empty; move old files to
  `vNN_oct/` (`find vNN -newermt <today>` keeps today's).
- **stream2.py lost the last piece of a recording** (6 Nov, video 6): when a recording finished, the cuts were recomputed
  from zero, and the tail (597–778 s) was merged into the first piece that was already transcribed, so it was never sent.
  Fixed: the cuts already made are kept (`KEY_cuts.json`). Check `KEY_cuts.json` → `"final": true` and the last cut = the
  recording length; if a piece is missing, run stream2 again for that key and re-fuse (carry the judges' decisions over by
  matching items on pos/end/old text — new items only need judging).
- **The Doc's hash for the post** must come from the Apps Script's own text: read it with `browser/docget.js`
  (`window.__docGet(KEY, DOC)` in the Sudhar Desk tab) and `bin/getdoc.py KEY VM/doc_orig.txt`.
- **One set of YouTube tabs for many videos** (6 Nov): `browser/recorder_fn.js` defines `__loadVid(id)` (the player's
  `loadVideoById`, which keeps the relay), `__startRec(KEY,START,END)` and `__getCaps(KEY)`. Inject it once per tab. The
  recorder reuses the tab's audio graph (`createMediaElementSource` works only once per video element).
- If Manav's computer sleeps, Chrome stops answering and the recordings stall: tell him, carry on with work that needs no
  browser (book pages, judging), and check the recorders (`window.__R`) when Chrome is back.

- **Old helper scripts write the repo** (6 Nov): `t/mkreview2.py` (October, શાશ્વત સંવાદ) rewrites `review/*.json` of the
  old videos 7–13 when run — it was run by mistake to print a list; the changes were set aside with `git stash`, nothing
  committed. Use `t/revlist.py VID` to list judge decisions with context (id, f/m/a, →[new], ⟪old⟫, S/Y/B, why).
  Always `git status` before `git add`, and add only the files of the video being posted.
- `pauses.py` found no offset for whole recordings (video 12 a/b): pass `part.wav:START:0.1` — the recorder seeks to START,
  so the offset is about 0.1 s (it was 0.1–0.14 everywhere it could be measured).

## Part E — Standing rules from Manav (summary; full text in RULES.md)
- Don't change the words the speaker said. Learn from his edits.
- Mantras: replace with the standard text (internet + the book), his layout, only the recited part.
- Sanskrit terms in the Gujarati get the visarga: ભૂઃ, ભુવઃ, સ્વઃ, જ્યોતિઃ.
- આગળે after અહીંયા/ત્યાં/જ્યાં/ક્યાં (place) → write આગળે, mark "likely".
- No paragraph break in the middle of a sentence. No quotation marks or brackets in transcripts.
- Ask before anything that cannot be undone. Doc changes only through the Apps Script with the hash check.
- Secrets (SECRET, CAP_KEY, API keys) never in chat, files in the repo, or commits.

## Part F — Done so far
| Doc | YouTube | Contents | State |
|---|---|---|---|
| શાશ્વત સંવાદ 6–13 | see index.html | | corrected, Manav checked 9–13 |
| ઉપનિષદ - 1 | sBXs4P2SE2U | અથર્વશિર ઉપનિષદ્ | corrected 29 Oct, Manav finished 30 Oct |
| ઉપનિષદ - 38-1 | fWU6DWzNHN0 | મણ્ડલબ્રાહ્મણોપનિષદ્ ૧ (89 s, the start of the introduction) | posted 4 Nov (Sarvam + book), 4 ✎ |
| ઉપનિષદ - 38-2 | dhb0yGKvDkI | મણ્ડલબ્રાહ્મણોપનિષદ્ ૨ (intro to બ્રાહ્મણ 2 ખંડ 1) | posted 4 Nov (Sarvam + book typed from the page images, no Gemini), 215 ✎ |
| ઉપનિષદ - 39 | 6AO_nSW_Rig | મણ્ડલબ્રાહ્મણોપનિષદ્ ૩ (2nd ખંડ to the end) | posted 31 Oct (Sarvam + book, no Gemini), 182 ✎; Manav listening (4 Nov) |
| ઉપનિષદ - 40 | 4Qr-R5LMUh0 | મહાવાક્યોપનિષદ્ & મૈત્રેય્યુપનિષદ્ ૧ | posted 30 Oct (Sarvam + book, no Gemini), 109 ✎; Manav FINISHED (in "total final", do not touch): of 99 applied changes he undid 1, changed 7 further |
| ઉપનિષદ - 41 | wHLe6v2nhNk | મૈત્રેય્યુપનિષદ્ ૨ & યાજ્ઞવલ્ક્યોપનિષદ્ | posted 30 Oct (Sarvam + book, no Gemini), 210 ✎; Manav FINISHED (in "total final", do not touch): of 186 applied changes he undid 4, changed 6 further; took out the empty lines around mantras (RULES 5) |
| ઉપનિષદ - 128 | Cnlxw_9qLnE | મહોપનિષદ્ ૧ | posted 5 Nov (Doc + Sarvam + book), 169 ✎ |
| ઉપનિષદ - 129 | 9pPrQQvohU0 | મહોપનિષદ્ ૨ | posted 5 Nov, 216 ✎ |
| ઉપનિષદ - 130 | c-ugolBSmdo | મહોપનિષદ્ ૩ | posted 5 Nov, 389 ✎; જોવે → જોઈએ fixed 6 Nov |
| ઉપનિષદ - 131 | 5mVrWO5YWXs | મહોપનિષદ્ ૪ | no Doc and no captions: new Doc from Sarvam alone (Part G), posted 6 Nov, 350 ✎ |
| ઉપનિષદ - 2 | Gdf-v5vCaxE | અધ્યાત્મોપનિષદ્ ૧ | posted 6 Nov (Doc + Sarvam + captions + book), 137 ✎ |
| ઉપનિષદ - 3 | 26BCmgXarnQ | અધ્યાત્મોપનિષદ્ ૨ | posted 6 Nov, 27 ✎ |
| ઉપનિષદ - 6 | dAcFljzoovI | અવધૂતોપનિષદ્ | posted 6 Nov, 100 ✎ |
| ઉપનિષદ - 7 | 8ezSSa_Fekc | આત્મપૂજોપનિષદ્ (Ganapati Atharvashirsha recited) | posted 6 Nov, 32 ✎ |
| ઉપનિષદ - 9 | n1jM69CmFzo | આત્મબોધોપનિષદ્ | posted 6 Nov, 75 ✎ |
| ઉપનિષદ - 10 | AFwySZGsBQo | આત્મોપનિષદ્ | posted 6 Nov, 131 ✎ |
| ઉપનિષદ - 12 | aN-h116qCHU | આરુણિકોપનિષદ્ | posted 6 Nov, 38 ✎ (first post without the cache key, posttext.js) |
| ઉપનિષદ - 13 | 4i2gQGDZIDQ | આશ્રમોપનિષદ્ + કઠરુદ્રોપનિષદ્ | posted 6 Nov, 49 ✎ |
| ઉપનિષદ - 14 | KDzXX0WYXhM | કુંડિકોપનિષદ્ ૧ | posted 6 Nov, 27 ✎ |
| ઉપનિષદ - 15 | qL7csyr5HEc | કુંડિકોપનિષદ્ ૨ | posted 6 Nov, 61 ✎ |
| ઉપનિષદ - 16 | QXl32jx-G2s | કૈવલ્યોપનિષદ્ ૧ | posted 6 Nov, 36 ✎ |
| ઉપનિષદ - 17 | F7TunKZ2_V8 | કૈવલ્યોપનિષદ્ ૨ | posted 6 Nov, 17 ✎ |
| ઉપનિષદ - 18 | lqmE7p2GCjw | કૌષીતકિબ્રાહ્મણોપનિષદ્ | posted 6 Nov, 143 ✎ |
| ઉપનિષદ - 19 | z3RMzwt2Cas | ક્ષુરિકોપનિષદ્ ૧ | posted 6 Nov, 78 ✎ (pauses: v19b needed a fixed offset, `:0.14:fix`) |
| ઉપનિષદ - 20 | JRrJR3wVyVA | ક્ષુરિકોપનિષદ્ ૨, guided meditation | posted 6 Nov, 37 ✎; Doc was the captions: اللہ on the silent part removed, 4th જય સચ્ચિદાનંદ added; no PUNCT pass (music: pause offsets unreliable) |
| ઉપનિષદ - 22 | p9l_rU1GgDk | જાબાલદર્શનોપનિષદ્ ૧ | posted 7 Nov (Doc + Sarvam + captions + book), 216 ✎; first direct post from the work folder (`bin/postdoc.py`) |
| ઉપનિષદ - 23 | CmC12T0YSeo | જાબાલદર્શનોપનિષદ્ ૨ (4 min) | posted 7 Nov, 8 ✎ (judged by hand) |
| ઉપનિષદ - 24 | SNFkEooCbPM | જાબાલદર્શનોપનિષદ્ ૩ (ખંડ 5–8) | posted 7 Nov, 136 ✎ (v24b pauses needed `:0.1:fix`) |
| ઉપનિષદ - 25 | nVxpSqF7rsA | જાબાલદર્શનોપનિષદ્ ૪ (ધારણા to the end) | posted 7 Nov, 16 ✎ |
| ઉપનિષદ - 26 | 0SNy2V7byT8 | જાબાલોપનિષદ્ | posted 14 Nov (Doc + Sarvam + captions + book), 122 ✎ (v26b pauses needed `:0.1:fix`; overlapping last-step rows folded into one item) |
| ઉપનિષદ - 5 | 8YbF5PwMMnU | અધ્યાત્મોપનિષદ્ ૩ | no Doc: new Doc from Sarvam + captions hint + book (PDF 24–29 typed), posted 7 Nov, 92 ✎ |
| ઉપનિષદ - 48 | Cv61CQOqbIw | શાણ્ડિલ્યોપનિષદ્ ૫ (guided meditation) | no Doc: new Doc from Sarvam (Part G), posted 7 Nov, 13 ✎; shared with manavk7 as editor |
| ઉપનિષદ - 142 | 5A0I2r8P50k | લાઙ્ગૂલોપનિષદ્ (Hanuman mantras) | no Doc: new Doc (Part G), posted 7 Nov, 90 ✎ (17 check items on mantra words); no book (not in બ્રહ્મ વિદ્યા ખંડ) |

**Playlist vs Docs (7 Nov).** The ઉપનિષદ playlist (Manav's channel, 150 videos) against the 147 "UPNISHAD -video N" Docs:
three videos have no Doc — video 5 = 8YbF5PwMMnU (અધ્યાત્મોપનિષદ્ ૩, 47 min), video 48 = Cv61CQOqbIw
(શાણ્ડિલ્યોપનિષદ્ ૫, 19 min), video 142 = 5A0I2r8P50k (લાઙ્ગૂલોપનિષદ્, 21 min). All three have Gujarati auto-captions.
The numbers 4, 8, 11, 21 are just skipped (no video). Docs moved to "total final" by 7 Nov: Atharvashir, 38-1, 38-2,
39, 40, 41, 128, 129, 130 — never write those.

## Part G. A video with no Doc and no YouTube captions (ઉપનિષદ - 131, 5–6 Nov)
YouTube said "captions unavailable", so there was no Doc. What worked:
1. Record as usual, but run the stream with `SARTS=1` (Sarvam with timestamps; same price). Add the R.map sampler in each
   tab (recording time vs video time) — for 131 the drift stayed under 0.1 s, so video time = START + recording time.
2. `t/sarts.py audio/mNNN VM key:START,…` → `VM/sarw.json` (tokens with times placed on the speech, pauses at word
   boundaries), `VM/sar.txt`, `VM/seams.txt` (check the joins between recordings). `t/sarparas.py` → `VM/doc_orig.txt`
   (paragraphs at long pauses after a sentence end, ~90 words) and the word-time file `sync/YT.tsv`.
3. `t/stageA.py` rows (fillers, words split by a stop, RULES 2 spellings, **જોવે → જોઈએ**, જાઓ → જાવ) → manualgen →
   `VM/doc.txt`; save the items as `VM/backbone_items.json` (kind auto). Run cands2 AFTER any hand edit of doc.txt
   (its positions; a one-character edit once shifted 312 candidates and corrupted the applied ones).
4. Proofreading agents (`proofreading/PROOF1.md`; `t/mkproof.py` splits, `t/proof2spec.py` turns answers into rows;
   my review goes in `VM/proof_override.json`: drop / d / alt). Then finalvid (j_kept.json = []), manualgen, mantras,
   આગળે, punctuation as in C9.
5. Book: type the pages from the images with agents (`gk/clean/BRIEF.md`, [S]/[G] lines), `t/bookalign.py` on the final
   text, `t/bookfilter.py` keeps real word differences, agents decide (`proofreading/BOOKJUDGE.md`), `t/bookapply.py`.
6. Check items from the agents' "ask" answers: `t/mkchecks.py` on the final text. revertcheck must give 0 diffs.
7. Make the Doc in the series folder with the Drive connector (account upnishad321) AND give it the same sharing as
   the other series Docs: **anyone with the link → Editor** (Manav set this for 131 on 6 Nov; manavk7 as editor also works) — the Apps Script runs as manavk7: without edit access reads work, an empty save
   "works", and every real save fails with "Failed to fetch". Brackets in a Doc now become commas automatically in backbone_m.py (7 Nov). Then post with the hash check (OLD = e3b0c44298fc1c14,
   the sha of an empty Doc).
