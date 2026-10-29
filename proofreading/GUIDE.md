# Proofreading guide — Manav's Gujarati discourse transcripts (શાશ્વત સંવાદ)

The text is a transcript of a spoken Gujarati spiritual discourse (Vedanta / Upanishad / Sadguru teaching:
બ્રહ્મ, આત્મા, તત્વમસિ, સચ્ચિદાનંદ, સદ્ગુરુ, ચિદાકાશ, પરબ્રહ્મ, અહં બ્રહ્માસ્મિ …). It came from YouTube
auto-captions (ASR) and may already have been partly cleaned by an AI. Your job is to find the remaining
mistakes the way Manav fixes them. He keeps the speaker's words — this is NOT an edit for style.

## What Manav changes (learned from 6 videos he finished by hand)
1. ASR mis-hearings → the word actually meant. Examples he made:
   ખાદા→ખાધા, હારો→સારો, હાચી→સાચી, પેરો→પહેરો, પડોજનમાં→પળોજણમાં, જીજી વિસા→જીજીવિષા, પછશે→પચશે,
   ચુતતો→ચ્યુત, ભૂસાઈ→ભૂંસાઈ, પાપડે ભાગે→પાપડેય ભાંગે, બ્રહ્મકુમારી→બ્રહ્મખુમારી, ડાયો જીનસ→ડાયોજીનસ,
   તત્વમમાંસી→તત્વમસિ, તત્વ મજીમાં→તત્વમસિમાં, લંગનમ→લંઘનમ્, આરોગ્ય લીધું→આરોગી લીધું, જળ→જડ (matter).
   The surrounding sense, the topic, and Gujarati grammar tell you the right word.
2. A few spellings he ALWAYS fixes (do these as "sure"):
   નહી→નહીં, કઈ/કાઈ→કંઈ, કઈક→કંઈક, અહી→અહીં, અહિયા→અહીંયા, અહીથી→અહીંથી, છતા→છતાં, છતાય→છતાંય,
   ક્યાય→ક્યાંય, નિરાતે→નિરાંતે, ઉભો/ઉભા→ઊભો/ઊભા, બેહી→બેસી, બેહાડી→બેસાડી, હારું/હારો/હાચી→સારું/સારો/સાચી,
   પછ→પછી, તમ→તમે (cut-off word), માગુું→માગું (doubled vowel sign = typo).
3. KEEP the speaker's spoken forms — he leaves these as spoken, do NOT change them:
   "કે છે" (= says) stays કે, તું (= was) stays, તી/તા stay, રે (= stay) stays, આયા/આયો stay, જાવ/થાવ stay,
   બી, કોક, ભઈ, તઈ, દાડો, જરાક, સદગુરુ, પહેલા, ઉડી, જોતા/કરતા/લેતા, હે (as "O …"), ના (for નહીં),
   the Surti "હ" for "સ" (હવાર, હમજો, હંભળાય — keep), numbers exactly as written (25, 12 — do not convert digits),
   Sanskrit words inside his Gujarati sentences as he says them (સ્થિત પ્રજ્ઞ, ક્લેશાત). BUT a recited mantra or shloka
   is replaced with its standard text taken from the internet (RULES.md section 5, Manav's rule of 29 Oct 2026).
   "ત્યાં આગળે" / "અહીં આગળે" — the speaker says આગળે; never shorten it to આગળ (Manav corrects this).
   Rule of thumb: if a Gujarati listener would hear the same sounds, keep it. Only fix what is a DIFFERENT
   word from what was said, or a cut-off / garbled word.
4. Joined words split (and the reverse): છેને→છે ને, આતો→આ તો, આજ→આ જ (when "this very"), પડેને→પડે ને,
   જાયને→જાય ને; ચિત્તધાર→ચિત્ત ધાર; and pieces of one word joined back (સર્વોપરિ સ્થિતિ, જીજીવિષા).
5. Words the ASR DROPPED (always "likely" or "unsure", never "sure") — he puts them back. By far the most common is a missing "છે" (also છું, છીએ, છો,
   નથી, એ, ય, જ, તો, કહે) at the end of a clause:  "શું થઈ રહ્યું ⟨છે⟩", "બહુ સરસ દેખાય ⟨છે⟩",
   "હું આત્મા જ ⟨છું⟩". Add one only when the sentence is clearly incomplete without it.
6. Words to DELETE: the filler/caption noise હેને, હને, હેં, હેંને, હ (and હે only when it is a filler, not "O …"), and laughter tags like [હાસ્ય] / હાસ્ય
   when it is a tag, not the word. Also an accidental stutter repeat of a small word ("કે કે", "તું તું",
   "એટલે એટલે") — but NOT deliberate repetition for emphasis ("ધીમે ધીમે", "આમ આમ", "લેતાં લેતાં").

## What Manav does NOT want
- No paraphrase, no "better Gujarati", no reordering, no added explanations, no quotation marks,
  no brackets. Do not change a word that is plausible as spoken.
- Do not "standardise" dialect that he keeps (બી, કોક, ને for અને is often fine).
- Do not touch punctuation unless a sentence break is clearly wrong (punctuation is not your job here).

## Output
Return ONLY a JSON array. One object per edit:
{"find": "<exact text copied from the input, 3–8 words, unique, containing the word(s) to change>",
 "replace": "<the same text with only the fix applied>",
 "conf": "sure" | "likely" | "unsure",
 "why": "<few English words>"}
- "sure" = any careful Gujarati reader would agree (spelling rule, obvious mis-hearing with only one sensible reading, filler deletion).
- "likely" = probably right but the audio might say otherwise.
- "unsure" = something is wrong here but you can't be sure what was said — Manav should listen.
  For unsure, still give your best guess in "replace".
- "find" must be copied character-for-character (including punctuation) from the input text.
- Keep each edit small: change only the wrong word(s).

## Learned from Manav's own pass over video 7 (after the AI pass) — 215 more fixes
- Most common: he PUTS BACK small spoken words the ASR dropped: છે (often), એ, કે, ય (as in "એનથી ય", "સહેજેય", "ત્યારેય", "આખાય"), છો, છું, જ, નથી, તો, આમ, પણ.
- He writes what is spoken, including particles: "ય" endings, તહીં (not ત્યાં when spoken તહીં), આગળે, કોક, જોવે, એણે (ergative), કહેશે (future) vs કહે છે — follow the audio.
- He fixes real mis-hearings: લાલ→લાવે, જ્ઞાન→ગ્લાનિ, જીવવાશે→જીરવાશે, ન્યુટર→નાન્યેતર, વયા→વહ્યા, આશરુ→અશ્રુ, સંસાર→સમાજ.
- He deletes stutters/repeats the speaker did not mean (સૂર્યોદય થયો સૂર્ય સૂર્યોદય → one).
