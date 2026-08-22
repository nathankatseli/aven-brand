"""One-shot restructure of the brand book around the Avenue mark family (Aug 2026 direction change).
Run after src/avenue.py is final:  python src/patch_avenue.py
"""
import pathlib, re, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import avenue  # noqa: E402

p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")


def rep(a, b, count=1):
    global s
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b, count)


WEARS = {
    20: "signage, website hero, welcome pack cover, letterhead.",
    21: "everything - the all-rounder; business card, email signature, boards.",
    22: "social tiles, the fee brochure cover, anywhere it sits on cloud or paper.",
    23: "signage at distance, vehicle decal, one-colour print, embroidery.",
    24: "\"For Lease\" boards, letterbox drops, tenant welcome material.",
    25: "welcome cards, seasonal social, the plant tag, the booklet cover.",
    26: "South West regional material, rural and lifestyle listings.",
    27: "dark-mode website, the card back, evening social posts.",
    28: "stamps, embroidery, very small print, dark backgrounds.",
    29: "social avatar, window decal, wax-seal and stamp moments.",
    30: "quiet uses - document footer, lapel pin, email footer.",
    31: "monogram uses - cufflinks, pin, watermark, document corner.",
    32: "favicon, phone contact, app icon at small sizes, embroidery.",
    33: "app icon, social avatar, Google Business Profile, favicon.",
}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

marks = sorted(avenue.MARKS, key=lambda m: m[0])
assert len(marks) == 14, len(marks)

# ---- chapter 07 cards ----
cards = []
opts_p, opts_s = [], []
for i, (num, slug, label, fn) in enumerate(marks):
    name, _, desc = label.partition(" - ")
    letter = LETTERS[i]
    fav = ' fav' if num == 21 else ''
    tag = f'{letter} · <span class="favnote">Cara\'s brief, drawn straight</span>' if num == 20 else (f'{letter} · <span class="favnote">small cut</span>' if num == 31 else letter)
    cards.append(f'      <div class="card{fav}"><div class="art"><img src="kit/marks/{num}-{slug}.svg" alt="{H.escape(name)} mark"></div><div class="body"><div class="tag">{tag}</div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc[0].upper() + desc[1:])}.</p><p><b>Wears well on:</b> {WEARS[num]}</p></div></div>')
    short = name.replace("The ", "")
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{slug}" data-label="{letter} · {H.escape(name)}"> {letter} · {H.escape(short)}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{slug}" data-label="{H.escape(short)}"> {H.escape(short)}</label>')

RESERVE = [
    ("01-doorway", "doorway", "The Doorway", "Round-one favourite - the arched door with the Southern Cross as its fanlight."),
    ("02-signature", "signature", "The Signature", "No symbol; the name is the mark, one raindrop through the rule."),
    ("12-full-circle", "full-circle", "Full Circle", "Ring broken at the top, the drop falling into the gap - Cara's circular brief, answered literally."),
]
res_cards = "".join(f'      <div class="card small"><div class="art"><img src="kit/marks/{f}.svg" alt="{n} mark"></div><div class="body"><div class="tag">{LETTERS[14 + i]} · reserve</div><div class="nm serif">{n}</div><p>{d}</p></div></div>\n' for i, (f, v, n, d) in enumerate(RESERVE))
for i, (f, v, n, d) in enumerate(RESERVE):
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{v}" data-label="{LETTERS[14 + i]} · {n}"> {LETTERS[14 + i]} · {n.replace("The ", "")}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{v}" data-label="{n.replace("The ", "")}"> {n.replace("The ", "")}</label>')

