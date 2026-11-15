# BOOKCHECK — every word of the read passages against the book

Manav (15 Nov, ઉપનિષદ - 29): the Doc had "મહીપુષા, રમા, તીવ્રત" where the book prints "મહી, પૂષા, રમા, બ્રહ્મા,
ત્રિવૃત્ત (સત્, રજ્, તમ્)". "Trivrut is not written as it is there in the book … so many times in the book is what is
written, and when we see, it is not written like this. So kindly check each and every word, so I have to correct less."

The speaker (Divyangsaheb) reads the book's Gujarati translation aloud, sentence by sentence, and explains in between.
Your job: find every place where he is READING and the transcript does not spell the book's words the way the book does.

## Inputs
- `final.txt` — the transcript (what will go into Manav's Doc).
- `book_gu.txt` — the book's Gujarati text (OCR: a few letters may be misread; ignore OCR noise like `|`, `1૨।`, stray
  Devanagari digits). `book.txt` also has the Sanskrit verses in Gujarati script.
- `sar.txt` — what the Sarvam recogniser heard (a second opinion on what he actually said).

## What to change (write the BOOK's form)
1. **The same word written or heard differently**: ત્રિવૃત્ત (Doc તીવ્રત), ગાર્હપત્ય (Doc ગાહપત્ય), પૂષા (Doc પુષા),
   ઋત્વિજ (Doc ઋત્વીજ), સમભાવ (Doc સંભાવ), આપ્તબંધુ (Doc આપ તો બંધુ). Names of gods, sages, Upanishads, Sanskrit terms,
   numbers, technical words: always the book's spelling — even when he pronounces it a little differently.
2. **Words run together or split differently**: "મહીપુષા" → "મહી, પૂષા" (the book lists them separately);
   "નિર્વિકલ્પ" written as one word when the book does.
3. **Book punctuation inside the read sentence**: commas between list items, ? and ! as in the book.
   **Too many commas** (Manav, 15 Nov, twice): where the book prints a BRACKET, the transcript must NOT have a comma.
   Book "તેઓ (જાગૃતિ, સ્વપ્ન તેમજ સુષુપ્તિ) ત્રણેય અવસ્થાઓથી પર તુરીયાવસ્થા (ચોથી અવસ્થા) સ્વરૂપ" → write
   "તેઓ જાગૃતિ, સ્વપ્ન, સુષુપ્તિ ત્રણેય અવસ્થાઓથી પર તુરીયાવસ્થા ચોથી અવસ્થા સ્વરૂપ" (the commas INSIDE the bracket
   stay; the ones standing for "(" and ")" go). Book "એ જ (બ્રહ્મ પ્રાપ્તિનો) માર્ગ" → "એ જ બ્રહ્મ પ્રાપ્તિનો માર્ગ";
   book "તેઓ (બ્રહ્મ)જ બધાનો" → "તેઓ બ્રહ્મ જ બધાનો"; book "શિખા (ચોટલી) છે" → "શિખા ચોટલી છે". So: REMOVE every comma
   in final.txt that stands exactly where the book has "(" or ")" in the passage he is reading. Never add a comma the
   book does not have inside a read sentence.
4. **Book spellings of ordinary words** inside the read sentence when the Doc's spelling is just a different spelling of
   the same word (સિદ્ધિયો/સિદ્ધિઓ both fine — leave; but a misspelling like વિષ્ટા for વિષ્ઠા → book).

## What NOT to change
- His explanations and additions ("તીવ્રત એટલે સત, રજ અને તમસ", "એટલે કે …", "સમજાયું?") — they are his words. Inside an
  explanation, still spell a repeated book term the book's way (the second "તીવ્રત" → "ત્રિવૃત્ત" too).
- A DIFFERENT everyday word he really said instead of the book's (book તથા, he says અને; book કેમકે, he says કારણ કે):
  keep his word. Check sar.txt: if Sarvam heard the book's word, it is a mishearing → book; if Sarvam heard his word, keep.
- Book words he skipped: do NOT insert them. List them as a note ("listen: the book has બ્રહ્મા here") with `conf: "listen"`.
- Doc conventions that stay: તત્વ (not તત્ત્વ), સન્યાસ / સન્યાસી, મહીં for મય, જોઈએ, આગળે; no brackets, no quotes, no apostrophes.
- Mantras already in standard Sanskrit layout (lines ending । / ॥) — leave them.

## How to work
Go through final.txt paragraph by paragraph. For each paragraph, find the book passage it reads (search book_gu.txt for
2–3 distinctive words). Compare word by word. Use sar.txt for doubtful places.

## Output
A JSON array, one row per change: `[old, new, why, conf]`
- `old`: an exact substring of final.txt (copy it character for character) — the changed word(s) WITH one or two
  neighbouring words so that `old` occurs EXACTLY ONCE in final.txt. Check uniqueness yourself (grep -c / python count).
- `new`: the same substring with only the change made.
- `why`: short: "book: ત્રિવૃત્ત (Sarvam: તિવ્રત)".
- `conf`: "sure" (clear book word), "likely", or "listen" (a note only; old == new, nothing changes).
Do not include rows where nothing differs. Never change text outside the read passages except a repeated book term.
