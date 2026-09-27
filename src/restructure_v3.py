"""V3 restructure of index.html - one shot, reproducible, refuses to run twice.
  python src/restructure_v3.py [--dry-run]
Reorders chapters open-first, renumbers ids/markers/numerals, injects data-calls for the folds,
replaces old 03+04 with src/ch02_idea.html, swaps the lock strip for the Where-we-are shell,
and renames mark -> logo in user-facing copy only (text nodes + alt/data-label/placeholder/title).
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "index.html"
DRY = "--dry-run" in sys.argv
s = P.read_text(encoding="utf-8")
if 'id="c02-idea"' in s:
    sys.exit("already V3 - nothing to do")

# ---- split into head, chapter chunks, tail ----
MARK = re.compile(r"<!-- =+ (\d\d) =+ -->\r?\n")
parts = re.split(r"(?=<!-- =+ \d\d =+ -->)", s)
head, chunks = parts[0], parts[1:]
TAIL_SPLIT = '\n</div>\n<footer class="ink bleed">'
assert TAIL_SPLIT in chunks[-1], "footer split marker missing"
last, tail = chunks[-1].split(TAIL_SPLIT, 1)
chunks[-1] = last + "\n"
tail = TAIL_SPLIT + tail
old = {MARK.match(c).group(1): c for c in chunks}
assert sorted(old) == [f"{i:02d}" for i in range(1, 15)], sorted(old)

ORDER = [  # (new NN, old NN or None, old slug, new slug)
    ("01", "01", "how", "how"), ("02", None, None, "idea"), ("03", "07", "mark", "logo"), ("04", "06", "promise", "promise"),
    ("05", "02", "name", "name"), ("06", "05", "owner", "owner"), ("07", "08", "colour", "colour"), ("08", "09", "type", "type"),
    ("09", "10", "imagery", "imagery"), ("10", "11", "voice", "voice"), ("11", "12", "apps", "apps"), ("12", "13", "kit", "kit"),
    ("13", "14", "decisions", "decisions"),
]
CALLS = {"idea": "soi,lines-hero,lines-proof,lines-guarantee", "logo": "mark-primary,mark-secondary", "name": "name-story,name-descriptor",
         "colour": "colour", "type": "type-serif,type-sans", "imagery": "imagery", "voice": "voice", "apps": "apps=right"}
ATTR = {"owner": ' data-fold="always" data-decided="Cara\'s words, kept"'}
LABEL = {"00": "Where we are", "01": "How this session works", "02": "The idea", "03": "The logo", "04": "The promise", "05": "The name",
         "06": "The owner's story", "07": "Colour", "08": "Type", "09": "Imagery", "10": "Voice", "11": "Applications", "12": "The operator kit", "13": "Decisions"}
SLUG = {n: sn for n, o, so, sn in ORDER}


def must(txt, a, b, n=1):
    assert txt.count(a) == n, (a[:80], txt.count(a))
    return txt.replace(a, b)


def renum(c, o, n, so, sn):
    extra = (f' data-calls="{CALLS[sn]}"' if sn in CALLS else "") + ATTR.get(sn, "")
    c = must(c, f'<section class="chapter" id="c{o}-{so}">', f'<section class="chapter" id="c{n}-{sn}"{extra}>')
    c = must(c, f'<div class="big-num">{o}</div><div class="p-num">Chapter {o}</div>', f'<div class="big-num">{n}</div><div class="p-num">Chapter {n}</div>')
    return MARK.sub(f"<!-- ===================== {n} · c{n}-{sn} ===================== -->\n", c, count=1)


# ---- pieces lifted from the chapters being retired (old 03 + 04) ----
lg = re.search(r'    <fieldset class="call" data-id="lines-guarantee".*?</fieldset>\n', old["04"], re.S)
assert lg, "lines-guarantee fieldset not found in old 04"
lg = lg.group(0).replace("> Everywhere — always visible</label>", "> Yes — always visible</label>")
mission = re.search(r'    <blockquote class="cara-q">To make property management feel.*?</blockquote>\n', old["03"], re.S)
assert mission, "mission quote not found in old 03"
tpl = (ROOT / "src" / "ch02_idea.html").read_text(encoding="utf-8")
assert tpl.count("{LINES_GUARANTEE_FIELDSET}") == 1 and tpl.count("{CARA_MISSION_QUOTE}") == 1, "template placeholders"
ch02 = tpl.replace("{LINES_GUARANTEE_FIELDSET}", lg.rstrip("\n")).replace("{CARA_MISSION_QUOTE}", mission.group(0).rstrip("\n"))
if not ch02.endswith("\n\n"):
    ch02 = ch02.rstrip("\n") + "\n\n"
assert ch02.startswith("<!-- ===================== 02 · c02-idea ===================== -->"), "template must start with its marker"

body = "".join(ch02 if o is None else renum(old[o], o, n, so, sn) for n, o, so, sn in ORDER)

# ---- head rewrites ----
rail_links = "".join(f'  <a href="#{"c00-cover" if n == "00" else f"c{n}-{SLUG[n]}"}"><span class="n">{n}</span>{LABEL[n]}</a>\n' for n in ["00"] + [x[0] for x in ORDER])
m = re.search(r'(<nav class="rail"[^>]*>\n  <div class="k">[^<]*</div>\n)(.*?)(  <div class="done")', head, re.S)
assert m, "rail block"
head = head[:m.start(2)] + rail_links + head[m.end(2):]
toc_links = "".join(f'<a href="#c{n}-{SLUG[n]}">{n} {LABEL[n]}</a>' for n in [x[0] for x in ORDER])
m = re.search(r'(<details class="toc rise d4"><summary>Chapters</summary>\n\s*)(.*?)(\n\s*</details>)', head, re.S)
assert m, "toc block"
head = head[:m.start(2)] + toc_links + head[m.end(2):]
head = must(head, '<span class="n">00</span>Where we\'ve landed</div>', '<span class="n">00</span>Where we are</div>')

WHERE = '''<section class="where reveal" id="where">
  <div class="eyebrow">Where we are</div>
  <h2 class="serif">What's open, and what's decided</h2>
  <div class="lead"><span><span data-counter>0 of 0 calls made</span>. The open calls come first; a decided chapter folds to one line and opens on tap. Chapter 13 has the table and the export.</span><button type="button" class="btn ghost" data-act="show-all">Show everything</button></div>
  <details class="acc" id="where-open-acc" open><summary>Open now <span class="cnt"></span></summary><div class="list" id="where-open"></div></details>
  <details class="acc" id="where-decided-acc"><summary>Decided <span class="cnt"></span></summary><div class="list" id="where-decided"></div></details>
</section>

'''
head, n = re.subn(r'<section class="locked reveal">.*?</section>\n\n', WHERE, head, count=1, flags=re.S)
assert n == 1, "lock strip not replaced"
head = must(head, '<div class="n serif">14</div><div class="l">calls to make</div>', '<div class="n serif" data-total>15</div><div class="l">calls to make</div>')
head = must(head, "0<small>/14</small>", "0<small>/15</small>")
head = must(head, "made on this device", "made so far")
head = must(head, "AVEN Property — Brand Book · V2", "AVEN Property — Brand Book · V3")
head = must(head, "round 2 · review copy", "round 3 · review copy")

out = head + body + tail
out = must(out, "<span>Brand Book · V2</span>", "<span>Brand Book · V3</span>")
out = out.replace("Your call — round 2", "Your call — round 3")
out = must(out, "and chapter 14 turns them into a table", "and chapter 13 turns them into a table")
out = must(out, "When the calls are exported in chapter 14", "When the calls are exported in chapter 13")
out = must(out, "the descriptor call lives in chapter 02", "the descriptor call lives in chapter 05")

# ---- rename mark -> logo in user-facing copy only ----
RX = re.compile(r"(?<![\w/-])(Marks?|marks?)(?![\w/-])")
MAP = {"mark": "logo", "marks": "logos", "Mark": "Logo", "Marks": "Logos"}


def fix(mo):
    w, st, i = mo.group(1), mo.string, mo.start()
    if st[max(0, i - 12):i].endswith("exclamation "):
        return w
    if st[mo.end():mo.end() + 17] == " an open decision":
        return w
    if st[max(0, i - 11):i] == "Thank you, ":
        return w
    return MAP[w]


SAFE = re.compile(r'\b(alt|data-label|placeholder|title)="([^"]*)"')


def rename(html):
    toks = re.split(r"(<[^>]+>)", html)
    res = []
    for k, t in enumerate(toks):
        if k % 2:
            res.append(SAFE.sub(lambda a: f'{a.group(1)}="{RX.sub(fix, a.group(2))}"', t) if not t.startswith("<!--") else t)
        else:
            res.append(RX.sub(fix, t))
    return "".join(res)


out = rename(out)

# ---- post-conditions ----
ids = set(re.findall(r'<(?:section|header) class="chapter[^"]*" id="([^"]+)"', out))
hrefs = set(re.findall(r'<a href="#(c\d\d-[a-z]+)"', out))
missing = sorted(h for h in hrefs if h not in ids)
assert not missing, ("rail/toc href without a section", missing)
for mo in re.finditer(r'<!-- ===================== (\d\d) · (c\d\d-[a-z]+) ===================== -->\n<section class="chapter" id="([^"]+)"[^>]*>\n  <div class="part reveal"><div class="big-num">(\d\d)</div><div class="p-num">Chapter (\d\d)</div>', out):
    nn, mid, sid, bn, pn = mo.groups()
    assert mid == sid and nn == bn == pn == sid[1:3], mo.groups()
markers = re.findall(r"<!-- ===================== (\d\d) · ", out)
assert markers == [x[0] for x in ORDER], markers
call_ids = set(re.findall(r'<fieldset class="call(?: wordbox)?" data-id="([^"]+)"', out))
for spec in CALLS.values():
    for cid in [x.split("=")[0] for x in spec.split(",")]:
        assert cid in call_ids, ("data-calls id missing", cid)
n_calls = len(re.findall(r'<fieldset class="call" data-id=', out))
assert n_calls == 15, ("non-wordbox calls", n_calls)
plain = re.sub(r"<[^>]+>", " ", out)
left = sorted(set(m.group(0) for m in re.finditer(r"[^\s]*\b[Mm]arks?\b[^\s]*", plain)))
print("leftover mark tokens (expected: exclamation marks, 'marks an open decision', Thank you Mark, kit/marks/):", left)

print("chapters:", " ".join(f"{n}-{SLUG[n]}" for n in [x[0] for x in ORDER]))
print("non-wordbox calls:", n_calls, "| data-calls chapters:", len(CALLS))
if DRY:
    print("dry run - nothing written")
else:
    P.write_text(out, encoding="utf-8")
    print("index.html restructured to V3")
