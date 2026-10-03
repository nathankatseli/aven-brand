"""Regenerate ONLY the logo chapter: Cara's ChatGPT logo leads (option A),
the fourteen generated avenue drawings follow (B-O), three in reserve (P-R).
Run: python src/regen_ch07.py   (idempotent - replaces the whole section, wherever it now sits)
The chapter is found by its id (c<NN>-logo, or the pre-V3 c07-mark) and ends at the next chapter marker.
"""
import pathlib, re, sys, html as H

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import avenue  # noqa: E402

WEARS = {
    20: "signage, website hero, welcome pack cover, letterhead.",
    21: "everything — the all-rounder: business card, email signature, boards.",
    22: "social tiles, the fee brochure cover, anywhere it sits on cloud or paper.",
    23: "signage at distance, vehicle decal, one-colour print, embroidery.",
    24: "\"For Lease\" boards, letterbox drops, tenant welcome material.",
    25: "welcome cards, seasonal social, the plant tag, the booklet cover.",
    26: "South West regional material, rural and lifestyle listings.",
    27: "dark-mode website, the card back, evening social posts.",
    28: "stamps, embroidery, very small print, dark backgrounds.",
    29: "social avatar, window decal, wax-seal and stamp moments.",
    30: "quiet uses — document footer, lapel pin, email footer.",
    31: "monogram uses — cufflinks, pin, watermark, document corner.",
    32: "favicon, phone contact, app icon at small sizes, embroidery.",
    33: "app icon, social avatar, Google Business Profile, favicon.",
}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

marks = sorted(avenue.MARKS, key=lambda m: m[0])
assert len(marks) == 14, len(marks)

p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
m = re.search(r'<section class="chapter" id="(c(\d\d)-(?:logo|mark))"[^>]*>', s)
assert m, "logo chapter not found"
open_tag, nn = m.group(0), m.group(2)
nm = re.search(r'href="#c(\d\d)-name"', s)
name_nn = nm.group(1) if nm else "05"

cards, opts_p, opts_s = [], [], []

# --- option A: Cara's own logo ---
cards.append("      <div class=\"card fav\"><div class=\"art\"><img src=\"assets/cara/cara-a.jpg\" alt=\"Cara's A — her ChatGPT logo: the road's edges rise into an A-frame with the tree-lined avenue inside\"></div>"
             "<div class=\"body\"><div class=\"tag\">A · <span class=\"favnote\">Cara's pick</span></div><div class=\"nm serif\">Cara's A</div>"
             "<p>Cara's own round, drawn in ChatGPT: the road's edges rise into an A-frame and the tree-lined avenue runs away inside it — the letter is the journey. Wordmark beneath, tagline set with the slash. The current frontrunner — not yet the lock; more concepts to explore next round (a cleaner serif-A variant from the same session is held with it).</p>"
             f"<p><b>To productionise:</b> it's a raster image, so if it wins we redraw it as vector in the family grammar (closest drawn cousin: The A, option M) for signage, embroidery and one-colour print. Note it says <i>Real Estate</i> — the registered name is AVEN Property; the descriptor call lives in chapter {name_nn}.</p></div></div>")
opts_p.append("        <label><input type=\"radio\" name=\"mark-primary\" value=\"caras-a\" data-label=\"A · Cara's A (ChatGPT)\"> A · Cara's A</label>")
opts_s.append("        <label><input type=\"checkbox\" name=\"mark-secondary\" value=\"caras-a\" data-label=\"Cara's A\"> Cara's A</label>")

# --- B-G: rendered concepts, made to the same brief grammar as Cara's ---
RENDERED = [
    ("r-aframe", "The Avenue A", "Cara's idea taken straight: the road's edges rise into a tall serif A and the tree-lined avenue runs away inside it toward a lit house. Same drawing as her frontrunner, with the right descriptor.", "signage, website hero, welcome pack cover, proposals."),
    ("r-circle", "The Circle", "A ring holds the avenue and the house at the end of it; the road leaves the ring through a gap at the base. The crest version, and the one that works as a stamp or avatar.", "social avatar, window decal, stamp, wax seal."),
    ("r-serif-a", "The Serif A", "A classical A with the road painted up through the letter to a house at the apex and the crossbar as the horizon. The most typographic of the set.", "letterhead, email signature, the card back."),
    ("r-landscape", "The Landscape", "No frame at all: the avenue, the house and the evening light fading into the paper. The warmest telling, and the one that says Bunbury.", "website hero, booklet cover, the plant tag."),
    ("r-house", "The House", "A gabled house outline with the avenue inside it; the front door is where the road begins. The destination made literal.", "\"For Lease\" boards, letterbox drops, tenant material."),
    ("r-monogram", "The Monogram", "Two rows of cypress converge into an A with the house glowing at the apex. Minimal, almost a monogram; the one that survives smallest.", "favicon, app icon, embroidery, the small cut."),
]
for i, (slug, name, desc, wears) in enumerate(RENDERED):
    letter = LETTERS[i + 1]
    tag = f'{letter} · <span class="favnote">rendered</span>' if i else f'{letter} · <span class="favnote">rendered · closest to Cara\'s</span>'
    cards.append(f'      <div class="card"><div class="art photo"><img src="assets/concepts/{slug}.jpg" alt="{H.escape(name)} logo concept"></div><div class="body"><div class="tag">{tag}</div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc)}</p><p><b>Wears well on:</b> {wears}</p></div></div>')
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{slug}" data-label="{letter} · {H.escape(name)}"> {letter} · {H.escape(name.replace("The ", ""))}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{slug}" data-label="{H.escape(name)}"> {H.escape(name.replace("The ", ""))}</label>')
OFFSET = 1 + len(RENDERED)

