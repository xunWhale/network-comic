"""检查 index.html 与 arp.html 在三档宽度下的文字行盒重叠。"""
import pathlib
import sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
PAGES = ("index.html", "arp.html", "ospf.html", "lab.html")
WIDTHS = (1440, 900, 390)

JS = r"""
() => {
  const out = [];
  let idx = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent.replace(/\s+/g, " ").trim();
    if (t.length < 2) continue;
    const el = n.parentElement;
    if (!el) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === "hidden" || cs.display === "none") continue;
    if (parseFloat(cs.opacity) < 0.05) continue;
    idx += 1;
    if (!(el.dataset.ovl)) el.dataset.ovl = String(idx);
    let blk = el;
    while (blk && blk !== document.body) {
      const d = getComputedStyle(blk).display;
      if (d !== "inline" && d !== "contents") break;
      blk = blk.parentElement;
    }
    if (blk && !blk.dataset.ovlp) blk.dataset.ovlp = "b" + idx;
    const parentId = blk ? blk.dataset.ovlp : "x";
    const range = document.createRange();
    range.selectNodeContents(n);
    for (const r of range.getClientRects()) {
      if (r.width < 2 || r.height < 2) continue;
      out.push({ id: idx, own: idx, text: t.slice(0, 28), parent: parentId, x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height });
    }
  }
  return out;
}
"""

def intersects(a, b):
    return a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]

def area(r):
    return r["w"] * r["h"]

def overlap_area(a, b):
    w = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    h = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return max(0, w) * max(0, h)

def main(page, width, browser):
    pg = browser.new_page(viewport={"width": width, "height": 1000})
    pg.goto((ROOT / page).as_uri(), wait_until="networkidle")
    pg.wait_for_timeout(400)
    boxes = pg.evaluate(JS)
    pg.close()
    fails = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a["own"] == b["own"] or a["parent"] == b["parent"]:
                continue
            if not intersects(a, b):
                continue
            smaller = min(area(a), area(b))
            if smaller <= 0:
                continue
            ratio = overlap_area(a, b) / smaller
            if ratio > 0.12:
                fails.append((round(ratio, 2), a["text"], b["text"], a["y"], b["y"]))
    print(f"[{page} {width}px] 文字块 {len(boxes)} 个，重叠告警 {len(fails)} 处")
    for r, t1, t2, y1, y2 in sorted(fails, reverse=True)[:15]:
        print(f"  {r:.0%} 「{t1}」(y={y1:.0f}) × 「{t2}」(y={y2:.0f})")
    return len(fails)

def run():
    total = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for page in PAGES:
            for width in WIDTHS:
                total += main(page, width, browser)
        browser.close()
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(run())
