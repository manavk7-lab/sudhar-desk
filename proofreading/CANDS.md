# Judge: three narrow lessons from Manav's own corrections (video 9)

Read /home/claude/sudhar-desk/proofreading/RULES.md first (sections 3, 4 and 5 are the ones that matter here).
Each input line is one spot:  id KIND [time] …context ⟪DOC WORD⟫ context… || S: what Sarvam heard || G: what Gemini heard

KIND tells you what to decide:
- ERG — the Doc has એને / આને / તેને / જેને. Write એણે / આણે / તેણે / જેણે ONLY when that person is the DOER of a past
  action in that clause (એણે શું કર્યું? / આણે મને જે જે ના કર્યા / જેણે પરમપદનો સાક્ષાત્કાર કર્યો) and nobody else in the clause is the doer.
  Keep એને when it means "to him / him / for him" (મેં એને કીધું, તમે એને પ્રેમ કરો, એને સંતોષ છે, એને કંઈ થતું નથી,
  એને ટ્રેસ પાસિંગ કહેવામાં આવે = "that is called"). Most spots are correct as they are — change only the clear doer cases.
  If an engine wrote એણે/આણે that is extra evidence.
- SHU — a lone "શું?" standing as its own sentence between two sentences. This is the speaker's verbal habit; Manav deleted
  every one of these in video 9 (8 of 8). Decide "fix" with text "" to delete it, UNLESS it is a real question that the next
  words answer or that belongs to the sentence (e.g. "એટલે શું? …", "તો શું થયું?") — then keep.
- SKT — an engine heard a Sanskrit ending (-મ / -મ્) on a word in a shloka or Sanskrit phrase. Manav writes the ending as
  pronounced (સદગુરુમ, ગુરુમ, મૂર્તિમ, શ્રીગુરુમ, ભવેત). Add it (written મ, no halant) when the word is in a Sanskrit phrase and
  the ending is plausible as spoken: fix if both engines heard it, maybe if one. Keep for ordinary Gujarati.

## Output
Write a JSON array (UTF-8, ensure_ascii=False) to the output path you are given, ONLY for spots you change:
{"id":"e12","d":"fix|maybe|ask","text":"<what replaces ⟪ ⟫>","why":"<3-8 English words>"}
For SHU deletions "text" is "" (the "?" after it goes with it automatically — do not include it).
Reply with only the counts of fix / maybe / ask.
