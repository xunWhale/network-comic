# 零基础数通漫画图解验收记录

## 1. 交付文件
- 新增第五弹：`ospf-multi.html`（《多区域 OSPF：ABR、骨干区与 DR 选举》），源自真实 eNSP 多区域拓扑提问
- 五页顶栏导航互通：`index.html`、`arp.html`、`ospf.html`、`lab.html`、`ospf-multi.html`
- 检测脚本 `check_overlap.py` 覆盖 5 页
- 截图：`preview-ospf-multi.png`（1440px 全页）、`preview-ospf-multi-mobile.png`（390px 全页）

## 2. 文本重叠机检（`check_overlap.py`）
```text
[index.html 1440px] 文字块 185 个，重叠告警 0 处
[index.html 900px] 文字块 196 个，重叠告警 0 处
[index.html 390px] 文字块 207 个，重叠告警 0 处
[arp.html 1440px] 文字块 181 个，重叠告警 0 处
[arp.html 900px] 文字块 193 个，重叠告警 0 处
[arp.html 390px] 文字块 208 个，重叠告警 0 处
[ospf.html 1440px] 文字块 302 个，重叠告警 0 处
[ospf.html 900px] 文字块 329 个，重叠告警 0 处
[ospf.html 390px] 文字块 347 个，重叠告警 0 处
[lab.html 1440px] 文字块 185 个，重叠告警 0 处
[lab.html 900px] 文字块 194 个，重叠告警 0 处
[lab.html 390px] 文字块 211 个，重叠告警 0 处
[ospf-multi.html 1440px] 文字块 178 个，重叠告警 0 处
[ospf-multi.html 900px] 文字块 180 个，重叠告警 0 处
[ospf-multi.html 390px] 文字块 202 个，重叠告警 0 处
```

## 3. Playwright 三档视口溢出、SVG 边界与交互验证
```text
[index.html 1440] overflow=0 clipped=[]
[index.html 900] overflow=0 clipped=[]
[index.html 390] overflow=0 clipped=[]
[arp.html 1440] overflow=0 clipped=[]
[arp.html 900] overflow=0 clipped=[]
[arp.html 390] overflow=0 clipped=[]
[ospf.html 1440] overflow=0 clipped=[]
[ospf.html 900] overflow=0 clipped=[]
[ospf.html 390] overflow=0 clipped=[]
[lab.html 1440] overflow=0 clipped=[]
[lab.html 900] overflow=0 clipped=[]
[lab.html 390] overflow=0 clipped=[]
[mode=area0] badge='Area 0 视角' mark_opacity='0'
[mode=area1] badge='Area 1 视角' mark_opacity='0'
[mode=wrong] badge='跨区中断' mark_opacity='1'
[mode=all] badge='三网段互通' mark_opacity='0'
[ospf-multi.html 1440] overflow=0 clipped=[]
[ospf-multi.html 900] overflow=0 clipped=[]
[ospf-multi.html 390] overflow=0 clipped=[]
ALL PAGE CHECKS PASSED
```

## 4. 目视核验
桌面全页与 390px 手机全页各切两张拼图，在 Firefox ESR 中肉眼逐段检查：
- hero 文案、四个模式按钮、状态行排布正常，无压字
- 拓扑图内 Area 0 / Area 1 虚线框、五个路由器节点、三台 PC、两条网段标签均无重叠或越界
- 三部分正文（两条铁律 / 完整配置 / DR-BDR）代码块横向可滚动，卡片间距一致
- 手机端导航折成多行但仍在一屏内，无横向滚动
