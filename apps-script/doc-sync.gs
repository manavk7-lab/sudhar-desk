/**
 * Sudhar Desk — Google Doc sync + cross-device position (v2)
 *
 * What it does
 *   GET  ?token&docId                 → { text }            read the Doc
 *   POST {token, docId, fullText}     → { ok }              write the Doc (JSON or hidden-form)
 *   GET  ?token&action=getpos&key     → { pos }             where you were (video time + text spot)
 *   GET  ?token&action=setpos&key&data→ { ok, pos }         save where you are, for your other devices
 *
 * UPDATE (keeps the same /exec URL):
 * 1. script.google.com → open the "sudhar-desk doc sync" project.
 * 2. Replace all code with this file, then put YOUR existing SECRET back on the line below.
 * 3. Deploy → Manage deployments → ✏️ edit → Version: "New version" → Deploy.
 */

const SECRET = 'PASTE-YOUR-EXISTING-SECRET-HERE';

function doPost(e) {
  var req = {};
  try {
    if (e.postData && e.postData.contents && e.postData.contents.charAt(0) === '{') {
      req = JSON.parse(e.postData.contents);          // fetch() JSON body
    } else {
      req = e.parameter || {};                        // hidden-form fallback
    }
  } catch (err) {
    req = e.parameter || {};
  }

  if (req.token !== SECRET) return out({ error: 'auth' });
  if (!req.docId) return out({ error: 'no-docId' });

  var doc = DocumentApp.openById(req.docId);
  var body = doc.getBody();

  if (req.fullText !== undefined && req.fullText !== null) {
    body.setText(String(req.fullText));
    doc.saveAndClose();
    return out({ ok: true, mode: 'full' });
  }

  var applied = 0;
  var reps = req.replacements || [];
  for (var i = 0; i < reps.length; i++) {
    var r = reps[i];
    if (!r.from || r.from === r.to) continue;
    var pat = escapeRegex_(r.from);
    if (body.findText(pat)) { body.replaceText(pat, r.to); applied++; }
  }
  doc.saveAndClose();
  return out({ ok: true, applied: applied });
}

function doGet(e) {
  var p = e.parameter || {};
  if (p.token !== SECRET) return out({ error: 'auth' });

  // ---- cross-device position ----
  if (p.action === 'getpos' || p.action === 'setpos') {
    if (!p.key || !/^[\w-]{6,40}$/.test(p.key)) return out({ error: 'bad-key' });
    var props = PropertiesService.getScriptProperties();
    var name = 'pos_' + p.key;

    if (p.action === 'getpos') {
      var v = props.getProperty(name);
      return out({ pos: v ? JSON.parse(v) : null });
    }

    var d;
    try { d = JSON.parse(p.data || ''); } catch (err) { return out({ error: 'bad-json' }); }
    var lock = LockService.getScriptLock();
    lock.waitLock(5000);
    try {
      var old = props.getProperty(name);
      if (old) {
        var o = JSON.parse(old);
        if (o.t && d.t && o.t > d.t) return out({ ok: true, stale: true, pos: o });  // a newer one already won
      }
      props.setProperty(name, JSON.stringify(d));
    } finally {
      lock.releaseLock();
    }
    return out({ ok: true, pos: d });
  }

  // ---- read the Doc ----
  if (!p.docId) return out({ error: 'no-docId' });
  var doc = DocumentApp.openById(p.docId);
  return out({ text: doc.getBody().getText() });
}

function escapeRegex_(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function out(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
