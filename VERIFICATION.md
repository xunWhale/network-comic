# 零基础数通漫画图解验收记录

## 1. 文本重叠机检（`check_overlap.py`）

Command:
```bash
/home/fish/.venv/bin/python check_overlap.py
```

Output:
```text
[index.html 1440px] 文字块 183 个，重叠告警 0 处
[index.html 900px] 文字块 194 个，重叠告警 0 处
[index.html 390px] 文字块 205 个，重叠告警 0 处
[arp.html 1440px] 文字块 179 个，重叠告警 0 处
[arp.html 900px] 文字块 191 个，重叠告警 0 处
[arp.html 390px] 文字块 206 个，重叠告警 0 处
[ospf.html 1440px] 文字块 300 个，重叠告警 0 处
[ospf.html 900px] 文字块 327 个，重叠告警 0 处
[ospf.html 390px] 文字块 345 个，重叠告警 0 处
```

## 2. 视口溢出与 SVG 边界检查（Playwright Chromium）

```text
[width=1440] overflow_px=0 svg_clipped=[]
[width=900] overflow_px=0 svg_clipped=[]
[width=390] overflow_px=0 svg_clipped=[]
[interactive] stage='Full · 全网互通' route='R3 学到 OSPF 1.1.1.1/32 (下一跳 192.168.23.2)'
```

全页截图已留存为 `preview-ospf.png`。
