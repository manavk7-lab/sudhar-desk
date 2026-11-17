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
   **The book's brackets stay** (Manav, 16 Nov, ઉપનિષદ - 34: "you used to forget ( ) while checking from books";
   RULES.md since 1 Nov): where he reads a sentence and the book prints a bracket, write the SAME bracket around the
   same words — book "અચ્યુતરૂપી હંસ (ચેતન જીવ) હંમેશાં રહેતો" → "હંસ (ચેતન જીવ) હંમેશા રહેતો" (not "હંસ, ચેતન જીવ," and
   not "હંસ ચેતન જીવ"); book "તેઓ (બ્રહ્મ)જ બધાનો" → "તેઓ (બ્રહ્મ) જ બધાનો"; book "એષણાત્રય (પુત્રૈષણા, વિત્તૈષણા અને
   લોકૈષણા)" → the same with brackets. A comma that stands where the book has "(" or ")" goes. Only the book's own
   brackets: his spoken asides get no brackets. Never add a comma the book does not have inside a read sentence.
4. **Book spellings of ordinary words** inside the read sentence when the Doc's spelling is just a different spelling of
   the same word (સિદ્ધિયો/સિદ્ધિઓ both fine — leave; but a misspelling like વિષ્ટા for વિષ્ઠા → book).

5. **Question tags get "?"** (Manav, 15 Nov, ઉપનિષદ - 30: "પછી બરાબર?"): when he ends with a tag asking the
   listeners — બરાબર, ખરું ને, સમજાયું, ક્લિયર, ને, હેં — and the transcript has "." or "," or nothing, write "?".
   ("બરાબર છે." is a statement: leave it.) Do this in the whole text, not only the read passages.
6. **Whole words the Doc misheard while he reads**: book "અન્ય ભ્રમમાંથી મુક્તિ ઇચ્છે છે" — the Doc had "અન્ય બ્રહ્માદિ
   મુક્તિ"; book "એ (જીવ) ક્યારેક" → "એ જીવ ક્યારેક". When the transcript's word makes no sense and the book's word sounds
   alike, write the book's word.

## What NOT to change
- His explanations and additions ("તીવ્રત એટલે સત, રજ અને તમસ", "એટલે કે …", "સમજાયું?") — they are his words. Inside an
  explanation, still spell a repeated book term the book's way (the second "તીવ્રત" → "ત્રિવૃત્ત" too).
- A DIFFERENT everyday word he really said instead of the book's (book તથા, he says અને; book કેમકે, he says કારણ કે):
  keep his word. Check sar.txt: if Sarvam heard the book's word, it is a mishearing → book; if Sarvam heard his word, keep.
- Book words he skipped: do NOT insert them. List them as a note ("listen: the book has બ્રહ્મા here") with `conf: "listen"`.
- Doc conventions that stay: તત્વ (not તત્ત્વ), સન્યાસ / સન્યાસી, મહીં for મય, જોઈએ, આગળે; no brackets for his own spoken asides (the book's brackets stay, rule 3), no quotes, no apostrophes.
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
