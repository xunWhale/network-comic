# 零基础数通漫画图解验收记录

## 1. 交付文件
- 新增第四弹页面：`lab.html`（《三机串联实战：静态路由 vs OSPF 排错全解》）
- 更新系列顶栏导航：`index.html`、`arp.html`、`ospf.html`、`lab.html` 四页互通
- 更新检测脚本：`check_overlap.py`
- 留存截图：`preview-lab.png`（1440px 桌面全页）、`preview-lab-mobile.png`（390px 手机全页）

## 2. 文本重叠机检（`check_overlap.py`）
Command:
```bash
/home/fish/.venv/bin/python check_overlap.py
```

Output:
```text
[index.html 1440px] 文字块 184 个，重叠告警 0 处
[index.html 900px] 文字块 195 个，重叠告警 0 处
[index.html 390px] 文字块 206 个，重叠告警 0 处
[arp.html 1440px] 文字块 180 个，重叠告警 0 处
[arp.html 900px] 文字块 192 个，重叠告警 0 处
[arp.html 390px] 文字块 207 个，重叠告警 0 处
[ospf.html 1440px] 文字块 301 个，重叠告警 0 处
[ospf.html 900px] 文字块 328 个，重叠告警 0 处
[ospf.html 390px] 文字块 346 个，重叠告警 0 处
[lab.html 1440px] 文字块 184 个，重叠告警 0 处
[lab.html 900px] 文字块 193 个，重叠告警 0 处
[lab.html 390px] 文字块 210 个，重叠告警 0 处
```

## 3. Playwright 三档视口溢出、SVG 边界与交互验证（1440 / 900 / 390px）
- `index.html` / `arp.html` / `ospf.html` / `lab.html` 在 `1440px`、`900px`、`390px` 下均满足 `overflow_px=0`、`svg_clipped=[]`。
- `lab.html` 交互模式切换验证：
  - `ospf` -> `badge='OSPF Area 0 Full'`, `fail_opacity='0'`
  - `no-return` -> `badge='Ping 超时 · 缺回程'`, `fail_opacity='1'`
  - `no-gw` -> `badge='Ping 失败 · 无网关'`, `fail_opacity='1'`
  - `static` -> `badge='静态路由互通'`, `fail_opacity='0'`
- 桌面与手机截图拼图经 Firefox ESR 肉眼核验，拓扑节点、公式文字、代码块与四张排错卡片均无压字、无遮挡。
