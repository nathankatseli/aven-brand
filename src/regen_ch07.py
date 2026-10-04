"""Regenerate ONLY the logo chapter.
Order: A = Cara's concept (frontrunner) -> S1-S10 simplified flat set (4/10/26, closer to her first sheet)
-> P1-P6 painted set (kept as options) -> folded fine-line family D1-D14 + reserve R1-R3.
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

marks = sorted(avenue.MARKS, key=lambda m: m[0])
assert len(marks) == 14, len(marks)

p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
m = re.search(r'<section class="chapter" id="(c(\d\d)-(?:logo|mark))"[^>]*>', s)
assert m, "logo chapter not found"
open_tag, nn = m.group(0), m.group(2)
nm = re.search(r'href="#c(\d\d)-name"', s)
name_nn = nm.group(1) if nm else "05"

opts_p, opts_s = [], []


def opt(value, code, name):
    short = name.replace("The ", "")
    opts_p.append(f'        <label><input type="radio" name="mark-primary" value="{value}" data-label="{code} · {H.escape(name)}"> {code} · {H.escape(short)}</label>')
    opts_s.append(f'        <label><input type="checkbox" name="mark-secondary" value="{value}" data-label="{code} · {H.escape(short)}"> {code} · {H.escape(short)}</label>')


def group(label):
    g = f'        <div class="optgroup">{label}</div>'
    opts_p.append(g)
    opts_s.append(g)


# --- A: Cara's own concept, the frontrunner ---
cousin = next(f"D{i + 1}" for i, (num, slug, label, fn) in enumerate(marks) if label.startswith("The A "))
cara_card = ("      <div class=\"card fav\"><div class=\"art photo\"><img src=\"assets/cara/cara-a.jpg\" alt=\"Cara's A — her ChatGPT logo: the road's edges rise into an A-frame with the tree-lined avenue inside\"></div>"
             "<div class=\"body\"><div class=\"tag\">A · <span class=\"favnote\">Cara's pick</span></div><div class=\"nm serif\">Cara's A</div>"
             "<p>Cara's own round, drawn in ChatGPT: the road's edges rise into an A-frame and the tree-lined avenue runs away inside it: the letter is the journey. Wordmark beneath, tagline set with the slash. The current frontrunner, and the logo this book wears for now: the browser tab, the page header, the business cards in the applications chapter.</p>"
             f"<p><b>To productionise:</b> it's a raster image, so if it wins we redraw it as vector for signage, embroidery and one-colour print. Closest cousins already drawn: S2 The Outline A below, and {cousin} The A in the fine-line family. Note it says <i>Real Estate</i>; the registered name is AVEN Property; the descriptor call lives in chapter {name_nn}.</p></div></div>")
group("The frontrunner")
opts_p.append("        <label><input type=\"radio\" name=\"mark-primary\" value=\"caras-a\" data-label=\"A · Cara's A (ChatGPT)\"> A · Cara's A</label>")
opts_s.append("        <label><input type=\"checkbox\" name=\"mark-secondary\" value=\"caras-a\" data-label=\"A · Cara's A\"> A · Cara's A</label>")

# --- S1-S10: simplified flat set, closer to Cara's first sheet ---
SIMPLE = [
    ("s-circle", "The Badge", "The top-left tile of Cara's first sheet, cleaned up: a ring holds the avenue, the road runs up to a small house, flat trees either side. Two colours, no shading.", "signage, stamps, the social avatar, shirt embroidery."),
    ("s-aframe", "The Outline A", "Her frontrunner reduced to line: the A is a single outline, two cypress stand inside it and the road runs up the middle. Cara's A in a form that prints in one colour.", "business card, letterhead, boards, the small cut."),
    ("s-line", "The Fine Line", "One pen weight throughout: three trees, the house, three trees, and the road opening toward you. The quietest of the set and the closest to the line drawings on her sheet.", "letterhead, email signature, welcome pack, window decal."),
    ("s-wordmark", "The Leaf", "No symbol at all: the name in thin geometric capitals with a single leaf on the V. It is how many established agencies do it: the name is the logo.", "everything; pairs with any of the symbols as its wordmark."),
    ("s-house", "The Home", "A house outline with one tree inside it and the path leaving through the door. Home and tree in a single shape; reads as property at a glance.", "\"For Lease\" boards, letterbox drops, tenant material."),
    ("s-arch", "The Arch", "An arched window onto the avenue: cypress either side, the road rising to the house. The arch reads as a doorway and frames well on a board or a tile.", "boards, social tiles, the welcome pack cover."),
    ("s-tree", "The Tree", "One established tree sheltering a small house, the path curling toward you. The most illustrative of the ten, and the one that tells the haven half of the name.", "welcome cards, the plant tag, community sponsorship."),
    ("s-lockup", "The Lockup", "The avenue in a rounded square beside the name: the horizontal arrangement for website headers, email signatures and board footers. The square works alone as an app icon.", "website header, email signature, app icon, favicon."),
    ("s-monoline", "The Monoline", "The badge again, drawn in a single thin line with one green dot over the house. Lighter and more modern than S1; the dot is the only fill.", "stationery, stamps, a quiet watermark, the card back."),
    ("s-icon", "The Icon", "Five shapes: a house, two trees, a road. The most reduced symbol in the book; it survives at sixteen pixels and in one colour without a redraw.", "favicon, app icon, embroidery, signage at distance."),
]
simple_cards = []
group("Simplified · new this round")
for i, (slug, name, desc, wears) in enumerate(SIMPLE):
    code = f"S{i + 1}"
    simple_cards.append(f'      <div class="card"><div class="art photo flat"><img src="assets/concepts/{slug}.jpg" alt="{H.escape(name)} — simplified logo option {code}" loading="lazy"></div><div class="body"><div class="tag">{code} · <span class="favnote">simplified</span></div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc)}</p><p><b>Wears well on:</b> {wears}</p></div></div>')
    opt(slug, code, name)

# --- P1-P6: painted concepts from the last round, kept as options ---
RENDERED = [
    ("r-aframe", "The Avenue A", "Cara's idea taken straight: the road's edges rise into a tall serif A and the tree-lined avenue runs away inside it toward a lit house. Same drawing as her frontrunner, with the right descriptor.", "signage, website hero, welcome pack cover, proposals."),
    ("r-circle", "The Circle", "A ring holds the avenue and the house at the end of it; the road leaves the ring through a gap at the base. The crest version, and the one that works as a stamp or avatar.", "social avatar, window decal, stamp, wax seal."),
    ("r-serif-a", "The Serif A", "A classical A with the road painted up through the letter to a house at the apex and the crossbar as the horizon. The most typographic of the set.", "letterhead, email signature, the card back."),
    ("r-landscape", "The Landscape", "No frame at all: the avenue, the house and the evening light fading into the paper. The warmest telling, and the one that says Bunbury.", "website hero, booklet cover, the plant tag."),
    ("r-house", "The House", "A gabled house outline with the avenue inside it; the front door is where the road begins. The destination made literal.", "\"For Lease\" boards, letterbox drops, tenant material."),
    ("r-monogram", "The Monogram", "Two rows of cypress converge into an A with the house glowing at the apex. Minimal, almost a monogram; the one that survives smallest.", "favicon, app icon, embroidery, the small cut."),
]
painted_cards = []
group("Painted · kept from last round")
for i, (slug, name, desc, wears) in enumerate(RENDERED):
    code = f"P{i + 1}"
    painted_cards.append(f'      <div class="card"><div class="art photo"><img src="assets/concepts/{slug}.jpg" alt="{H.escape(name)} — painted logo concept {code}" loading="lazy"></div><div class="body"><div class="tag">{code} · <span class="favnote">painted</span></div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc)}</p><p><b>Wears well on:</b> {wears}</p></div></div>')
    opt(slug, code, name)

# --- D1-D14: the fine-line family (vector reserve) ---
drawn = []
group("Fine-line family · vector reserve")
for i, (num, slug, label, fn) in enumerate(marks):
    name, _, desc = label.partition(" - ")
    code = f"D{i + 1}"
    tag = code
    if num == 21:
        tag = f'{code} · <span class="favnote">drawn-set pick</span>'
    elif num == 32:
        tag = f'{code} · <span class="favnote">small cut</span>'
    elif num == 33:
        tag = f'{code} · <span class="favnote">app icon</span>'
    drawn.append(f'      <div class="card"><div class="art"><img src="kit/marks/{num}-{slug}.svg" alt="{H.escape(name)} logo" loading="lazy"></div><div class="body"><div class="tag">{tag}</div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc[0].upper() + desc[1:])}.</p><p><b>Wears well on:</b> {WEARS[num]}</p></div></div>')
    opt(slug, code, name)

RESERVE = [
    ("01-doorway", "doorway", "The Doorway", "Round-one favourite — the arched door with the Southern Cross as its fanlight."),
    ("02-signature", "signature", "The Signature", "No symbol; the name is the logo, one raindrop through the rule."),
    ("12-full-circle", "full-circle", "Full Circle", "Ring broken at the top, the drop falling into the gap — Cara's circular brief, answered literally."),
]
res_cards = "".join(f'      <div class="card small"><div class="art"><img src="kit/marks/{f}.svg" alt="{n} logo" loading="lazy"></div><div class="body"><div class="tag">R{i + 1} · <span class="favnote">reserve</span></div><div class="nm serif">{n}</div><p>{d}</p></div></div>\n' for i, (f, v, n, d) in enumerate(RESERVE))
for i, (f, v, n, d) in enumerate(RESERVE):
    opt(v, f"R{i + 1}", n)

total = 1 + len(SIMPLE) + len(RENDERED) + len(drawn) + len(RESERVE)
NL = chr(10)
section = f'''{open_tag}
  <div class="part reveal"><div class="big-num">{nn}</div><div class="p-num">Chapter {nn}</div><h2 class="serif">The logo</h2>
  <p>One idea: trees either side, a house in the middle, a road running down to it. Cara's concept still leads as option A. The painted concepts from last round had the polish but were drifting toward artwork, so this round adds ten simplified options: flat, two colours, thin geometric capitals, the way her first sheet looked and the way established agencies build a logo. The painted six stay on the table beneath them, and the fine-line drawings sit folded at the bottom as the vector reserve. One primary to pick; up to two secondaries to keep for campaigns.</p></div>
  <section class="option reveal">
    <blockquote class="cara-q">Inspired by the words Avenue and Avenir, AVEN represents the road ahead.<cite>Cara — the story the logo is drawn from</cite></blockquote>
    <div class="eyebrow" style="margin-top:var(--s5)">A · the frontrunner</div>
    <div class="quad">
{cara_card}
    </div>
    <div class="eyebrow" style="margin-top:var(--s6)">S1–S10 · simplified, closer to Cara's first sheet</div>
    <div class="checks solo">
      <div class="check"><div class="k">What changed this round</div><div class="v">A logo is not an illustration. The test of a simple one is that it is two colours, a handful of shapes, and still itself on a pen, a shirt and a sign at forty metres. These ten keep the drawing sharp but take the painting out: no gradients, no texture, no light effects. They borrow the lettering from Cara's original sheet (thin, wide-set geometric capitals with PROPERTY between two rules), so any of the symbols can swap onto the same wordmark.</div></div>
    </div>
    <div class="quad">
{NL.join(simple_cards)}
    </div>
    <div class="eyebrow" style="margin-top:var(--s6)">P1–P6 · painted, last round's concepts, kept as options</div>
    <div class="checks solo">
      <div class="check"><div class="k">How these were made</div><div class="v">Cara's concept came out of ChatGPT's image model from a short brief: a classical serif letter, a tree-lined avenue painted in soft photographic detail, muted olive and sage on warm textured paper. These six were made by writing that same brief grammar into an image model, one composition at a time. They are painted images rather than logos in the strict sense. They suit a website hero, a proposal cover or a welcome pack, and each would need a simplified cut beside it for small sizes.</div></div>
    </div>
    <div class="quad">
{NL.join(painted_cards)}
    </div>
    <details class="fold-family">
      <summary>D1–D14 · the fine-line family, fourteen vector drawings, kept as the reserve for small cuts and one-colour print</summary>
      <div class="quad">
{NL.join(drawn)}
      </div>
      <div class="eyebrow" style="margin-top:var(--s6)">R1–R3 · held in reserve, the earlier direction</div>
      <div class="quad three">
{res_cards}      </div>
    </details>
    <div class="checks">
      <div class="check"><div class="k">Small-format rule</div><div class="v">Every option here is still an image, not a vector file. The simplified ten redraw as vector almost line for line, so the winner can go to signage, embroidery and one-colour print without changing character. A painted emblem cannot: it needs a simplified partner for the favicon, the stamp and the shirt. For now the browser tab carries a crop of Cara's concept.</div></div>
      <div class="check"><div class="k">How to choose</div><div class="v">Imagine it on a "For Lease" board at forty metres, embroidered on a shirt, and as a dot in a phone contact. The right one works in all three. A secondary logo can be the one you love that fails one of the tests.</div></div>
    </div>
    <fieldset class="call" data-id="mark-primary" data-label="Primary logo">
      <legend>Your call — primary — round 4</legend>
      <div class="q">Which one is the brand? {total} on the table: Cara's A, ten simplified, six painted, and the fine-line reserve.</div>
      <div class="opts">
{NL.join(opts_p)}
      </div>
      <textarea data-note placeholder="What to tweak on the winner?"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <fieldset class="call" data-id="mark-secondary" data-label="Secondary logos (campaign use)">
      <legend>Your call — secondaries (up to two) — round 4</legend>
      <div class="q">With Cara's A as the frontrunner, which others stay alive for campaigns, social and welcome material?</div>
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
print(f"logo chapter {nn} regenerated: Cara's A + {len(simple_cards)} simplified + {len(painted_cards)} painted + {len(drawn)} drawn + {len(RESERVE)} reserve = {total}")
