"""Regenerate ONLY the type chapter (reopened 4/10/26): ten pairings, one ballot (type-pairing).
EB Garamond + Nunito Sans is the standing call and the default the book is set in until another is picked.
Single source of truth for the pairings: writes the chapter into index.html AND the PAIRS map into book.js
(between the /* PAIRS:start */ and /* PAIRS:end */ markers).
Run: python src/regen_type.py   (idempotent)
"""
import pathlib, re, json, html as H

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERIF_FB = '"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif'
SANS_FB = '"Avenir Next","Avenir","Segoe UI",system-ui,sans-serif'
DEFAULT = "ebg-ns"

# id, display family, display kind, text family, chip, says, watch, extra class
PAIRS = [
    ("ebg-ns", "EB Garamond", "serif", "Nunito Sans", "standing call",
     "Classical and light on the page. A Garamond is the quietly confident, bookish choice, and the rounded sans beside it keeps it friendly. This is what the book, the lockups and the cards are set in today.",
     "Fine strokes thin out on signage and at very small sizes, so boards need a size bump. Slightly literary.", ""),
    ("corm-jost", "Cormorant Garamond", "serif", "Jost", "boutique",
     "The most boutique of the ten. A high-contrast display Garamond with sharp, elegant capitals, paired with a geometric sans in the Futura line. Jost is very close to the lettering on Cara's first logo sheet and on the simplified logos.",
     "Cormorant is a display face only: delicate, sets small, never for paragraphs. Everything in it needs to run a size larger.", "big"),
    ("play-mont", "Playfair Display", "serif", "Montserrat", "the industry classic",
     "Confident and high-contrast. The pairing many premium agencies reach for, so owners read it as property at a glance.",
     "Familiar for the same reason. It can read as a sales agency rather than a management-only one, which is the opposite of the position.", ""),
    ("fraun-inter", "Fraunces", "serif", "Inter", "modern and warm",
     "A soft, slightly quirky old-style serif with the most neutral screen sans there is. Feels like a new-generation business: warm headline, very clear forms and statements.",
     "Fraunces has a strong personality. Charming now, and the sort of face that can date.", ""),
    ("lora-karla", "Lora", "serif", "Karla", "approachable",
     "Brushed, friendly curves and a plain-spoken sans. Reads warm and honest, the tone of a manager who picks up the phone. Comfortable in long letters to owners.",
     "The least premium of the serif options. Good for trust, weaker for a top-of-market feel.", ""),
    ("marc-josefin", "Marcellus", "serif", "Josefin Sans", "inscriptional",
     "Roman carved capitals, like a street name cut into stone, with an elegant thin geometric sans. AVEN in capitals looks its best here, and Josefin matches the simplified logo lettering.",
     "Marcellus has one weight and no italic. Josefin has a low x-height, so small body text runs small and needs a size bump.", ""),
    ("caslon-mulish", "Libre Caslon Text", "serif", "Mulish", "established",
     "An English book face with three centuries behind it. Reads as a firm that has been here a long time: steady, traditional, trustworthy. Mulish stays out of its way.",
     "Can feel conservative, closer to a law firm than a fresh local business.", ""),
    ("ss4-inter", "Source Serif 4", "serif", "Inter", "practical",
     "Sturdy and screen-first. The strongest pairing for statements, inspection reports, forms and the owner portal, where most of the reading actually happens.",
     "The least distinctive on a sign or a card. Competent more than memorable.", ""),
    ("crimson-ns", "Crimson Pro", "serif", "Nunito Sans", "warm classical",
     "The warmest serif here and the closest to the original Mac-only face the brand started with. Darker on the page than Garamond, so it holds up better at small sizes.",
     "A near neighbour of the standing call. The difference is real but subtle, mostly weight and warmth.", ""),
    ("jost-jost", "Jost", "sans", "Jost", "all sans",
     "No serif at all: thin geometric capitals for display and the same family for text. This is the voice of Cara's first sheet and the simplified logos carried through everything. Modern, minimal, very clean on signage.",
     "Gives up the warmth a serif brings, and plenty of agencies look like this. The serif is part of what sets the book apart today.", "light"),
]


def fam(name, kind):
    return f'"Cand {name}",' + (SERIF_FB if kind == "serif" else SANS_FB)


def attr(css):
    return css.replace('"', "'")


cards, opts, js = [], [], {}
for i, (pid, dn, dk, tn, chip, says, watch, extra) in enumerate(PAIRS):
    no = f"{i + 1:02d}"
    title = f"{dn} + {tn}" if dn != tn else f"{dn}, display and text"
    ps, pa = fam(dn, dk), fam(tn, "sans")
    js[pid] = [ps, pa]
    cls = "pair" + (f" {extra}" if extra else "")
    cards.append(f'''      <div class="{cls}" data-pair="{pid}" style="--ps:{attr(ps)};--pa:{attr(pa)}">
        <div class="ph"><span class="no">{no}</span><span class="ttl">{H.escape(title)}</span><span class="chip">{H.escape(chip)}</span></div>
        <div class="spec">
          <div class="wm">AVEN<small>PROPERTY</small></div>
          <div class="hl">AVEN represents the road ahead.</div>
          <div class="bd">We benchmark every property before changing anything, manage to published service standards, and back it all with written guarantees.</div>
          <div class="who2"><span class="n">Cara Nash</span><span class="r">Licensee &amp; Director</span></div>
          <div class="lb">Property management · Bunbury &amp; the South West</div>
        </div>
        <div class="notes"><p><b>Says</b> {H.escape(says)}</p><p><b>Watch</b> {H.escape(watch)}</p></div>
        <button type="button" class="pick" data-pick="type-pairing:{pid}">Set the book in this pairing</button>
      </div>''')
    state = ' <span class="lockstate">standing</span>' if pid == DEFAULT else ""
    opts.append(f'        <label><input type="radio" name="type-pairing" value="{pid}" data-label="{H.escape(title)}"> {no} · {H.escape(title)}{state}</label>')

