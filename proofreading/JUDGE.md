# Judge: pick the right words where speech recognisers disagree with the transcript (Gujarati, શાશ્વત સંવાદ)

The Doc is a transcript of a spoken Gujarati spiritual discourse (Vedanta, Sadguru teaching). Manav corrects it by
listening. We want to fix as many real mistakes as possible BEFORE he listens, without adding new mistakes.

Each line of the input file is one spot where an independent speech recogniser heard something different from the Doc:

    c123 [12:34] …words before ⟪DOC WORDS⟫ words after… || S: … || G: … || Y: …

- ⟪ ⟫ = the Doc's words at this spot (⟪⟫ empty = the recogniser heard extra word(s) here that the Doc does not have).
- S = Sarvam (good Gujarati recogniser), G = Gemini (good, sometimes "tidies" speech), both made from the real audio,
  independently. What they wrote for exactly this ⟪ ⟫ span is shown (empty = they heard nothing there).
- Y = YouTube auto-captions for the span (if shown). The Doc was made from Y and then cleaned once by an AI, so
  Y ≠ Doc means the AI changed it. Y agreeing with the Doc is NOT extra evidence.
- Spelling differences (anusvara, ી/િ, ૂ/ુ, ણ/ન, ળ/લ, શ/સ/ષ) have already been ignored; what you see is a real word difference
  (or a join/split difference).

## Decide for each line
- keep (write nothing): the Doc is right, or the difference is only how a recogniser "standardised" speech.
- fix: the Doc is wrong and you are confident what was said.
- maybe: the Doc is probably wrong, your best guess is better than the Doc, but Manav should listen.
- ask: something is wrong but you can't tell what — he must listen (give your best guess anyway).

## Evidence rules (learned from comparing recognisers with Manav's finished transcripts)
1. S and G agree with each other and differ from the Doc, and their word fits the sentence → usually fix.
   When S = G = Y, the AI cleaner changed a correct word → fix back unless the Doc's version is clearly the meaning.
   Both can still be wrong together on Sanskrit, names, and English words — use the meaning.
2. Only one of S/G differs → the Doc is usually right. Fix only if the Doc's word makes no sense and the engine's word clearly does.
3. Recognisers STANDARDISE spoken Gujarati. Manav keeps what the speaker said, so NEVER adopt these:
   કે (= says) → કહે, રે → રહે, આઈને/આયા → આવીને/આવ્યા, જાવ/થાવ → જાઓ/થાઓ, તું/તી/તા (= was) → હતું/હતી/હતા,
   Surti હ → સ (હમજો, હવાર stay), digits ↔ words (12 stays 12), ને ↔ અને, બી → પણ, કોક → કોઈ, ડાયા → ડાહ્યા,
   any change of tense/person/number that is just grammar tidying, English words translated, or the reverse.
4. Recognisers DROP repeated words. The speaker repeats a lot (બધી બધી, હવે હવે, ધીમે ધીમે, કર્યા કર્યા) and Manav keeps it.
   Do not delete a repeat because the engines lack it. Delete only an obvious broken fragment (half word + whole word).
5. Small spoken words the Doc DROPPED are the most common real mistake. Manav most often puts back:
   છે (by far), એ, કે, ય (as a separate word "એ ય", "એટલે ય" or a suffix: ત્યારેય, આખાય, પાંચેય, તેમાંય, સદાય, એનાથીય),
   છું, છો, છીએ, નથી, જ, તો, કહે, આ, નહીં, પણ, અને.
   If S or G has one of these where the Doc lacks it, and the sentence reads naturally with it → fix (both engines) or maybe (one engine).
   Write ય the way the Doc's neighbourhood writes it; when the engine joins it (એનાથીય) keep it joined, otherwise "એ ય".
6. Real mis-hearings to fix: a Doc word that makes no sense in the sentence while S/G have a word that does
   (નમે→નથી, ટવાઈ→અટવાઈ, ચારે જ→ચારેય, સંસાર→સમાજ when meaning demands). Use the topic and grammar.
7. Fillers: never insert હેને, હને, હ, હેં, હમ્મ, ઓમ-as-noise, laughter. If the Doc has a filler (હેને/હને/હેંને) and engines don't → fix (delete).
8. Joins/splits: change only for the common particles (છેને → છે ને, આતો → આ તો, પડેને → પડે ને); otherwise keep the Doc.
9. Do not touch punctuation, do not paraphrase, do not add quotation marks or brackets.
10. Lessons from a test against Manav's finished video 1 (where the judge went wrong):
   - (Superseded 29 Oct — see lesson 13.) Do not add case endings the engines "complete" inside the speaker's Gujarati.
   - તહીં stays તહીં (never ત્યાં); બેરાને stays; ભાવ stayed ભાવ though both engines heard ભાવના — when the Doc's
     word is a normal, meaningful word in that sentence, keep it even if both engines differ (write maybe at most).
   - A word both engines lack is often still spoken (બેસ બેસવાનું): delete only clear garbage.
   - ય: he writes it as a separate word after a nasal/long ending (આવતાં ય, જતાં ય, સહેજે ય, એ ય) and joined in
     common words (ત્યારેય, પાંચેય, સદાય, આખાય, તેમાંય).