start = s.index('<section class="chapter" id="c07-mark">')
end = s.index('<!-- ===================== 08')
new07 = f'''<section class="chapter" id="c07-mark">
  <div class="part reveal"><div class="big-num">07</div><div class="p-num">Chapter 07</div><h2 class="serif">The mark</h2>
  <p>One idea, fourteen drawings. Cara's brief this week was precise: trees either side, a house in the middle, a road running down to it — the avenue of the name, drawn simply and tastefully. So the earlier marks step back (three stay in reserve at the end) and this chapter becomes one family. Every drawing shares the grammar — fine pine line, a sage road that leads the eye to the house, one rain-blue evening star, the wordmark beneath — and they differ only in how much they say, from a full avenue in perspective to three strokes that survive as a favicon. One primary to pick; up to two secondaries to keep for campaigns.</p></div>
  <section class="option reveal">
    <blockquote class="cara-q">Like a tree-lined avenue, every property journey should be guided with confidence, clarity and lasting value.<cite>Cara — the line the mark is drawn from</cite></blockquote>
    <div class="quad">
{chr(10).join(cards)}
    </div>
    <div class="eyebrow" style="margin-top:var(--s6)">Held in reserve — the earlier direction</div>
    <div class="quad three">
{res_cards}    </div>
    <div class="checks">
      <div class="check"><div class="k">Small-format rule</div><div class="v">Fine lines vanish at favicon size. Whichever avenue wins, its small cut is <b>The Lane</b> (and <b>The Tile</b> for app icons) — heavy road into the house, two solid trees — drawn with the vector suite so the brand survives at sixteen pixels and in embroidery.</div></div>
      <div class="check"><div class="k">How to choose</div><div class="v">Imagine it on a "For Lease" board at forty metres, embroidered on a shirt, and as a dot in a phone contact. The right one works in all three. A secondary mark can be the one you love that fails one of the tests.</div></div>
    </div>
    <fieldset class="call" data-id="mark-primary" data-label="Primary mark">
      <legend>Your call — primary</legend>
      <div class="q">Which drawing is the brand?</div>
      <div class="opts">
{chr(10).join(opts_p)}
      </div>
      <textarea data-note placeholder="What to tweak on the winner?"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <fieldset class="call" data-id="mark-secondary" data-label="Secondary marks (campaign use)">
      <legend>Your call — secondaries (up to two)</legend>
      <div class="q">Which drawings do we keep alive for campaigns, social and welcome material?</div>
      <div class="opts">
{chr(10).join(opts_s)}
      </div>
      <textarea data-note placeholder="Note"></textarea>
      <p class="call-print"></p>
    </fieldset>
  </section>
</section>

'''
s = s[:start] + new07 + s[end:]

# ---- cover lock strip + band ----
rep('<div class="lock open" data-for="mark-primary"><div class="k">The mark</div><div class="v">13 options</div>',
    '<div class="lock open" data-for="mark-primary"><div class="k">The mark</div><div class="v">The avenue — 14 drawings</div>')
rep('<div class="c"><div class="n serif">13</div><div class="l">marks on the table</div></div>',
    '<div class="c"><div class="n serif">14</div><div class="l">avenue drawings</div></div>')

# ---- lines: Cara's own line ----
rep('<li><b>The last property manager you\'ll switch to.</b>',
    '<li><b>Where trust meets performance.</b> Cara\'s own line, from her logo explorations this week — the promise in one breath, classic agency register. Reads as a statement of fact rather than a feeling, which is its strength and its risk. <span class="hz">candidate hero · on the ballot below</span></li>\n        <li><b>The last property manager you\'ll switch to.</b>')
rep('<label><input type="radio" name="lines-hero" value="aig" data-label="Answered. Inspected. Guaranteed."> Answered. Inspected. Guaranteed.</label>',
    '<label><input type="radio" name="lines-hero" value="aig" data-label="Answered. Inspected. Guaranteed."> Answered. Inspected. Guaranteed.</label>\n        <label><input type="radio" name="lines-hero" value="wtmp" data-label="Where trust meets performance."> Where trust meets performance. <span class="lockstate">Cara\'s</span></label>')

# ---- applications: working mark = The Avenue, icon = The Lane ----
s = s.replace('kit/marks/12-full-circle.svg', 'kit/marks/21-plain-avenue.svg')
s = s.replace('kit/marks/icons/full-circle-icon.svg', 'kit/marks/icons/avenue-icon.svg')
s = s.replace('kit/marks/05-windowsill.svg', 'kit/marks/25-canopy.svg')
rep('Drawn with the Full Circle as the working mark and the recommended pairing (the plant tag borrows the Windowsill); everything re-sets once the calls are made.',
    'Drawn with The Plain Avenue as the working mark, The Lane as its small cut and the recommended type pairing (the plant tag borrows The Canopy); everything re-sets once the calls are made.')

# ---- colour chapter sentence about every mark ----
s = s.replace('the rain-blue moment, a drop or the Southern Cross, in every mark', 'the rain-blue moment, the evening star above the house, in every mark')

p.write_text(s, encoding="utf-8")
print("index.html patched:", len(cards), "avenue cards +", len(RESERVE), "reserve")
