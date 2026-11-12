"""文字重叠自检：把页面里所有「直接包着文字」的元素取出矩形，两两比对是否相交。

设计机检抓不到的问题往往就是这种：绝对定位的字压在别一行的字上，
元素本身都在、都不报警，但人眼看是糊成一团。
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

URL = pathlib.Path(__file__).with_name("index.html").as_uri()

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
    // 用 Range 取这条文字自己的行盒，而不是父元素的盒子，
    // 否则父块会把子文字全包进去，全是假重叠。
    idx += 1;
    if (!(el.dataset.ovl)) el.dataset.ovl = String(idx);
    // 最近的块级祖先：同一个块里的相邻两行属于正常行距，不该报重叠
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
      out.push({ id: idx, own: idx, text: t.slice(0, 20), parent: parentId, x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height });
    }
  }
  return out;
}
"""

def intersects(a, b):
    return (
        a["x"] < b["x"] + b["w"]
        and b["x"] < a["x"] + a["w"]
        and a["y"] < b["y"] + b["h"]
        and b["y"] < a["y"] + a["h"]
    )


def area(r):
    return r["w"] * r["h"]


def overlap_area(a, b):
    w = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    h = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return max(0, w) * max(0, h)


def main(width):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": width, "height": 1000})
        pg.goto(URL, wait_until="networkidle")
        pg.wait_for_timeout(400)
        boxes = pg.evaluate(JS)
        b.close()

    fails = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a["own"] == b["own"]:  # 同一个文字节点的不同行盒，不算重叠
                continue
            if a["parent"] == b["parent"]:  # 同一段落里上下两行的字身框，属于正常行距
                continue
            if not intersects(a, b):
                continue
            smaller = min(area(a), area(b))
            if smaller <= 0:
                continue
            # 同类元素的父子重叠不可避免，只报「不小比例被盖住」的
            ratio = overlap_area(a, b) / smaller
            if ratio > 0.12:
                fails.append((round(ratio, 2), a["text"], b["text"], a["y"], b["y"]))

    print(f"[{width}px] 文字块 {len(boxes)} 个，重叠告警 {len(fails)} 处")
    for r, t1, t2, y1, y2 in sorted(fails, reverse=True)[:15]:
        print(f"  {r:.0%}  「{t1}」(y={y1:.0f})  ×  「{t2}」(y={y2:.0f})")
    return 1 if fails else 0


if __name__ == "__main__":
    rc = 0
    for w in (1440, 900, 390):
        rc |= main(w)
    sys.exit(rc)
