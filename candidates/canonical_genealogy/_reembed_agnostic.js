// Re-embed the canonical agnostic_framework spec/overlay/narration JSON into viewer_v3.html.
// The viewer carries inline <script type="application/json"> copies of the canonical files for
// offline rendering. They are GENERATED from the canonical files — never hand-edit the embed.
// Substrate is deliberately NOT regenerated here: its embed is a SLIM/COMPILED form (short keys,
// no `notes` field), produced by the substrate compiler, not a verbatim copy of the .jsonl.
// Usage: node _reembed_agnostic.js   (idempotent; rewrites only the 3 agnostic data blocks)
const fs = require('fs');
const dir = __dirname;
const VIEWER = dir + '/viewer_v3.html';

// ASCII-safe, </script>-safe JSON for inline embedding.
function embedJSON(obj) {
  let s = JSON.stringify(obj);
  // escape every non-ASCII char to \uXXXX (matches the existing embed style; keeps the HTML ASCII-safe)
  s = s.replace(/[-￿]/g, function (c) {
    return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
  });
  // neutralize any "</" so a string value can never prematurely close the <script> block
  s = s.replace(/<\//g, '<\\/');
  return s;
}

function replaceBlock(html, id, jsonText) {
  const idTok = 'id="' + id + '"';
  const i = html.indexOf(idTok);
  if (i < 0) throw new Error('block not found: ' + id);
  const tagEnd = html.indexOf('>', i);
  const close = html.indexOf('</' + 'script>', tagEnd);
  if (tagEnd < 0 || close < 0) throw new Error('malformed block: ' + id);
  return html.slice(0, tagEnd + 1) + jsonText + html.slice(close);
}

let html = fs.readFileSync(VIEWER, 'utf8');
const spec = JSON.parse(fs.readFileSync(dir + '/specimens/agnostic_framework.json', 'utf8'));
const ovl = JSON.parse(fs.readFileSync(dir + '/overlays/agnostic_framework.overlay.json', 'utf8'));
const narr = JSON.parse(fs.readFileSync(dir + '/narration/agnostic_framework.narration.json', 'utf8'));

html = replaceBlock(html, 'spec-agnostic_framework', embedJSON(spec));
html = replaceBlock(html, 'ovr-agnostic_framework', embedJSON(ovl));
html = replaceBlock(html, 'narr-agnostic_framework', embedJSON(narr));

fs.writeFileSync(VIEWER, html, 'utf8');
console.log('re-embedded spec/overlay/narration from canonical files.');
