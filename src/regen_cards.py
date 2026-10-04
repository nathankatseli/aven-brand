"""Business cards in the applications chapter (second draft, 4/10/26).
Three directions designed and judged: A portrait-led (shown), B logo-led and C vertical (folded alternates).
Sources live in src/cards/ (cards_a|b|c.fragment.html + cards.css); a fresh design round drops new files in out/
and this script copies them across. Injects between <!-- CARDS:start/end --> in index.html and
/* CARDS:start/end */ in book.css. Run: python src/regen_cards.py   (idempotent)
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "cards"
SRC.mkdir(exist_ok=True)
OUT = ROOT / "out"
for name in ("cards_a.fragment.html", "cards_b.fragment.html", "cards_c.fragment.html"):
    if (OUT / name).exists():
        shutil.copyfile(OUT / name, SRC / name)
if (OUT / "cards_final.css").exists():
    shutil.copyfile(OUT / "cards_final.css", SRC / "cards.css")

frag = {k: (SRC / f"cards_{k}.fragment.html").read_text(encoding="utf-8").strip() for k in "abc"}
css = (SRC / "cards.css").read_text(encoding="utf-8").strip()

block = f'''<!-- CARDS:start -->
    <div class="eyebrow">Business cards · second draft</div>
    <div class="app cardset">
      <div class="k">Direction A · portrait-led, 90 × 55 mm</div>
      <div class="cardstage">
{frag["a"]}
      </div>
      <p>The front is mostly paper: a portrait panel on the left, the working logo with the name set in type, then name, title and three contact lines. The portrait panels are placeholders until the photos are taken; a photo drops straight into the same frame. The back is the one dark surface in the system: the mark reversed on pine, the descriptor, the web address and a code that saves the contact to a phone, one per person. An alternate back without the code sits beside them. The cards are set in the standing type pairing and follow whichever pairing is picked in the type chapter.</p>
      <p class="fine">Borrowed from the Hybrid Ag cards: landscape format, name then title, accent contact icons and a personal QR code on the back. Borrowed from agency cards generally: the portrait, because people keep the card of a face they remember. Screen mockup at 90 × 55 mm. Portrait panel and pine back bleed 3 mm; all type sits inside a 4 mm safe margin. The logo needs its vector redraw and the QR a real contact file before print.</p>
    </div>
    <details class="fold-family cards-alt">
      <summary>Two other card directions · B logo-led and C vertical</summary>
      <div class="app cardset">
        <div class="k">Direction B · logo-led</div>
        <div class="cardstage">
{frag["b"]}
        </div>
        <p>The front is almost empty: the logo, a hairline and the name. The person, the portrait and the contact details move to the back. The quietest front of the three; the back carries more.</p>
      </div>
      <div class="app cardset">
        <div class="k">Direction C · vertical, 55 × 90 mm</div>
        <div class="cardstage">
{frag["c"]}
        </div>
        <p>A tall card built on an arch: the portrait sits in one on the front, the logo in a larger one on the back. Distinctive in the hand, and a bigger step away from the cards people already keep.</p>
      </div>
    </details>
    <fieldset class="call" data-id="cards" data-label="Business card direction">
      <legend>Your call — business cards</legend>
      <div class="q">Which card direction goes to print once the portraits and the logo are settled?</div>
      <div class="opts">
        <label><input type="radio" name="cards" value="a" data-label="A · Portrait-led"> A · Portrait-led <span class="lockstate">recommended</span></label>
        <label><input type="radio" name="cards" value="b" data-label="B · Logo-led"> B · Logo-led</label>
        <label><input type="radio" name="cards" value="c" data-label="C · Vertical"> C · Vertical</label>
        <label><input type="radio" name="cards" value="notes" data-label="Tweaks, see note"> Tweaks, see note</label>
      </div>
      <textarea data-note placeholder="What to change on the cards? QR code on the back, or the quiet back?"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <div class="eyebrow" style="margin-top:var(--s6)">Everything else</div>
    <!-- CARDS:end -->'''

p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
if "<!-- CARDS:start -->" in s:
    s = re.sub(r"<!-- CARDS:start -->.*?<!-- CARDS:end -->", lambda _: block, s, flags=re.S)
else:
    # first run: drop the two old business-card tiles, put the new set ahead of the applications grid
    m = re.search(r'<section class="chapter" id="c\d\d-apps"[^>]*>', s)
    assert m, "apps chapter not found"
    end = s.index("<!-- =====================", m.end())
    chap = s[m.start():end]
    n_before = chap.count('<div class="app">')
    chap = re.sub(r'\n      <div class="app"><div class="k">Business card — front</div>.*?</div>\n(?=      <div class="app">)', "\n", chap, count=1, flags=re.S)
    chap = re.sub(r'\n      <div class="app"><div class="k">Business card — back</div>.*?</div>\n(?=      <div class="app">)', "\n", chap, count=1, flags=re.S)
    assert chap.count('<div class="app">') == n_before - 2, (n_before, chap.count('<div class="app">'))
    anchor = '    <div class="apps">'
    assert chap.count(anchor) == 1
    chap = chap.replace(anchor, "    " + block + "\n" + anchor, 1)
    s = s[:m.start()] + chap + s[end:]
p.write_text(s, encoding="utf-8")

c = ROOT / "book.css"
t = c.read_text(encoding="utf-8")
host = (SRC / "host.css").read_text(encoding="utf-8").strip()
cblock = "/* CARDS:start */\n" + host + "\n" + css + "\n/* CARDS:end */"
if "/* CARDS:start */" in t:
    t = re.sub(r"/\* CARDS:start \*/.*?/\* CARDS:end \*/", lambda _: cblock, t, flags=re.S)
else:
    t = t.rstrip("\n") + "\n\n/* ---------- V3.2: business cards, second draft ---------- */\n" + cblock + "\n"
c.write_text(t, encoding="utf-8")
print("cards injected: A shown, B + C folded; css", len(css), "chars")
