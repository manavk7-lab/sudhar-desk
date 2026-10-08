# Sudhar Desk

Correct Gujarati transcripts while the video plays. YouTube player + your Google Doc on one screen; every edit saves straight into the Doc.

Live: https://manavk7-lab.github.io/sudhar-desk/

## Keyboard (works while typing)
| Key | Action |
|---|---|
| `Esc` | play / pause (in full screen: hold Esc to leave full screen) |
| `Tab` | back 5 s |
| `Shift`+`Tab` | forward 5 s |
| `⌘/Ctrl`+`S` | save to Doc now |
| `⌘/Ctrl`+`.` | speed 1× → 0.75× → 1.25× → 1.5× |

On-screen buttons no longer take the cursor out of the text.

## Same place on every device
Pause on the Mac, pick up the phone: it opens at the same video time, the same words at the top and the same cursor.
An idle device also follows the active one every ~15 s and whenever you switch back to it.
The place is stored as a character position, so it survives different screen widths and font sizes.

If the Doc was edited on another device since this screen loaded it, saving stops and asks
(load the Doc's version / keep this screen's text) instead of silently overwriting.

Needs `apps-script/doc-sync.gs` (v2) deployed. With the old script the app still works; cross-device sync just shows "⇅ off".

## Layout and install
- Wide window → video on the left, transcript on the right (⇆ / ☰ toggles). Narrow → video on top.
- ⛶ full screen.
- Installable: Chrome/Edge on Mac or Windows → install icon in the address bar (or ⤓ Install app on the home screen).
  Android Chrome → Install app. iPad/iPhone Safari → Share → Add to Home Screen.

## Apps Script update (one time)
1. script.google.com → project "sudhar-desk doc sync".
2. Replace all code with `apps-script/doc-sync.gs`, put your existing SECRET back on the `const SECRET` line.
3. Deploy → Manage deployments → ✏️ → Version: New version → Deploy (same /exec URL).

## Follow-along (spoken word lights up)
Videos that have `sync/<videoId>.tsv` get it automatically: as the video plays, the sentence
being spoken is shaded and the word is highlighted in the transcript.
- The times come from YouTube's auto-captions (word level) and are matched to the transcript
  in the browser, so corrections never break it — after typing pauses it re-matches (~20 ms).
- **◎ follow** scrolls the text with the speech; any scroll, click or typing pauses that for 5 s.
  Pressing play always brings the spoken words into view if they are off-screen.
- **✦** chooses word+sentence / sentence / word / off.
- `⌘/Ctrl+J` go to the spoken words · `⌘/Ctrl+Enter` play from the cursor's word · `⌥/Alt+click` play from a word.
- Phone: the ◎ button floats next to ↺5.

Currently: `n7WAOZ91KMc` (શાશ્વત સંવાદ - 6).
