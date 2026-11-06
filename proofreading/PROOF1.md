# Proofread a transcript that only Sarvam heard (no Doc, no YouTube captions)

Some videos have no Doc and no YouTube captions (ઉપનિષદ - 131, મહોપનિષદ્ part 4, 5 Nov). Their transcript is made
from Sarvam alone, so there is no second recogniser to compare with. Your job: find the words Sarvam MISHEARD and
put the right word, without making the transcript "better Gujarati". Manav then listens to the whole video and
corrects the rest, so a wrong change costs him as much as a missed one: change only what you are sure is wrong.

Read /home/claude/sudhar-desk/proofreading/RULES.md first (all of it — the spoken forms in sections 1, 6, 11 and 13
matter most). The speaker is Divyangsaheb, a Gujarati spiritual teacher (Vedanta, Sadguru teaching) from Surat; he
explains the મહોપનિષદ્ (dialogues of ઋભુ and નિદાઘ, શુકદેવ and જનક, the seven ભૂમિકાઓ of knowledge, જીવન્મુક્ત,
મન, વાસના, સંકલ્પ, ચિત્ત, આત્મા, બ્રહ્મ …), reading the Gujarati translation from a book and explaining it in his own
spoken Gujarati, with English words and Surti forms.

## Input
Each line is one paragraph:  `p0123 [mm:ss] text…`  (time = where the paragraph starts in the video).
A paragraph may be followed by lines `  B: …` — sentences of the book (typed from the page images) that he reads
somewhere in that paragraph, in order.

## What to change
1. **Mishearings**: a word that makes no sense where it stands, or breaks the grammar, while a word that sounds almost
   the same fits clearly. Typical Sarvam errors in this speaker's videos: રચકણને→રજકણને, અપુષ→અપુરુષ, સફાચત→સફાચટ,
   રૂક→ઋક્, એ યુવા→એવા, પરમહૂ સના→પરમહંસના, આધ્યાત્મ. નિક→આધ્યાત્મિક (a word split with a full stop inside it),
   names and terms heard wrong: રભુ→ઋભુ, નિદાક→નિદાઘ. Use the topic, the grammar and the sentence.
2. **Sanskrit terms and names**: correct spelling with visarga where the term is standard (જ્યોતિઃ, મનઃ, નિઃસંગ,
   પ્રાતઃકાળ, જીવન્મુક્ત when he says the term). Do NOT add Sanskrit endings to Gujarati words or names (RULES 11).
3. **A word cut in two or two words run together** so that the result is not a word (આધ્યાત્મ નિક).
4. **Small words**: add a dropped છે / એ / કે / ય / જ / તો / નથી ONLY when the sentence is clearly broken without it;
   otherwise leave it (he may really have dropped it).
5. **Read sentences (B: lines)** — Manav: "always see what is written in book". Inside a sentence he is reading, a word
   Sarvam MISHEARD (wrong, garbled, or a near-sound of the book's word: સુશોભનથી→સુષુપ્તિથી, ચિન્હ માત્ર→ચિન્માત્ર,
   રબુ→ઋભુ) becomes the book's word, in the book's spelling (keep the book's brackets). But words he really said
   differently stay: his own explanations and additions inside the sentence, repeats, and normal words that fit
   (રહેલા/રહેલ, બંને/બંનેય, પર/ઉપર, કહેવામાં આવે છે/કહે છે, a different but sensible word order). Never change only
   spelling, anusvara, halant or digits for the book's sake (દ્રષ્ટા/દૃષ્ટા, હંમેશા/હંમેશાં stay as Sarvam wrote them).
   Do not add book words he skipped. Put "book" in `why` for these.

## What NOT to change (Manav undoes these)
- Spoken forms: કે છે, તું/તી/તા, રે, આયા/આયો, જાવ/થાવ, બી, કોક, ભઈ, કીધું, Surti હ (હમજો, હવાર), ને for અને,
  English words as he says them, digits. Never change tense/person/number to tidy grammar.
- But **જોવે is always written જોઈએ** (Manav 6 Nov; જુએ only where it means "sees") — change every જોવે.
- Words that are fine but "could be nicer"; synonyms; word order; repeats he means (ધીમે ધીમે, બધી બધી).
- Pure spelling (anusvara, ી/િ, ૂ/ુ, પહેલાં/પહેલા, સંન્યાસ/સન્યાસ, દૃશ્ય/દ્રશ્ય, અદ્ભુત/અદભુત).
- Punctuation and paragraphing (a separate pass does them) — except a full stop inside a split word (rule 3).
- **Handled by other steps — write nothing for these**: fillers (હેને, હે ને, હેં, હેંને, હને, a closing હા), a lone
  શું?, એને/એણે and એમને/એમણે, આગળ/આગળે, and recited mantras and shlokas (Sanskrit verses, shanti path, ૐ …).
- No quotation marks, no brackets.

## Decide each change
- **fix** — Sarvam's word is clearly wrong and you are sure what he said (it sounds alike and fits).
- **maybe** — Sarvam's word is very probably wrong and your word is the best guess (Manav will hear it; it goes in
  marked "likely").
- **ask** — something is wrong but you cannot tell what: give your best guess in `alt`; the Doc keeps Sarvam's
  words and your guess goes on Manav's list as a suggestion to listen to.
Expect a few changes per paragraph at most; many paragraphs need none.

## Output
Write a JSON array (UTF-8, ensure_ascii=False) to the output path you are given:
`{"p":"p0123","cur":"<exact text from that paragraph>","alt":"<replacement>","d":"fix|maybe|ask","why":"<3-8 English words>"}`
- `cur` is copied EXACTLY from the paragraph (same letters, spaces and punctuation), 2–8 words: the wrong word(s) plus
  a neighbour or two so that `cur` occurs only once in that paragraph. `alt` is the same stretch as it should read
  (keep the neighbours and punctuation unchanged).
- One entry per spot; never two entries that overlap.
Reply with only the counts of fix / maybe / ask.
