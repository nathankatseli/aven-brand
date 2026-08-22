#!/usr/bin/env python
"""Publish the AVEN brand book to GitHub Pages (nathankatseli/aven-brand, branch main, root).
  python src/publish.py --check            PII/secret gate only
  python src/publish.py -m "message"       check -> commit -> push -> poll Pages build
  python src/publish.py -m "..." --pdf     also print out/AVEN Brand Book.pdf via headless Edge after build
Public repo: the gate BLOCKS on money, percentages, company identifiers, personal numbers,
internal-plan words; WARNS on competitor/partner/tool names. Allow-list lines in src/pii_allow.txt.
"""
import re, sys, subprocess, time, json, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = "nathankatseli/aven-brand"

def _patterns():
    """BLOCK/WARN regex lists live in src/pii_patterns.txt (gitignored, never published).
    Format per line: BLOCK|WARN<TAB>regex<TAB>why"""
    pf = ROOT / "src" / "pii_patterns.txt"
    if not pf.exists():
        sys.exit("src/pii_patterns.txt missing - the gate cannot run without it")
    block, warn = [], []
    for line in pf.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        kind, rx, why = line.split("\t", 2)
        (block if kind == "BLOCK" else warn).append((rx, why))
    return block, warn


def _scan_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [f for f in out if not f.endswith((".woff2", ".png", ".pdf"))]


def gate():
    allow = set()
    af = ROOT / "src" / "pii_allow.txt"
    if af.exists():
        allow = {l.strip() for l in af.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    BLOCK, WARN = _patterns()
    blocks, warns = [], []
    for rel in _scan_files():
        p = ROOT / rel
        if not p.exists():
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if any(a in line for a in allow):
                continue
            for rx, why in BLOCK:
                if why in ("money amount", "percentage") and p.suffix in (".css", ".js"):
                    continue
                if re.search(rx, line, re.I):
                    blocks.append(f"{rel}:{n} [{why}] {line.strip()[:110]}")
            for rx, why in WARN:
                if re.search(rx, line, re.I):
                    warns.append(f"{rel}:{n} [{why}] {line.strip()[:110]}")
    for w in warns:
        print("WARN ", w)
    for b in blocks:
        print("BLOCK", b)
    print(f"gate: {len(blocks)} block(s), {len(warns)} warning(s)")
    return not blocks


def sh(*a, check=True, capture=True):
    r = subprocess.run(a, cwd=ROOT, capture_output=capture, text=True)
    if check and r.returncode != 0:
        sys.exit(f"failed: {' '.join(a)}\n{r.stderr}")
    return r.stdout.strip() if capture else ""


def publish(msg):
    if sh("git", "status", "--porcelain"):
        sh("git", "add", "-A")
        sh("git", "commit", "-q", "-m", msg)
        print("committed:", msg)
    else:
        print("nothing to commit")
    sh("git", "push", "-q")
    head = sh("git", "rev-parse", "HEAD")
    print("pushed", head[:8])
    kicked = False
    for i in range(36):
        time.sleep(10)
        try:
            b = json.loads(sh("gh", "api", f"repos/{REPO}/pages/builds/latest"))
        except SystemExit:
            continue
        st, commit = b.get("status"), (b.get("commit") or "")
        print(f"  build {st} {commit[:8]}")
        if commit == head and st == "built":
            print("LIVE: https://nathankatseli.github.io/aven-brand/")
            return True
        if commit == head and st == "errored":
            if kicked:
                sys.exit("Pages build errored twice")
            print("  errored - kicking one rebuild"); sh("gh", "api", "-X", "POST", f"repos/{REPO}/pages/builds"); kicked = True
        if i == 9 and commit != head and not kicked:
            print("  no build for HEAD yet - kicking"); sh("gh", "api", "-X", "POST", f"repos/{REPO}/pages/builds"); kicked = True
    sys.exit("timed out waiting for Pages build")


def pdf():
    out = ROOT / "out"; out.mkdir(exist_ok=True)
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    target = out / "AVEN Brand Book.pdf"
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={target}", f"file:///{(ROOT/'index.html').as_posix()}"], capture_output=True)
    print("pdf:", target, target.stat().st_size // 1024, "KB" if target.exists() else "FAILED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("-m", "--msg", default="Update brand book")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    ok = gate()
    if a.check:
        sys.exit(0 if ok else 1)
    if not ok:
        sys.exit("gate failed - fix BLOCK lines or add an allow-list entry")
    publish(a.msg)
    if a.pdf:
        pdf()
