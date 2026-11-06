"""stageA.py out_spec.json — the rule-based clean-up of a Sarvam-only transcript (ઉપનિષદ - 131, 5 Nov), as manualgen rows.
Rules come from RULES.md and from how Sarvam's words differ from the finished Docs of 8 earlier videos (t/sarstats.py):
  - fillers Sarvam writes and Manav deletes (RULES 7): હે ને / હેને / હેં ને / હેંને / હેં — "છે હે ને" -> "છે" (19 of 19)
  - a word Sarvam split across its chunk boundary with a full stop: "દ્રશ્ય. થી અલગ" -> "દ્રશ્યથી અલગ"
  - RULES 2 spellings: નિંદ્રા -> નિદ્રા, નહિ -> નહીં, અહિયાં -> અહીંયા
  - જાઓ -> જાવ (the speaker's form; Sarvam standardises it: 28 of 39 in the finished Docs) — likely
Every match becomes its own ✎ item (kind auto)."""
import sys, json
F = r'(?:હેં ને|હેંને|હે ને|હેને)'
G = '઀-૿'
rows = [
  # filler opening a sentence (after a stop): "લો. હે ને બધું" -> "લો. બધું", "નથી. હેં ને? એ" -> "નથી. એ"
  [r'([.?!]) (?:' + F + r'|હેં)[?,.]? (?=[' + G + '])', r'\1 ', 'filler હે ને deleted (RULES 7)', 'sure', 'all'],
  # tag question in the middle: "ચોપડી, હે ને? એ" -> "ચોપડી. એ"
  [r',? (?:' + F + r'|હેં)\?', '.', 'filler હે ને (tag question) deleted (RULES 7)', 'sure', 'all'],
  # filler inside / at the end of a sentence: "કુરબાન હે ને તો" -> "કુરબાન તો", "આપ્યો હેને." -> "આપ્યો."
  [r',? ' + F + r'(?=[\s.,!])', '', 'filler હે ને deleted (RULES 7)', 'sure', 'all'],
  # a word split across Sarvam's chunk boundary
  [r'(?<=[' + G + r'])[.?!] (થી|માં|માંથી|નું|નો|ની|નાં)(?=[\s,.?!])', r'\1', 'one word (Sarvam split it with a full stop)', 'sure', 'all'],
  [r'નિંદ્રા', 'નિદ્રા', 'spelling નિદ્રા (RULES 2)', 'sure', 'all'],
  [r'(?<![' + G + r'])નહિ(?![' + G + r'])', 'નહીં', 'spelling નહીં (RULES 2)', 'sure', 'all'],
  [r'(?<![' + G + r'])અહિયાં(?![' + G + r'])', 'અહીંયા', 'spelling અહીંયા (RULES 2)', 'sure', 'all'],
  [r'(?<![' + G + r'])જોવે(?![' + G + r'])', 'જોઈએ', 'Manav always writes જોઈએ, never જોવે (6 Nov, RULES 1)', 'sure', 'all'],
  [r'(?<![' + G + r'])જાઓ(?![' + G + r'])', 'જાવ', 'his spoken form જાવ (Sarvam writes જાઓ)', 'likely', 'all'],
]
if '--doc' in sys.argv:   # a Doc made from captions: only the generic rules (no Sarvam chunk splits, no જાઓ)
    rows = [r for r in rows if 'Sarvam' not in r[2]]
json.dump(rows, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('rows', len(rows))
