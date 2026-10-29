# Judge: narrow lessons from Manav's own corrections (videos 9–13)

Read /home/claude/sudhar-desk/proofreading/RULES.md first (sections 3, 4, 5 and 11 are the ones that matter here).
Each input line is one spot:  id KIND [time] …context ⟪DOC WORD⟫ context… || S: what Sarvam heard || G: what Gemini heard

KIND tells you what to decide:
- ERG — the Doc has એને / આને / તેને / જેને (or the plural એમને / તેમને / જેમને / આમને). Write એણે / આણે / તેણે / જેણે
  (એમણે / તેમણે / જેમણે / આમણે) ONLY when that person is the DOER of a past
  action in that clause (એણે શું કર્યું? / આણે મને જે જે ના કર્યા / જેણે પરમપદનો સાક્ષાત્કાર કર્યો) and nobody else in the clause is the doer.
  Keep એને when it means "to him / him / for him" (મેં એને કીધું, તમે એને પ્રેમ કરો, એને સંતોષ છે, એને કંઈ થતું નથી,
  એને ટ્રેસ પાસિંગ કહેવામાં આવે = "that is called"). Most spots are correct as they are — change only the clear doer cases.
  If an engine wrote એણે/આણે that is extra evidence.
- SHU — a lone "શું?" or "શું" at the start of a sentence or after a comma. This is the speaker's verbal habit; Manav deleted
  every lone one in videos 9–13, with or without "?": "…તોડી નાખશે. શું? ક્રોધ, માન…", "કાઢ્યું કે, શું? ઘસી ઘસીને",
  "બેસવાનું. શું આનંદ કરવાનો", "ગમે તેમ કરીને, શું જોગવાઈ કરવી પડશે". Decide "fix" with text "" to delete it, UNLESS it
  is part of a real question (the sentence asks something and ends with "?": "શું કીધું?", "શું જનોઈ ધારણ કરી છે?",
  "એટલે શું?", "તો શું થયું?") — then keep. When "શું" starts a statement (no question), delete it.
- SKT — (changed 29 Oct) do NOT add endings as pronounced any more. Whole mantras/shlokas are replaced with their standard
  text from the internet in a separate step (RULES.md section 5). Write nothing for SKT lines.

- YA — a lone "એ" inside a sentence. Manav corrected several of these to "ય" (= also / even), which the recognisers also
  write as એ:  તમારાથી ⟪એ⟫ બહુ ભૂલો થઈ છે → ય · તમારા શરીરમાંથી ⟪એ⟫ કશું વ્યય નહીં થાય → ય ·
  સંભળાવનારો ⟪એ⟫ અંદર → ય · સમજણનું થોડું ઘણું ⟪એ⟫ અજવાળું → ય.
  Most lone એ are correct (he / she / it / that / those: "એ બાજુ", "એ લોકો", "મતલબ એ થયો", "તરત એ બાજુ", "છે એ હંમેશા").
  Write "ય" ONLY when એ cannot be a pronoun or "that" in the clause and "also / even" is clearly the meaning (fix), or very
  likely (maybe). An engine writing ય / યે / joined -ય is extra evidence. Otherwise keep. Expect only a handful per video.

## Output
Write a JSON array (UTF-8, ensure_ascii=False) to the output path you are given, ONLY for spots you change:
{"id":"e12","d":"fix|maybe|ask","text":"<what replaces ⟪ ⟫>","why":"<3-8 English words>"}
For SHU deletions "text" is "" (the "?" after it goes with it automatically — do not include it).
Reply with only the counts of fix / maybe / ask.
