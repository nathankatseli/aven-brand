"""Contact sheet of the avenue masters (inline SVG) -> out/_sheet.html + out/sheet.png"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
XMLNS = '<svg xmlns="http://www.w3.org/2000/svg" '


def sheet(pattern="[23]*.svg", cols=4, cell=300, out="sheet", src=None):
    files = sorted(pathlib.Path(src or ROOT / "src" / "marks").glob(pattern))
    cells = []
    for p in files:
        s = p.read_text(encoding="utf-8").replace("<svg ", XMLNS, 1)
        cells.append(f"<figure>{s}<figcaption>{p.stem}</figcaption></figure>")
    rows = -(-len(files) // cols)
    html = (f"<style>body{{margin:0;background:#fff;font:11px sans-serif}}.g{{display:grid;grid-template-columns:repeat({cols},{cell}px);gap:8px;padding:8px}}"
            f"figure{{margin:0;border:1px solid #ddd;background:#fbfcfa}}svg{{width:{cell}px;height:auto;display:block}}figcaption{{padding:4px 8px;color:#555}}</style>"
            f"<div class='g'>{''.join(cells)}</div>")
    (ROOT / "out" / f"_{out}.html").write_text(html, encoding="utf-8")
    w = cols * (cell + 8) + 16
    h = rows * (int(cell * 152 / 210) + 30) + 16
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={ROOT / 'out' / (out + '.png')}", f"file:///{(ROOT / 'out' / ('_' + out + '.html')).as_posix()}"],
                   capture_output=True)
    print(f"{len(files)} marks -> out/{out}.png ({w}x{h})")


if __name__ == "__main__":
    # usage: python src/sheet.py [pattern] [out-name] [src-dir]
    a = sys.argv[1:]
    sheet(a[0] if a else "[23]*.svg", out=a[1] if len(a) > 1 else "sheet", src=a[2] if len(a) > 2 else None)
