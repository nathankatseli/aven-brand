"""Regenerate ONLY the logo chapter.
Order: A = Cara's concept (frontrunner) -> research panel -> AU1-AU17 Australian set (round 5, 4/10/26)
-> folded earlier rounds: S1-S10 simplified + P1-P6 painted -> folded fine-line family D1-D14 + reserve R1-R3.
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
             f"<p><b>To productionise:</b> it's a raster image, so if it wins we redraw it as vector for signage, embroidery and one-colour print. Closest cousins already drawn: AU2 Cara's A, Replanted, which keeps her letter and changes the trees, S2 The Outline A, and {cousin} The A in the fine-line family. Note it says <i>Real Estate</i>; the registered name is AVEN Property; the descriptor call lives in chapter {name_nn}.</p></div></div>")
group("The frontrunner")
opts_p.append("        <label><input type=\"radio\" name=\"mark-primary\" value=\"caras-a\" data-label=\"A · Cara's A (ChatGPT)\"> A · Cara's A</label>")
opts_s.append("        <label><input type=\"checkbox\" name=\"mark-secondary\" value=\"caras-a\" data-label=\"A · Cara's A\"> A · Cara's A</label>")

# --- AU1-AU17: the Australian set (round 5), built from the research in out/au_research.json ---
AU_GROUPS = [
    ("The brief, re-planted", "Cara's brief exactly as she gave it, with the species, the roof and the road moved home.", [
        ("au-gum-avenue", "The Gum Avenue", "Cara's brief exactly as she gave it, moved home: a road running up to a low verandah house, gums either side, held in a ring. The trees lean, differ in height and you can see sky through them.", "signage, stamps, the social avatar, shirt embroidery.", "the house is fine line work and needs a heavier cut when small."),
        ("au-replanted-a", "Cara's A, Replanted", "Her frontrunner with the trees changed: the same crossbar-less A, with two gums standing either side, one taller than the other. The smallest move from option A that changes the continent.", "business card, letterhead, boards.", "the safest option, so it may read as a tweak more than a rethink."),
        ("au-gum-a", "The Gum A", "Two gum trunks cross to make the A, their foliage held in separate clumps at the branch ends, and a low verandah house stands where the crossbar would be. The path runs out toward you.", "boards, website header, welcome pack cover.", "the clumps must stay separate and uneven, or it becomes an umbrella tree."),
        ("au-open-ring", "The Open Ring", "The badge with its top taken off, so the gums stand up into open sky. Pale trunks cut out of the dark, and a low roof at the end of the road.", "signage, window decal, stamps, the card back.", "reads best large; the pale trunks thin out when small."),
        ("au-pepp-haven", "The Peppermint Haven", "Two peppermint trees, the ones on every Bunbury verge, shelter a low verandah house and the path to it. The haven half of the name, drawn as a picture.", "welcome material, tenant packs, social tiles.", "draw the hem too even and the trees become mushrooms."),
    ]),
    ("From here: Bunbury and the South West", "Options a local would recognise as ours before reading the name.", [
        ("au-pepp-verge", "The Peppermint Verge", "The street seen from the footpath: a low hip-roofed house, an old peppermint sheltering it and a young one coming up beside it. An old tree and a new one is the long view in one picture.", "website hero, welcome pack, community sponsorship.", "an illustration more than a mark; it needs a square crop designed beside it."),
        ("au-road-ahead", "The Road Ahead", "A flat horizon, a big sky and one evening light. The road runs on past the house instead of stopping at it, one gum breaks the skyline, and the low roof sits to one side.", "website header, proposals, letterhead, social tiles.", "reduced, it is a line and a triangle, so the gum and the roof have to stay bold."),
        ("au-colonnade", "The Gum Colonnade", "A gum avenue the way it looks from the car: pale trunks standing in shade under a broken canopy, the road running between them to a low roof. Drawn in the shape of a sign board.", "\"For Lease\" boards, vehicle decal, social tiles.", "pale uprights in a dark box can read as bars if they are drawn too even."),
    ]),
    ("In the letters", "The Australian cue built into the A, the V or the wordmark itself.", [
        ("au-cathedral-a", "The Cathedral A", "Two unequal trunks lean in and meet, the way trees do over the old coast road north of town. Nobody planted that avenue, which is why the A is lopsided.", "monogram, favicon, embroidery, lapel pin.", "without the leaves it is a tent; the lopsidedness is the point."),
        ("au-hanging-leaves", "The Hanging Leaves", "Gum leaves hang point down, so two of them make the V. One quiet change to the wordmark that moves it to the right continent.", "everything; pairs with any of the symbols as its wordmark.", "it says Australia in general, and nothing about avenues or property on its own."),
        ("au-verandah-line", "The Verandah Line", "The name stands under a verandah: a low hip roof with a separate, flatter verandah roof stepping out beneath it, and the four letters as the posts.", "boards at distance, embroidery, favicon, stationery.", "it drops the trees and the road, and a roof over a name is common in real estate."),
        ("au-avenue-letter", "The Avenue Letter", "No separate symbol. The A of AVEN is two gum trunks leaning together with their foliage at the top, so the name itself is the avenue.", "wordmark uses, email signature, website header.", "the lettering is heavier than the thin wordmark used so far."),
    ]),
    ("Out of the box", "The avenue left behind where it helps. Bolder ideas, each still something an owner would trust.", [
        ("au-verandah-ave", "The Verandah Avenue", "The avenue and the house as one drawing: a low verandah roof held up by gum trunks instead of posts, with the road running out from under it.", "boards, the card back, the social avatar.", "some people will see a carport or a picnic shelter; test it cold."),
        ("au-hollow-home", "The Hollow Home", "One old gum with one small hollow. The South West's black cockatoos nest in the hollows of very old gums, so the home is in the tree, and it takes a century of care to make one.", "welcome material, community sponsorship, a secondary mark.", "to a landlord a hollow old tree can also mean risk; and there is no house or road in it."),
        ("au-verandah", "The Verandah", "No avenue at all: the front of a house under a curved verandah, with a gum branch hanging into the corner. A verandah keeps the weather off the walls before the damage starts, which is the promise in one picture.", "website header, welcome pack, tenant material.", "it reads heritage cottage, older than most homes we will manage, and needs a simplified cut."),
        ("au-street-blade", "The Street Blade", "AVEN is short for avenue, so the logo is a street-name blade with a gum where the crest would sit. The \"For Lease\" board, the office sign and the letterhead can all be the same object.", "boards, signage, a stationery system.", "it can look municipal, as if the council made it."),
        ("au-front-gate", "The Front Gate", "The letterbox at the front fence, drawn as a small house, with the gate open and the path running on. It is where an owner hears from us.", "a secondary mark for correspondence and statements.", "it carries no avenue; a companion mark more than the logo."),
    ]),
]
au_blocks, n_au = [], 0
for gi, (gtitle, gline, items) in enumerate(AU_GROUPS):
    cards = []
    group(f"Australian · {gtitle.lower()}" if gi else "Australian · new this round · the brief, re-planted")
    for slug, name, desc, wears, watch in items:
        n_au += 1
        code = f"AU{n_au}"
        cards.append(f'      <div class="card"><div class="art photo flat"><img src="assets/concepts/{slug}.jpg" alt="{H.escape(name)} — Australian logo option {code}" loading="lazy"></div><div class="body"><div class="tag">{code} · <span class="favnote">Australian</span></div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc)}</p><p><b>Wears well on:</b> {wears}</p><p><b>Watch:</b> {H.escape(watch)}</p></div></div>')
        opt(slug, code, name)
    first, last = n_au - len(items) + 1, n_au
    au_blocks.append(f'''    <div class="eyebrow" style="margin-top:var(--s6)">AU{first}–AU{last} · {gtitle}</div>
    <p class="grpnote">{H.escape(gline)}</p>
    <div class="quad">
{chr(10).join(cards)}
    </div>''')

# --- S1-S10: simplified flat set (round 4) ---
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
group("Simplified · round 4")
for i, (slug, name, desc, wears) in enumerate(SIMPLE):
    code = f"S{i + 1}"
    simple_cards.append(f'      <div class="card"><div class="art photo flat"><img src="assets/concepts/{slug}.jpg" alt="{H.escape(name)} — simplified logo option {code}" loading="lazy"></div><div class="body"><div class="tag">{code} · <span class="favnote">simplified</span></div><div class="nm serif">{H.escape(name)}</div><p>{H.escape(desc)}</p><p><b>Wears well on:</b> {wears}</p></div></div>')
    opt(slug, code, name)

# --- P1-P6: painted concepts (round 3), kept as options ---
RENDERED = [
    ("r-aframe", "The Avenue A", "Cara's idea taken straight: the road's edges rise into a tall serif A and the tree-lined avenue runs away inside it toward a lit house. Same drawing as her frontrunner, with the right descriptor.", "signage, website hero, welcome pack cover, proposals."),
    ("r-circle", "The Circle", "A ring holds the avenue and the house at the end of it; the road leaves the ring through a gap at the base. The crest version, and the one that works as a stamp or avatar.", "social avatar, window decal, stamp, wax seal."),
    ("r-serif-a", "The Serif A", "A classical A with the road painted up through the letter to a house at the apex and the crossbar as the horizon. The most typographic of the set.", "letterhead, email signature, the card back."),
    ("r-landscape", "The Landscape", "No frame at all: the avenue, the house and the evening light fading into the paper. The warmest telling of the six.", "website hero, booklet cover, the plant tag."),
    ("r-house", "The House", "A gabled house outline with the avenue inside it; the front door is where the road begins. The destination made literal.", "\"For Lease\" boards, letterbox drops, tenant material."),
    ("r-monogram", "The Monogram", "Two rows of cypress converge into an A with the house glowing at the apex. Minimal, almost a monogram; the one that survives smallest.", "favicon, app icon, embroidery, the small cut."),
]
painted_cards = []
group("Painted · round 3")
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

total = 1 + n_au + len(SIMPLE) + len(RENDERED) + len(drawn) + len(RESERVE)
NL = chr(10)
section = f'''{open_tag}
  <div class="part reveal"><div class="big-num">{nn}</div><div class="p-num">Chapter {nn}</div><h2 class="serif">The logo</h2>
  <p>One idea: trees either side, a house in the middle, a road running down to it. Cara's concept still leads as option A. Last round's options were simple enough, but they looked as if they belonged in Europe. So this round starts from research into what reads as Australian, and as Bunbury: the gum drawn properly, the peppermint on the verge, the verandah, the low horizon. Seventeen options come out of it, from Cara's brief re-planted to a few that leave the avenue behind. The earlier rounds stay on the table, folded beneath. One primary to pick; up to two secondaries to keep for campaigns.</p></div>
  <section class="option reveal">
    <blockquote class="cara-q">Inspired by the words Avenue and Avenir, AVEN represents the road ahead.<cite>Cara — the story the logo is drawn from</cite></blockquote>
    <div class="eyebrow" style="margin-top:var(--s5)">A · the frontrunner</div>
    <div class="quad">
{cara_card}
    </div>
  </section>
  <section class="option reveal" id="australian">
    <div class="eyebrow">What the research found</div>
    <p class="position">Before drawing anything we looked at what actually makes a picture read as Australian and as the South West: the trees on our verges, the local house, the way a road and an avenue look here, how good Australian brands signal where they are from, and what a small business should leave alone. Local and state sources throughout.</p>
    <div class="cols">
      <div class="panel"><h4>Why the last round read European</h4><ul>
        <li>The trees were cypress, poplar, oak and ball-on-a-stick shapes. None of them grows on a South West verge.</li>
        <li>Every canopy was one closed mass that started low on the trunk. A gum is the reverse: a bare trunk, a fork, and the leaves held high in separate clumps you can see sky through.</li>
        <li>Every pair of trees was a mirror image at even spacing, which is the planted estate avenue. Trees here lean, fork unevenly and differ from their neighbours.</li>
        <li>The houses were steep pointed gables with no eaves. The local house is low and wide: a hip roof of iron with a verandah on posts.</li>
        <li>The view ran straight down a drive to a house that closed it off, inside an arch or a ring, with no sky. This coast reads the other way: low, wide, a flat horizon and a lot of sky.</li>
      </ul></div>
      <div class="panel"><h4>What reads as Australian, and as ours</h4><ul>
        <li><b>The gum, drawn trunk first.</b> Bare below, leaning, forked, with a crown you can see through.</li>
        <li><b>The WA peppermint.</b> The weeping verge tree from Bunbury to the capes: a wide dome with an uneven hem.</li>
        <li><b>The tuart.</b> It grows only on this strip of coast, and the forest drive south of town is our avenue.</li>
        <li><b>The verandah and the low hip roof.</b> Shade before damage: prevention in one line.</li>
        <li><b>Trees that lean in and meet overhead,</b> as they do on the old coast road near Australind. An avenue nobody planted, and an A.</li>
        <li><b>A low horizon and a big sky,</b> with the road running on. Avenir means the future.</li>
        <li><b>The hanging gum leaf.</b> Long, curved, point down.</li>
      </ul></div>
    </div>
    <div class="checks">
      <div class="check"><div class="k">What we left out, and why</div><div class="v">No Aboriginal art styles, symbols or language: that visual culture is not ours to borrow. No coats of arms, flags, Southern Cross or green and gold. No black swan, because a black swan event is a nasty surprise and the promise is no surprises. No magpie, possum, dolphin, lighthouse or jetty: pests on a rental sign, or tourism. No red earth or windmills, which belong to another region. And nothing that needs its story told before it makes sense.</div></div>
      <div class="check"><div class="k">The colour note</div><div class="v">The research found that the olive green in last round's drawings reads Mediterranean. These are drawn in the grey-green already in the palette, with rain blue as the one light in the sky, so nothing in the colour chapter has to change. As before, every option is an image for choosing a direction; the winner is redrawn as vector.</div></div>
    </div>
    <p class="fine srcline">Sources include the <a href="https://www.bunbury.wa.gov.au/news/tree-streets-renewal-program">City of Bunbury tree streets program</a>, the <a href="https://inherit.dplh.wa.gov.au/public/inventory/printsinglerecord/4fba0b55-d601-4fa1-b026-dbf1bb8596f7">WA heritage register entry for Cathedral Avenue</a>, <a href="https://www.dbca.wa.gov.au/landscope/winter-2024/kalgulup-regional-park">DBCA on Bunbury's regional park</a>, the <a href="https://www.bgpa.wa.gov.au/kings-park/area/fraser-avenue-precinct">Kings Park gum avenue</a>, and the <a href="https://www.artslaw.com.au/information-sheet/indigenous-cultural-intellectual-property-icip-aitb/">Arts Law Centre on Indigenous cultural and intellectual property</a>.</p>
{NL.join(au_blocks)}
    <details class="fold-family">
      <summary>Earlier rounds · S1–S10 simplified and P1–P6 painted, kept as options</summary>
      <div class="eyebrow" style="margin-top:var(--s3)">S1–S10 · simplified, round 4</div>
      <div class="quad">
{NL.join(simple_cards)}
      </div>
      <div class="eyebrow" style="margin-top:var(--s6)">P1–P6 · painted, round 3</div>
      <div class="quad">
{NL.join(painted_cards)}
      </div>
    </details>
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
      <div class="check"><div class="k">Small-format rule</div><div class="v">Every option here is still an image, not a vector file. The flat options redraw as vector almost line for line, so the winner can go to signage, embroidery and one-colour print without changing character. A painted emblem cannot: it needs a simplified partner for the favicon, the stamp and the shirt. For now the browser tab carries a crop of Cara's concept.</div></div>
      <div class="check"><div class="k">How to choose</div><div class="v">Imagine it on a "For Lease" board at forty metres, embroidered on a shirt, and as a dot in a phone contact. The right one works in all three, and a Bunbury owner should look at it and think it is ours. A secondary logo can be the one you love that fails one of the tests.</div></div>
    </div>
    <fieldset class="call" data-id="mark-primary" data-label="Primary logo">
      <legend>Your call — primary — round 5</legend>
      <div class="q">Which one is the brand? {total} on the table: Cara's A, seventeen Australian options, and the earlier rounds.</div>
      <div class="opts">
{NL.join(opts_p)}
      </div>
      <textarea data-note placeholder="What to tweak on the winner? Which parts of two options would you combine?"></textarea>
      <p class="call-print"></p>
    </fieldset>
    <fieldset class="call" data-id="mark-secondary" data-label="Secondary logos (campaign use)">
      <legend>Your call — secondaries (up to two) — round 5</legend>
      <div class="q">Which others stay alive for campaigns, social and welcome material?</div>
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
s = re.sub(r'<div class="n serif">\d+</div><div class="l">logos on the table</div>', f'<div class="n serif">{total}</div><div class="l">logos on the table</div>', s)
p.write_text(s, encoding="utf-8")
print(f"logo chapter {nn} regenerated: Cara's A + {n_au} Australian + {len(simple_cards)} simplified + {len(painted_cards)} painted + {len(drawn)} drawn + {len(RESERVE)} reserve = {total}")