NL = chr(10)
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")
m = re.search(r'<section class="chapter" id="(c(\d\d)-type)"[^>]*>', s)
assert m, "type chapter not found"
cid, nn = m.group(1), m.group(2)
am = re.search(r'href="#c(\d\d)-apps"', s)
apps_nn = am.group(1) if am else "11"

section = f'''<section class="chapter" id="{cid}" data-calls="type-pairing">
  <div class="part reveal"><div class="big-num">{nn}</div><div class="p-num">Chapter {nn}</div><h2 class="serif">Type</h2>
  <p>Reopened on 4 October. EB Garamond with Nunito Sans was the call on 27 September and it still stands: the book is set in it until a different pairing is picked. Below are ten pairings that suit a calm, structured, boutique property manager, each shown as the wordmark, a headline, a paragraph, a name and a label. Choose one and the whole book re-sets itself, the business cards in chapter {apps_nn} included, so it can be read in place before anything is locked.</p></div>
  <section class="option reveal">
    <div class="eyebrow">Ten pairings · a display face for what we want remembered, a text face for what we want read</div>
    <div class="pairs">
{NL.join(cards)}
    </div>
    <div class="checks">
      <div class="check"><div class="k">What stands</div><div class="v">Pairing 01 is the default. It was called on 27 September, the kit and the logo lockups are built on it, and nothing changes unless a different pairing is picked below. Picking 01 again simply confirms it. All ten are open-licence fonts hosted inside this book, free to use in print, on signage and on the website, with no per-seat fees.</div></div>
      <div class="check"><div class="k">How to judge</div><div class="v">Read the name first, then the paragraph. The display face has to carry AVEN in capitals at sign size and a name on a business card. The text face has to stay readable in a nine-point statement and on a phone. If the logo ends up being one of the simplified options, look hardest at the pairings whose sans matches that lettering: 02, 06 and 10.</div></div>
    </div>
    <fieldset class="call" data-id="type-pairing" data-label="Type pairing">
      <legend>Your call — type pairing — reopened 4/10</legend>
      <div class="q">Which pairing is the brand set in? 01 stands until another is picked. Choosing one re-sets the whole book so it can be read in place.</div>
      <div class="opts">
{NL.join(opts)}
      </div>
      <textarea data-note placeholder="Anything to mix? e.g. this display face with that text face"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <div class="cols">
      <div class="panel"><h4>Type rules, whichever pairing wins</h4><ul>
        <li>Display face for the wordmark, taglines, pull quotes and chapter headings. Text face for everything else.</li>
        <li>Headings in sentence case. Wide-tracked capitals only for small labels: eyebrows, the PROPERTY line, sign-board footers.</li>
        <li>Taglines set straight. No italics on any line the brand wants remembered.</li>
        <li>Body copy at a comfortable size with generous leading. Calm is mostly white space.</li>
      </ul></div>
      <div class="panel"><h4>Never</h4><ul>
        <li>Bold display headlines. The display face works at regular weight; bold makes it shout.</li>
        <li>Condensed or novelty faces borrowed from another brand.</li>
        <li>All-caps sentences. Exclamation logos.</li>
        <li>The display face in UI labels or forms.</li>
      </ul></div>
    </div>
  </section>
</section>

'''
start = s.rfind("<!-- =====================", 0, m.start())
head_end = m.start()
end = s.index("<!-- =====================", m.end())
s = s[:head_end] + section + s[end:]
p.write_text(s, encoding="utf-8")

# book.js PAIRS map
j = ROOT / "book.js"
b = j.read_text(encoding="utf-8")
block = "/* PAIRS:start */\n  var PAIR_DEFAULT = " + json.dumps(DEFAULT) + ";\n  var PAIRS = {\n" + ",\n".join(
    f"    {json.dumps(k)}: [{json.dumps(v[0])}, {json.dumps(v[1])}]" for k, v in js.items()) + "\n  };\n  /* PAIRS:end */"
assert "/* PAIRS:start */" in b, "book.js has no PAIRS markers - run out/_patch_type_js.py first"
b = re.sub(r"/\* PAIRS:start \*/.*?/\* PAIRS:end \*/", lambda _: block, b, flags=re.S)
j.write_text(b, encoding="utf-8")
print(f"type chapter {nn} regenerated: {len(PAIRS)} pairings, default {DEFAULT}; book.js PAIRS updated")