## Output
Write a JSON array (UTF-8, ensure_ascii=False) to the output path you are given. Only lines you change:
{"id":"c123","d":"fix|maybe|ask","text":"<what should stand in place of ⟪ ⟫>","why":"<3-8 English words>"}
- "text" replaces exactly the ⟪ ⟫ content. Keep any punctuation that was inside ⟪ ⟫. For an empty ⟪⟫, "text" is the word(s) to insert.
  To delete the Doc words, "text" is "".
- Spell in the Doc's style (નહીં, કંઈ, અહીં, છે…).
Reply with only the counts of fix / maybe / ask.
11. Lessons from Manav's own pass over video 9 (after this same pipeline) — see also /home/claude/sudhar-desk/proofreading/RULES.md:
   - He kept 97% of fix/maybe changes. Gemini-only differences were right in only ~4% of cases, Sarvam-only ~2%:
     with one engine only, keep the Doc unless its word is clearly nonsense.
   - Never ADD a rhetorical "શું" (he removed every lone "શું?" between sentences — it is the speaker's habit). If the
     ⟪ ⟫ span is a lone "શું?" standing between two sentences and an engine lacks it → fix (delete).
   - (Superseded 29 Oct — see lesson 13: shlokas are replaced with their standard text, not written as pronounced.)
   - Keep "હમ્મ" when the Doc has it. Keep "કે છે" (never કહે છે), "ક્લોરોફોમ", "જોવે", "લેવાઈ", "તી".
   - આગળ vs આગળે: the speaker says both; change only if an engine clearly heard આગળે.
   - Ergative: if the change is between એને and એણે (or આને/આણે, તેને/તેણે, જેને/જેણે): એણે when એ is the DOER of a past
     action (એણે શું કર્યું?), એને when it means "to him / him" (મેં એને કીધું, તમે એને આપી દીધું).
12. Lessons from Manav's pass over videos 10–13 after this pipeline (RULES.md section 11):
   - He undid only ~2% of fix/maybe changes. What he undid: repeated words we put back because S, G and Y all heard them
     (હું હું, છે છે, ખબર છે ખબર) — NEVER insert a stutter repeat; a filler હા at a sentence end; one આ both engines heard.
   - What he still had to fix himself: a closing કે / કે છે (= "he says") the Doc dropped (ભાઈ કે., હાજર રહેજે કે.) —
     put it back when an engine heard it; કોક where the Doc has કોઈ and an engine heard કોક; ય (see CANDS); એમણે for a doer.
   - Delete fillers when the engines lack them: a closing હા, the English સો ("so") opening a sentence, a lone શું.
   - Upanishad / shloka lines: see lesson 13.
13. MANTRAS AND SHLOKAS (RULES.md section 5, Manav 29 Oct): a recited mantra/shloka is NOT judged word by word and NOT written as pronounced — it is replaced afterwards by its standard text from a reliable online source. For such lines write nothing (keep), unless a non-Sanskrit Gujarati word around it is wrong.
14. આગળે (Manav, 29–30 Oct; RULES.md section 1): after અહીંયા/અહીં/ત્યાં/જ્યાં/ક્યાં meaning "at that place" the speaker usually says આગળે (22 of 28 times in ઉપનિષદ - 1), but every engine writes આગળ, so the engines cannot decide it. Do not judge આગળ/આગળે here: write nothing (keep). These spots are handled separately and go on the ✎ list as "likely". Keep આગળ for "forward / next" (આગળ વધે, આગળ કહે છે).
15. THE BOOK (ઉપનિષદ - 40/41 onward): the speaker reads the Gujarati translation from the book (બ્રહ્મ વિદ્યા ખંડ), often word for word, sometimes changing or explaining it. When a line has "B:", that is the book's sentence for this stretch. Use it as evidence for names, Sanskrit terms and rare words the engines garble (શાકાયન્ય, બૃહદ્રથ, અપરોક્ષાનુભવ, તત્વજ્ઞાતા): a Doc word that is a mishearing of the book's word → fix to the book's spelling. But the speaker's own words win: where S/G clearly heard something else (his own phrasing, કરું છું for the book's કરીએ છીએ), keep what he said, and never copy book words he did not say.
