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

## 5. 线上核验（GitHub Pages）
构建状态 `built`，内容提交 `4f94db4`（验收记录提交 `b45be58`）。

### 5.1 五页可达性复核（2026-11-19 08:05 实跑，下面是命令原样输出）
命令：`curl -s -o /dev/null -w '%{http_version} %{http_code} %{size_download}' https://xunwhale.github.io/network-comic/<page>`

```text
index.html       -> HTTP/2 200  42530 bytes
arp.html         -> HTTP/2 200  44690 bytes
lab.html         -> HTTP/2 200  31926 bytes
ospf.html        -> HTTP/2 200  46367 bytes
ospf-multi.html  -> HTTP/2 200  29965 bytes
```
五页均 HTTP/2 200，体积与本地文件同量级（29 KB – 47 KB），无空页、无跳 404。

### 5.2 真实读者反馈记录
| 时间 | 动作 | 结果 |
| --- | --- | --- |
| 2026-11-18 12:42 | 第五弹链接发到 QQ 群「ikun之家2.0」（并发给 e0_7 私聊） | 群内 0 回复 |
| 2026-11-18 17:05 | 第一次复查群消息 | 无回复 |
| 2026-11-19 08:06 | 第二次复查（最近 15 条） | 无回复；最后一条群消息是 e0_7 11-18 19:11 的「叮咚鸡」，与本页无关 |
| 2026-11-19 08:01 | 改用定向提问：在群里 @月月鸟，就 DR 选举判定顺序与 Area 1 出口数请他对照自己的 eNSP 拓扑验收 | 待回 |
| 2026-11-19 14:31 | 月月鸟在「ikun之家2.0」主动 @我 回复提问：「DR选举的目的是什么」 | 已于 14:32 现场拆解省邻接数 $O(n)$（2-Way 机制）与 224.0.0.6/224.0.0.5 统一泛洪/2类LSA，并追问是否因页面未讲清而问 |
| 2026-11-19 14:35 | 追问反馈 | 月月鸟回复：「噢，那没有，因为我根本没看」——**并未点开网页**，直接在群里把问题抛给我 |

结论（截至 2026-11-19 14:36）：**真实反馈为「未点击网页、直接在聊天里提问」**。这比沉默更有信息量：群友天然排斥点外链看页面，更愿意直接对话问答案；截至当前，第五弹网页尚未收到基于实际阅读页面的验收意见。

### 5.3 待办
- [ ] 月月鸟回复后，把他指出的对不上处直接改进 `ospf-multi.html`，并在本文件记下改了哪段
- [ ] 拿到第一条真实反馈后，才算这一件真正交付
