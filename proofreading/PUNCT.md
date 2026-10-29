# Judge: full stops by speech pauses AND meaning (Manav's punctuation)

The text is a transcript of a spoken Gujarati discourse. ⟨0.8⟩ after a word = the speaker paused 0.8 seconds there
(only pauses ≥ 0.3 s are shown). [1], [2] … mark the word boundaries you must decide. The punctuation already there is shown
just before the [n] mark (e.g. "છે.[1]⟨1.2⟩" = a full stop is there now and the speaker paused 1.2 s).

For every [n] decide what should stand right after that word: "." (sentence ends), "?" (a question ends), "," (pause inside a
sentence), or "" (nothing — the sentence runs on). Output only the [n] you would CHANGE.

What we know from Manav's own corrections (video 9, 0–1:34):
- Manav keeps most punctuation as it is. Of the full stops where the speaker does not pause, he kept 85%. Of the long pauses
  with no punctuation, he left 87% unchanged. A pause alone is NOT a reason for a full stop, and a missing pause alone is
  NOT a reason to remove one. Change only when meaning AND pause agree.
- The typical change he makes: in spoken Gujarati the speaker often adds a few words AFTER the verb and only then pauses.
  Those trailing words belong to the sentence before, so the full stop moves to the pause:
    રાહ જોશે.[ ]પછી⟨0.6⟩ ફરી ક્યારે …   →  રાહ જોશે પછી. ફરી ક્યારે …
    ડાબલી બંધ કરી દીધી.[ ]જાણે⟨1.9⟩ આવી જીવનમાં …  →  … દીધી જાણે. આવી …
    તોડી નાખશે.[ ]વ્યવહારની અંદર⟨2.2⟩ ભલે કરડીએ …  →  … નાખશે વ્યવહારની અંદર. ભલે …
    એવી રીતે બેસવાનું.[ ]આપણે⟨1.3⟩ બેસવું એટલે …  →  … બેસવાનું આપણે. બેસવું …
    ધક્કામુક્કી જ છે એક જાતની.[ ]એ બી તો⟨3.3⟩ એવી …  →  … એક જાતની એ બી તો. એવી …
  Trailing words like these: પછી, જાણે, તો, આપણે, તમે, એને, એમ, આમ, ત્યારે, ભાઈ, a place/time phrase, or a repeated
  word. Move the stop only when the trailing words clearly finish the sentence before and the next part starts fresh.
- He adds a full stop where a sentence clearly ends at a long pause (≥ 1 s) but the text runs on, and a "?" where the
  speaker clearly asks a question (શું, કેમ, ક્યાં, કોણ, કેવું, ખરું ને …) and pauses.
- He almost never adds commas: NEVER add a ",". Never turn a "," into "." unless a complete sentence clearly ends there.
- Most real changes come as a MOVE: a full stop with no pause is removed AND a full stop is added at the pause 1–4 words
  later (or earlier). Prefer moves; a lone removal or a lone addition needs very strong reasons.
- A test run showed these were WRONG (he kept the text as it was): adding "," after તો / કે; moving the stop in
  "બારી બંધ કર દો. ભાઈ કે એના જેવું"; adding "." after તોય, પાછી, રહેવાનું when the thought continued.
- Test on video 11, which Manav finished himself (29 Oct): of 31 changes, 13 were exactly his choice, 5 were at a spot where
  he put a different mark, and 13 he did not want. The unwanted ones were mostly MOVES over trailing words that can just as
  well open the next sentence — he kept the stop where it was:
    દીધો.[ ] … તો⟨4.0⟩ · નાખો.[ ] … આપણે⟨1.5⟩ · છે.[ ] … પછી⟨0.9⟩ · કરીએ.[ ] … આપણે⟨0.9⟩ · છે.[ ] … બસ,⟨4.0⟩
  The moves he did want had trailing words that only finish the sentence before: "હામે જોતા તો. પેલી …",
  "સંસાર ભાવ આખેઆખો ત્યારે! પછી …". So move a stop only when the trailing words CANNOT start the next sentence;
  if they could open it (તો …, આપણે …, પછી …, બસ …, એટલે …), leave the stop where it is.
- At long pauses with no mark he left 81% unchanged and added "." 9%, "," 7%, "?" 2%; at stops with no pause he kept 89%.
  Change only clear cases — expect roughly one change per 10–15 marks, not more.
- Where a question clearly ends at a pause and has no "?", add "?" (he did: "નારદને થોડી પૈણે?", "સ્વસ્થ છો?").
- Keep full stops between two complete sentences even without a pause (the speaker often runs sentences together).
- Do not touch Sanskrit shloka lines, mantras or bhajan lines (બ્રહ્માનંદમ પરમ સુખદમ …, સદગુરુ તમ નમામિ …) except their final stop.
- Never change words — only the punctuation mark at [n].

## Output
Write a JSON array (UTF-8, ensure_ascii=False) to the output path you are given, only for [n] you change:
{"id":"r12.2","p":"."|"?"|","|"","why":"<3-8 English words>"}
("id" = region id + "." + the number in brackets.) Reply with only the number of changes by type.