# --- H-U: the fine-line family (vector reserve) ---
drawn = []
for i, (num, slug, label, fn) in enumerate(marks):
    name, _, desc = label.partition(" - ")
    letter = LETTERS[i + OFFSET]
    tag = letter
    if num == 21:
        tag = f'{letter} · <span class="favnote">drawn-set pick</span>'
    elif num == 32:
        tag = f'{letter} · <span class="favnote">small cut</span>'
    elif num == 33:
        tag = f'{letter} · <span class="favnote">app icon</span>'
    drawn.append(f'      <div class="card"><div class="art"><img src="kit/marks/{num}-{slug}.svg" alt="{H.escape(name)} logo"></div><div class="body"><div class="tag">{tag}</div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc[0].upper() + desc[1:])}.</p><p><b>Wears well on:</b> {WEARS[num]}</p></div></div>')
    short = name.replace("The ", "")
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{slug}" data-label="{letter} · {H.escape(name)}"> {letter} · {H.escape(short)}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{slug}" data-label="{H.escape(short)}"> {H.escape(short)}</label>')

RESERVE = [
    ("01-doorway", "doorway", "The Doorway", "Round-one favourite — the arched door with the Southern Cross as its fanlight."),
    ("02-signature", "signature", "The Signature", "No symbol; the name is the logo, one raindrop through the rule."),
    ("12-full-circle", "full-circle", "Full Circle", "Ring broken at the top, the drop falling into the gap — Cara's circular brief, answered literally."),
]
res_cards = "".join(f'      <div class="card small"><div class="art"><img src="kit/marks/{f}.svg" alt="{n} logo"></div><div class="body"><div class="tag">{LETTERS[OFFSET + 14 + i]} · <span class="favnote">reserve</span></div><div class="nm serif">{n}</div><p>{d}</p></div></div>\n' for i, (f, v, n, d) in enumerate(RESERVE))
for i, (f, v, n, d) in enumerate(RESERVE):
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{v}" data-label="{LETTERS[OFFSET + 14 + i]} · {n}"> {LETTERS[OFFSET + 14 + i]} · {n.replace("The ", "")}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{v}" data-label="{n.replace("The ", "")}"> {n.replace("The ", "")}</label>')

NL = chr(10)
section = f'''{open_tag}
  <div class="part reveal"><div class="big-num">{nn}</div><div class="p-num">Chapter {nn}</div><h2 class="serif">The logo</h2>
  <p>One idea — trees either side, a house in the middle, a road running down to it — and Cara drew it best. Her concept leads this chapter as option A, and the six concepts after it are made to the same standard and the same brief, with the right descriptor on them. The fine-line drawings from the last round now sit folded below as the vector reserve: they are what the winner gets redrawn into for favicons, embroidery and one-colour print, where a painted emblem can't go. One primary to pick; up to two secondaries to keep for campaigns.</p></div>
  <section class="option reveal">
    <blockquote class="cara-q">Inspired by the words Avenue and Avenir, AVEN represents the road ahead.<cite>Cara — the story the logo is drawn from</cite></blockquote>
    <div class="checks">
      <div class="check"><div class="k">How Cara's concept was made — and how these match it</div><div class="v">Her concept came out of ChatGPT's image model from a short brief, and the brief is the whole trick: a classical serif letter, a tree-lined avenue painted in soft photographic detail, muted olive and sage on warm textured paper, the wordmark set inside the picture. Concepts B to G were made by writing that same brief grammar into an image model, one composition at a time, so they sit beside hers as equals rather than as sketches. All seven are painted images, not vectors — the choice here is the direction; the vector redraw for small sizes comes after.</div></div>
    </div>
    <div class="quad">
{NL.join(cards)}
    </div>
    <details class="fold-family">
      <summary>The fine-line family — fourteen vector drawings, kept as the reserve for small cuts and one-colour print</summary>
      <div class="quad">
{NL.join(drawn)}
      </div>
      <div class="eyebrow" style="margin-top:var(--s6)">Held in reserve — the earlier direction</div>
      <div class="quad three">
{res_cards}      </div>
    </details>
    <div class="checks">
      <div class="check"><div class="k">Small-format rule</div><div class="v">A painted emblem lives on the website, proposals, signage and print. It cannot be a favicon, an embroidery or a one-colour stamp; for those the winning direction is redrawn as a vector small cut in the fine-line grammar (the reserve below), the way The Lane and The Tile already are. For now the browser tab carries a crop of Cara's concept.</div></div>
      <div class="check"><div class="k">How to choose</div><div class="v">Imagine it on a "For Lease" board at forty metres, embroidered on a shirt, and as a dot in a phone contact. The right one works in all three. A secondary logo can be the one you love that fails one of the tests.</div></div>
    </div>
    <fieldset class="call" data-id="mark-primary" data-label="Primary logo">
      <legend>Your call — primary</legend>
      <div class="q">Which drawing is the brand?</div>
      <div class="opts">
{NL.join(opts_p)}
      </div>
      <textarea data-note placeholder="What to tweak on the winner?"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <fieldset class="call" data-id="mark-secondary" data-label="Secondary logos (campaign use)">
      <legend>Your call — secondaries (up to two) — round 3</legend>
      <div class="q">With Cara's A as the frontrunner, which drawn logos stay alive for campaigns, social and welcome material?</div>
      <div class="opts">
{NL.join(opts_s)}
      </div>
      <textarea data-note placeholder="Note"></textarea>
      <p class="call-print"></p>
    </fieldset>
  </section>
</section>

'''

start = m.start()
end = s.index("<!-- =====================", start)
s = s[:start] + section + s[end:]
p.write_text(s, encoding="utf-8")
print(f"logo chapter {nn} regenerated:", len(cards), "rendered cards (Cara first) +", len(drawn), "drawn +", len(RESERVE), "reserve")
