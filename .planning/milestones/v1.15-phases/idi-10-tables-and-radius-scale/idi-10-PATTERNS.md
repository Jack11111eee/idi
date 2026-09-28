# Phase 10: 表格重做与圆角刻度收敛 - Pattern Map

**Mapped:** 2026-09-27
**Files analyzed:** 4 个文件族（1 个产品文件 + 1 个新门 + 2 类产物），本阶段**零新增应用文件**
**Analogs found:** 4 / 4（每一族都有 exact 或 role-match 的同仓库先例）

> **本阶段的形状（决定了这张图为什么这么短）。** 这是一个**纯 CSS 阶段**：唯一的产品文件是
> `frontend/style.css`，且两处改动都是**改写既有声明**（表格规则就地改写 / 令牌删除 + 2 处消费者改归属）。
> 没有新模块、没有新分层、没有新接口 —— 所以「找同类构件」的答案全部落在**同一个文件的既有先例**上。
> 真正需要跨文件抄的只有一件事：**新运行时门的骨架**（`scripts/check-09-idi09-validation.py`）。

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/style.css` §`.markdown-body table` / `th, td`（`:1081-1086`） | config（stylesheet，声明层） | transform（声明式层叠 → 渲染几何） | `frontend/style.css:752-775`（Phase 9 就地改写 `#doc-panel` 的 `border-left` → `border`）+ `:728-750`（就地扩写 `#main-pane > section`） | **exact**（同文件、同手法、上一阶段刚落地） |
| `frontend/style.css` §`--radius-lg` 声明（`:405`）+ 2 处消费者（`:1173` / `:1202`） | config（stylesheet，令牌层） | transform（令牌删除 + 引用改归属） | `frontend/style.css:402-406`（圆角刻度块本身）+ `:334-336`（`--shadow-card` 用户裁定值重新登记） | **role-match**（同是「令牌层动刀」，但先例是改值，本阶段是删名 + 搬引用） |
| `frontend/style.css` §PAIR 清单注释（`:552-560` 附近 + 规模台账 `:466-511`） | config（清单注释，机器可解析） | transform（注释即契约，被 `check-02` 正则消费） | `frontend/style.css:513-550`（Phase 9 页面地面重算登记段） | **exact** |
| `scripts/check-10-idi10-validation.py`（**新建**） | test（运行时门） | request-response（真实浏览器驱动自起 uvicorn） | `scripts/check-09-idi09-validation.py` | **exact** |
| `.planning/phases/idi-10-tables-and-radius-scale/screenshots/*.png`（**新建**） | artifact | file-I/O | `.planning/phases/idi-09-card-containers/screenshots/`（5 张 1440×900） | **exact** |
| `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/*.log`（**新建**） | artifact | file-I/O | `.planning/phases/idi-09-card-containers/gate-logs/`（9 个日志） | **exact** |
| **1** 份 VERIFICATION 报告（`idi-09`）的**重新验证**（modify，非刷新）—— 见文末裁定块:「10 份覆盖，1 份可执行」 | test（报告） | file-I/O | `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 `re_verification:` 块 | **exact** |

---

## Pattern Assignments

### `frontend/style.css` §`.markdown-body table / th / td`（config, transform）

**Analog A（就地改写既有声明 —— 本阶段的主手法）：** `frontend/style.css:752-775`

这是 Phase 9 亲手留下的**同型先例**，也是 CONTEXT / ROADMAP 逐字点名要照抄的那一个：改写既有声明时**就地改写**，不追加覆盖规则。

**承重注释块**（`:752-759`，注意它是「为什么就地改写」的论证，不是装饰）：
```css
/* 右:文档面板(基准宽由 --doc-panel-w 控制;收起态为 48px 竖条)

   Phase 9:与左栏**同族卡片** —— 同底色令牌 / 同边界令牌 / 同圆角令牌 / 同阴影令牌
   (CARD-02)。原 `border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代,故这里
   是就地改写那条声明,不是追加一条 `border` 覆盖它(留下一条已死的 border-left 会让
   注释与代码互相矛盾)。
   `overflow-y: auto` 是**承重的滚动契约**,不得删除:它是右列的滚动者,L-1 的 sticky
   表头依赖 #doc-panel 仍是最近的可滚祖先。 */
```

**被改写的那一条声明**（`:765`，`border-left` → `border`，其余声明逐字不动）：
```css
#doc-panel {
  flex: 0 0 var(--doc-panel-w);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  border: 1px solid var(--color-border);   /* ← HEAD 是 border-left: 1px solid var(--color-border-subtle); */
  background: var(--color-surface-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  min-width: 0;
}
```

**本阶段的对应落点**（`frontend/style.css:1081-1086`，HEAD 原文，逐字）：
```css
.markdown-body table { border-collapse: collapse; }
.markdown-body th, .markdown-body td {
  border: 1px solid var(--color-border);
  padding: var(--space-1) var(--space-2-5);
  font-size: var(--text-base);
}
```
⇒ 按 Analog A 的手法：把 `border: 1px solid var(--color-border);` **就地改写成**
`border: none; border-bottom: 1px solid var(--color-border-subtle);`（或等价形态），
**不是**追加一条 `border: none` 覆盖它。`padding` 与 `font-size` 两行**逐字保留**
（`font-size` 被 `check-05-ui-uat.py:1126` 的活断言锁死，见下方 Shared Patterns）。

**Analog B（就地扩写既有规则体 —— 给 `th` 加底色用的就是这一手）：** `frontend/style.css:728-750`

Phase 9 给 `#main-pane > section` 加四条声明的做法，是「追加到既有规则体内、选择器文本与源码顺序逐字不变」的落地形态：

```css
/* 左栏四个面板的卡片语言(Phase 9 / CARD-01 / CARD-02)。就地扩写既有规则体,
   选择器文本与源码顺序逐字不变 —— 硬规则 3「追加,不重排」的落地形态。 */
#main-pane > section {
  width: 100%;                              /* ← HEAD 已有的两条,逐字保留 */
  max-width: 768px;
  background: var(--color-surface-card);    /* ← 本阶段新增的四条 */
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
}
```

⇒ 给 `.markdown-body th` 新增 `background: var(--color-surface);` 时，若需要**拆开**
`:1082` 的并集选择器 `.markdown-body th, .markdown-body td`，注意那是**重排风险区**：
CONTEXT 的编辑纪律明写「追加，不重排（至少一对等特异性规则由源码顺序决定）」。稳妥形态是
**保留并集选择器逐字不动**，只在其后追加一条 `.markdown-body th { background: …; }`
（新增规则块只能**追加到既有规则之后**，不得插到既有规则之前）。

**表头底色的档位依据**（必须写进注释，否则会被读成任选）—— `frontend/style.css:73-116` 的 role-bands 段与 `:466-511` 的清单头部：

```
Radix's 12 steps are read as: 1-2 ground / 3-5 component surface / 6-8
border / 9-10 solid fill / 11-12 text.
```
`--color-surface: var(--radix-gray-2);`（`:208`，gray-2 = `#f9f9f9` = `rgb(249,249,249)`）正是
Phase 9 三级刻度里的「内陷面」档（`gray-3 页面 < gray-2 内陷面 < 白卡片`）。**不得**改落
`--color-surface-sunken`（gray-3，那是页面档）或 `--radix-gray-4`（围栏外不得引用 tier-1 原语，
`check-01` 会 FAIL）。

---

### `frontend/style.css` §`--radius-lg` 删除 + 2 处消费者改归属（config, transform）

**Analog（令牌层动刀）：** `frontend/style.css:402-406`

```css
  /* Radius — four values. */
  --radius-sm: 8px;
  --radius-md: 10px;
  --radius-lg: 28px;
  --radius-pill: 999px;
```

⇒ 删掉 `--radius-lg: 28px;` 一行后，上方注释 `/* Radius — four values. */` 变成**假陈述**
（`check-01` 不数注释，但 CONTEXT 的编辑纪律要求注释与代码不互相矛盾）⇒ 该注释须同步改为
`/* Radius — three values. */`。这是 Phase 9 改写 `#doc-panel-header` 注释时的同一纪律
（`:792-810` 那段注释被逐句重写过）。

**消费者 1 —— `.chat-user`（`frontend/style.css:1171-1177`，HEAD 原文）：**
```css
.chat-user {
  align-self: flex-end;
  border-radius: var(--radius-lg);        /* ← 改为 var(--radius-md) —— 本阶段唯一外观真变的消费者 */
  background: var(--color-surface-user);
  color: var(--color-text);
  border-bottom-right-radius: var(--radius-sm);   /* ← 8px 尖角(气泡尾巴),逐字保留不动 */
}
```

**消费者 2 —— `#chat-input-row input`（`frontend/style.css:1197-1205`，HEAD 原文）：**
```css
#chat-input-row input {
  flex: 1;
  min-height: 52px;                       /* ← 52px 高是「28px 早被 UA 钳到 26px」这条算术的自变量 */
  padding: var(--space-1-5) var(--space-2-5);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);        /* ← 改为 var(--radius-pill) —— 外观零变化 */
  box-shadow: var(--shadow-composer);
  font-size: var(--text-md);
}
```

**为什么两处去向不同（承重点，写进注释，否则会被后人「统一」掉）：**

| 消费者 | 现值 | 改为 | 依据 |
|---|---|---|---|
| `.chat-user` | `var(--radius-lg)` | `var(--radius-md)` | 它**真的是**大圆角气泡；28px → 10px 是收进卡片档，外观**真变** |
| `#chat-input-row input` | `var(--radius-lg)` | `var(--radius-pill)` | `min-height: 52px` 下 28px 早被 UA 钳到 26px ⇒ 它**实际就是**一个胶囊，改记 `--radius-pill` 是**如实登记** |

⚠️ **一律改成 `--radius-md` 会让输入框外观真的变化**（胶囊 → 10px 圆角矩形），那是用户没选的档位
（ROADMAP Pitfalls 第 1 条）。

⚠️ **「28px 会被钳成胶囊」是算术推断，不是测量。** 判据必须取收敛**前后**的真实
`getComputedStyle` 读数并排比对（ROADMAP SC 4 / Pitfalls 第 2 条）。

**令牌删除的判据（两个独立量，别只数一个）** —— 本机 `grep` 是 **ugrep**，`-` 算词字符，`\b` 对含连字符的令牌名不可靠：
- `grep -c -- '--radius-lg' frontend/style.css` == **0**（全文，含散文注释）
- 围栏内 `--radius-lg` 声明数 == **0**
- `grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l` == **0**

HEAD 实测基线（规划期实测，执行器须复核）：`--radius-lg` 全文 **3 处** —— `:405`（声明）+ `:1173` + `:1202`（消费者）。

**不得碰**：`#doc-panel-header` 的 `border-radius: 0;`（`frontend/style.css:809`）—— 它是**显式零值**、
不消费任何 `--radius-*` 令牌，带一段 2026-09-26 的论证（`:799-804`），与本阶段的收敛**无关**，一字不动。
**不得删** `--radius-md` —— `scripts/check-09-idi09-validation.py:136` / `:186` **动态解析**它做卡片断言
（令牌相对，改值不破；**删该令牌会破**）。

---

### `frontend/style.css` §PAIR 清单注释（config, transform）

**Analog（清单注释的机器可解析契约）：** `frontend/style.css:466-476`

```css
  /* ---- Contrast pair manifest (CHECK-02) -----------------------------------
     Every entry below names two tokens declared in this fence. The checker
     scripts/check-02-contrast.py reads this manifest and fails loudly on a name
     that is not declared here, so the manifest and the token block cannot drift
     apart. Thresholds: TEXT 4.5:1, NON-TEXT 3:1; an optional @<alpha> suffix on
     TEXT composites the foreground over the background before measuring. The
     single ordering entry asserts a strict ratio ordering on one shared ground.
     Token names only — never hex.
     Re-enumerated for the Radix rewrite (Phase 04.1 D-15): every entry below is a
     combination that actually renders. Decorative separators are deliberately
     absent — SC 1.4.11 does not apply to a border that identifies nothing.
```

**⚠️ 围栏内注释的硬约束（`scripts/check-02-contrast.py:27`）：**
```python
DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")
```
`DECL_RE` 扫的是**围栏全文（含注释）**。⇒ **围栏内注释里不得出现「令牌名 + 冒号」**：
写 `--radix-gray-12: …` 会被当成一条值不可解析的声明而 **FAIL**。本阶段若要在清单注释里
登记表格相关的事实，只能用行文指代令牌名（`--color-surface`），**不得写成声明形态**。

**本阶段要复用的既有 PAIR 条目**（`frontend/style.css:552-560`，**早已登记，预期零新增**）：
```css
  /* body text on its four real grounds (page, panel, sunken, amber container) */
  /* PAIR --color-text ON --color-surface-page TEXT */
  /* PAIR --color-text ON --color-surface TEXT */        /* ← :554，表头文字色在新绘制面上的这条 */
  /* PAIR --color-text ON --color-surface-sunken TEXT */
  ...
```
规划期实测（`python3 scripts/check-02-contrast.py`）：
```
PASS  15.48  --color-text on --color-surface
PASS: 0 failures
```
表头文字色是 `.markdown-body th` 从 `.markdown-body`（`:1060-1063`）继承的 `--color-text`
（`:119` = `var(--radix-gray-12)`），新绘制面 `--color-surface` = gray-2 ⇒ **该配对已覆盖**。
但 ROADMAP SC 2 明写：**须以 `check-02` 的实际输出证实，不得以「我认为已覆盖」结案** ⇒
SUMMARY 里贴 `PASS  15.48  --color-text on --color-surface` 这一行原文。

**装饰性边界的判据（已有登记，本阶段须显式引用而非重新发明）——** `frontend/style.css:94-96`：
```
       · border band 6-8 → step 9 for --color-border-strong. Nothing in 6-8
         clears SC 1.4.11's 3:1 on any surface: gray-6 1.34, gray-7 1.49,
         gray-8 1.82 on --color-surface. This border is the control boundary —
         the only thing identifying a text input's edge — so it has to leave the
         band. ... The other
         three borders stay in band 6-8: they are decorative, and SC 1.4.11 does
         not apply to a border that identifies nothing.
```
以及 `:475-476`：`Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing.`

⇒ 表格的行间分隔线与表头下边线**不标识任何东西**（它们是视觉分组的装饰），故**不需 NON-TEXT 条目**。
ROADMAP 要求「此判断须在计划里显式论证，不留空白」⇒ 计划与 SUMMARY 都要**引用上面两处既有登记**，
不得只写一句「不需要」。

**清单规模台账**（`frontend/style.css:477-511`，六个历史数字 `24 / 34 / 43 / 47 / 50 / 53`）：
本阶段**零 PAIR 增删**（表格表头底色已覆盖、分隔线不需条目、圆角不涉色）⇒
`grep -o '/\* PAIR' frontend/style.css | wc -l` 仍为 **53**，`grep -o '/\* ORDER' frontend/style.css | wc -l` 仍为 **1**。
**不得**改写那六个历史数字，也**不得**把 Phase 10 混进那串数字（与 Phase 9 plan 02 的纪律逐条一致）。

---

### `scripts/check-10-idi10-validation.py`（test, request-response）

**Analog:** `scripts/check-09-idi09-validation.py`（552 行，本阶段要抄的**唯一**跨文件先例）

**为什么另开一个文件（docstring 的第一段就是这条论证，`:3-16`）：**
```python
"""check-09-idi09-validation.py — Phase 9「卡片容器化与页面底色下沉」的运行时门。

为什么另开一个文件
    既有五条门里**没有任何一条**断言五个容器的 `background` / `border` /
    `border-radius` / `box-shadow`:
      - `check-01-token-conformance.sh`  只数围栏外的裸 hex 与 tier-1 原语引用
      ...
    需求 CARD-01 / CARD-02 / CARD-03 的渲染判据在本文件之前**零自动化覆盖** ——
    本文件补的正是这条缝。全部断言是真实浏览器里的 `getComputedStyle` 读数,
    不是源码文本匹配:卡片是**画出来**的,文本里写着 `background` 不等于它真的生效。
```
⇒ Phase 10 版本的第一段必须给出**同型的实测论证**：规划期已 grep 全部 7 个门 + 2 个探针，
**没有任何一条断言表格的边框 / 底色 / 布局**（唯一接触点是 `check-05-ui-uat.py:1126` 的
`td font-size`，断言的不是本阶段要改的属性）；圆角侧 `check-09:136/:186` 动态解析
`--radius-md`、`check-06-idi05-validation.py:224` 只经 `info()` 打印不断言 ⇒ 表格重做与
`--radius-lg` 删除的渲染判据**零自动化覆盖**。

**模块级设施的复用形态（`:51-93`，照抄这一手，不要重写服务生命周期）：**
```python
from __future__ import annotations
import argparse, importlib.util, re, shutil, struct, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK05 = ROOT / "scripts" / "check-05-ui-uat.py"

def load_check05():
    """把 check-05 当模块加载(文件名含连字符,不能用 import)。"""
    spec = importlib.util.spec_from_file_location("check05_ui_uat", CHECK05)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c05 = load_check05()
ok = c05.ok
ok_true = c05.ok_true
blocked = c05.blocked
info = c05.info
read_style = c05.read_style
resolve_color = c05.resolve_color
resolve_token = c05.resolve_token
```

**「两侧都写死」的令牌级断言形态（`:86-91` + `:140-143`）—— 本阶段删令牌时这一手是承重的：**
```python
# 用户裁定值(D-9-3)。字面量写在这里,是因为本断言的用途正是「运行时读到的值等于
# 用户裁定的那个值」—— 若两侧都从同一个令牌解析,改坏令牌值也照样 PASS。
SHADOW_CARD_LITERAL = "0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)"
CARD_WHITE = "rgb(255, 255, 255)"
...
ok(item, "c1 [令牌] --color-surface-card 解析为白", CARD_WHITE, card,
   note="令牌级断言:两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿")
```
⇒ Phase 10 对应写法：`--color-surface` 解析值写死为 `"rgb(249, 249, 249)"`（gray-2），
**同时**用 `resolve_color("--color-surface")` 做等值复核 —— 与 `check-09` 的 `c3` 同型。

**元素读数的 BLOCKED 纪律（`:145-171`，每个 style.css 计划都必须带至少一项运行时验证）：**
```python
    for sel in LEFT_SECTIONS:
        bg = read_style(page, sel, "background-color")
        ...
        if None in (bg, tl_radius, bw, bs, shadow):
            blocked(item, f"[p1] {sel} 五个读数可读", "5 个非 None 读数",
                    f"{bg} / {tl_radius} / {bw} / {bs} / {shadow}", "元素/选择器不存在")
            continue
        ok(item, f"[p1] {sel} 计算底色 == var(--color-surface-card)", card, bg, ...)
```
⇒ **元素读不到时走 `blocked()`，绝不记 PASS。** 表格探针的宿主建议沿用
`check-05` 的既有形态：`#draft-content td`（`:1126` 用的就是它）/ `#round-doc` 等
`MARKDOWN_HOSTS`（`check-05-ui-uat.py:993`）。

**CLI / 退出码 / 汇总（`:477-548`，逐字照抄这个形状）：**
```python
ITEMS = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}

def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="Phase 9 卡片语言的运行时门")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:c1 / c2 / c3 / c4 / c5(可重复,或逗号分隔)")
    ap.add_argument("--screenshot", default=None, metavar="DIR",
                    help="遍历 check-05 的 5 个样本,每个样本出一张 1440x900 整窗截图到 DIR")
    ap.add_argument("--keep", action="store_true", help="保留临时工作目录供排查")
    return ap.parse_args()
```
```python
    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-09-gate-"))
    ...
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
```
```python
    print(f"item {i}: {v.upper()}  ({len(rows)} 条断言,{fails} FAIL,{blocks} BLOCKED)")
    ...
    code = 1 if any_fail else (2 if any_blocked else 0)
    print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)", flush=True)
    return code
```
退出码语义：**0 = 全 pass；1 = 至少一条 FAIL；2 = 无 FAIL 但至少一条 BLOCKED**（与 check-05 一致）。

**浏览器路线（`:47-49` 的实测结论，不是偏好）：**
```
    固定走 Playwright 自带 chromium + 无头(与 check-06 同款)。本机 `channel="chrome"`
    + headless 会 CDP 挂死(见 check-05 文件头的实测记录),故本文件不提供 `--browser`。
```
⇒ 新门**不要**提供 `--browser` 参数，固定 `pw.chromium.launch(headless=True)`（bundled）。

**截图函数（`:455-474`，本阶段要取到至少两张机器可解析表）：**
```python
def run_screenshots(page, out_dir, tmp_root):
    out_dir.mkdir(parents=True, exist_ok=True)
    for state in c05.STATES:                      # ["p1","p12","p3","checking","archive"]
        proj = c05.make_fixture(state, tmp_root)
        c05.enter_project(page, proj)
        path = out_dir / f"{state}.png"
        page.screenshot(path=str(path))
        width, height = png_size(path)
        ok_true(item, f"shot [{state}] 截图落盘且为 1440x900",
                width == 1440 and height == 900, "1440x900", f"{width}x{height}")
```
`png_size()`（`:111-120`）读 PNG 的 IHDR 取宽高 —— 出图断言是**逐张**的，不是「有文件就算」。

**命名：** `scripts/` 现有 `check-01…check-07` + `check-09`（**无 check-08**）⇒ `check-10-idi10-validation.py` 名字空闲。

**既有门中唯一会被本阶段触碰的断言**（`scripts/check-05-ui-uat.py:1126-1127`，**不得改它**）：
```python
    ok(item, "[p1] .markdown-body td font-size == var(--text-base)", base_size,
       read_style(page, "#draft-content td", "font-size"))
```
它断言的**不是**本阶段要改的属性，且期望侧由 `resolve_token` 运行时解析 ⇒ **值层不改就恒过**。
⇒ **本阶段不得碰 `td` 的 `font-size`。**

**L-2 三宽度溢出诊断的复跑面**（`scripts/check-05-ui-uat.py:1630-1637` 的 `WIDE_MD` = 一张 12 列表
+ 一个 240 字符不可断 token；断言在 `:2290-2340` 的 item 8）：
```python
WIDE_MD = (
    "| " + " | ".join(f"列{c}" for c in range(1, 13)) + " |\n"
    + "| " + " | ".join("---" for _ in range(12)) + " |\n"
    + "| " + " | ".join("单元格内容" for _ in range(12)) + " |\n\n"
    + "不可断长 token:" + ("a" * 240) + "\n"
)
```
它断言的是**文档级 `scrollWidth`** 与 `#doc-panel` 的**实测宽 vs 声明上界**
（`clamp(340px, 30vw, 480px)`）⇒ 去掉竖线只会让表更窄、方向安全，但**必须复跑**（不是推断，是实测）。

---

### `.planning/phases/idi-10-tables-and-radius-scale/screenshots/*.png`（artifact, file-I/O）

**Analog:** `.planning/phases/idi-09-card-containers/screenshots/`

磁盘实测该目录恰含 **5 张**，与 `check-05` 的 `STATES = ["p1", "p12", "p3", "checking", "archive"]` 逐项一一对应：
```
archive.png  checking.png  p1.png  p12.png  p3.png
```
规格 **1440×900** 整窗截图（`check-09` 的 `run_screenshots` 逐张断言宽高）。
ROADMAP Deliverables 要求本阶段「含至少一个渲染出三种表格的样本」，SC 1 要求
「三张机器可解析表（批注回应表 / 覆盖维度表 / 未决问题清单）在截图里取到至少两张作为证据」。

---

### `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/*.log`（artifact, file-I/O）

**Analog:** `.planning/phases/idi-09-card-containers/gate-logs/`
```
check-02.log            check-05-full.log       check-06-idi05-validation.log
check-07-idi08-validation.log                   check-09-shot.log
probe-05-resolve-color.log                      probe-07-focus-composite.log
pytest.log              static-gates.log
```
⇒ 一个门一个日志文件，文件名即门的名字。ROADMAP Deliverables 要求「五条浏览器门的复跑记录
（`check-05` / `check-06` / `check-07` / `probe-05` / `probe-07`）与四个静态门结果」。

---

### 6 份 VERIFICATION 报告的**重新验证**（test 报告, file-I/O）

**Analog:** `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 frontmatter

```yaml
---
phase: idi-09-card-containers
verified: 2026-09-26T15:20:00Z
status: passed
score: 24/24 must-haves verified
covered_files:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-09-idi09-validation.py
covered_digest: "v1:sha256:6e811a1122c2e6d5c63308554a39c5d2d8dce462abef73847f0c7be39e2bb89e"
behavior_unverified: 0
re_verification:
  previous_status: passed
  previous_score: 21/21
  gaps_closed: []
  gaps_remaining: []
  regressions: []
---
```

**同型正文（`idi-09-VERIFICATION.md:29-40`，这是「重新验证 vs 刷新指纹」的论证模板）：**
```markdown
## Why this is a re-verification, and what changed

The previous report (`status: passed`, 21/21) was **stale by real content change**, not by a
bookkeeping edit. Two of its `covered_files` were deliberately modified after it was written:
...
**This is a ruling, not a regression.** The old values are superseded; where this report's numbers
differ from the previous report's pinned literals, the difference IS the ruling.
```

⇒ **处置法是「以 HEAD 内容重新验证」，不是「刷新指纹」** —— 内容确实变了，刷新等于断言
「自验证以来覆盖输入无变化」，那是不实陈述（CONTEXT §「最高连带成本」/ ROADMAP Pitfalls）。

**⚠️ 规划期实测的口径差（必须转告 planner —— 别按文档的「6」直接开工）：**

CONTEXT 与 ROADMAP 都写 **6 份**（`idi-04` / `idi-04.1` / `idi-05` / `idi-06` / `idi-07` / `idi-09`）。
规划期在磁盘上**精确**核对 `covered_files` frontmatter（用 `awk` 只取 frontmatter，不是全文 grep），
实测 `status: passed` 且 `covered_files` 逐行含 `  - frontend/style.css` 的报告有 **10 份**：

| # | 报告 | status | 是否在 ROADMAP 的「6 份」名单内 |
|---|---|---|---|
| 1 | `.planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md` | passed | ❌（v1.13 归档） |
| 2 | `.planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md` | passed | ❌（v1.13 归档） |
| 3 | `.planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md` | passed | ❌（v1.13 归档） |
| 4 | `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | passed | ✅ |
| 5 | `.planning/milestones/v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` | passed | ✅ |
| 6 | `.planning/milestones/v1.14-phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md` | passed | ✅ |
| 7 | `.planning/milestones/v1.14-phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` | passed | ✅ |
| 8 | `.planning/milestones/v1.14-phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` | passed | ✅ |
| 9 | `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` | passed | ✅ |
| 10 | `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md` | passed | ❌（quick 报告） |

四份都带 `covered_digest`（`v1:sha256:…`）⇒ 技术上都会因 `frontend/style.css` 变更而 stale。
**但这不等于「都要重验」**：v1.13 三份在**已冻结并归档的里程碑**下，quick 那份是 quick 的产物 ——
两者是否在收口流程的连带复验口径内，是**规划期的决策点**，不是可以默认略过的推断。
CONTEXT 与 ROADMAP 的「6」是**该文档的口径**，磁盘是 10。**planner 须显式裁定取哪个口径并写进计划**，
不得让执行器在收口时才发现第 7～10 份。（判据锚的是 frontmatter 的 `covered_files` 逐行匹配，
不是全文 grep —— 全文 grep 会把只在正文里提及 `frontend/style.css` 的报告也算进来。）

> **✅ 该口径差已由 orchestrator 裁定并落盘（2026-09-27,规划期,planner 直接采纳本裁定即可,不必重开）。**
> 判据不止「谁覆盖了该文件」,还要加一问「**`covered_files` 的路径还在盘上吗**」—— 只看覆盖名单会把
> 10 份都算成债务,只看路径解析又会把 `idi-09` 漏掉。逐份实测路径缺失数:
> `12/41`、`11/26`、`13/31`、`8/13`、`8/12`、`8/11`、`8/10`、`6/9`、**`0/10`**、`2/7`。
> ⇒ **只有 `idi-09` 全部在盘**;其余 9 份的 stale 成因是**路径**(归档后
> `.planning/phases/<id>/…` → `.planning/milestones/<ver>-phases/<id>/…`),不是内容,
> 属 STATE.md 于 **2026-09-14** 登记并复认的已知限制「归档后的报告不再被 staleness 机制消费」,
> **在 Phase 10 之前就已是 fail-closed stale,与本次改动无关**。
> **裁定:本阶段只重新验证 `idi-09` 一份**,仍按「以 HEAD 内容重新验证,不是刷新指纹」处置;
> 其余 9 份的重验须先修复归档路径引用,是另一件已登记的 backlog 事项,不在本阶段边界内
> (Phase 9 改同一文件时同样只重验了 live 树内的 `idi-09`)。
> **配套硬约束:本阶段不得改 `scripts/check-05-ui-uat.py`** —— 它在 `idi-08` 的 `covered_files` 里
> (`idi-08` 不含 `style.css`),改它会把重验面从 1 份变成 2 份。
> **⚠ 另:本文件上方引用的 `PASS  15.48  --color-text on --color-surface` 是 pattern-mapper 的读数,
> orchestrator 因 Bash 分类器不可用而未能复现。执行器须当场跑 `check-02` 并贴出真实输出,不得沿用此数字。**

---

## Shared Patterns

### 就地改写既有声明（追加,不重排）
**Source:** `frontend/style.css:752-775`（`#doc-panel` 的 `border-left` → `border`）
**Apply to:** 表格规则（`:1083` 的 `border` 声明）、`--radius-lg` 的 2 处消费者（`:1173` / `:1202`）

Phase 9 亲手留下的同型先例，注释里逐字写着理由：
```css
   是就地改写那条声明,不是追加一条 `border` 覆盖它(留下一条已死的 border-left 会让
   注释与代码互相矛盾)。
```
配套纪律（CONTEXT §编辑纪律）：
- **不得移动任何既有规则块的位置** —— 至少一对等特异性规则由源码顺序决定（例：`.chat-ai` 与
  `.chat-bubble` 同为 0-1-0，`frontend/style.css:1178-1179` 的注释逐字登记了这条依赖）。
- 需要新增规则块时（如 `.markdown-body th { background: …; }`），只能**追加到既有规则之后**。

### 注释纪律（围栏内 vs 围栏外，两套不同的禁令）
**Source:** `frontend/style.css:466-476`（围栏内可写裸 hex，但不得写「令牌名 + 冒号」）+ Phase 9 plan 01/02 的 `<prohibitions>`
**Apply to:** 本阶段全部 `style.css` 改动

| 位置 | 允许 | 禁止 |
|---|---|---|
| 围栏内（`===== DESIGN TOKENS: START/END` 之间） | 裸 `#hex`、数值 | **「令牌名 + 冒号」**（`check-02` 的 `DECL_RE` 扫围栏全文含注释，会当成值不可解析的声明而 FAIL）；字面量 `!important;` |
| 围栏外 | 令牌名（`--color-surface` / `--color-border-subtle` / `--radius-md`） | 裸 `#hex`、`var(--radix-…` / `var(--white)`（tier-1 原语私有于围栏，`check-01` 扫围栏外全文）、字面量 `!important;`（`check-04` 按**出现次数**数 `!important;`，散文注释会把计数从 1 顶高 —— 本项目已因此红过三次）、`@layer` / `@property` / `var(--x, #fallback)` |

### 令牌消费契约（D-04 / Hard Rule 5）
**Source:** `frontend/style.css:402-406`（`/* Radius — four values. */`）
**Apply to:** `--radius-lg` 的删除

「never declare a token you are not consuming」⇒ 2 处消费者搬走后，**不得**留下未消费的
`--radius-lg` 声明。但**删令牌前必须先搬消费者**，且删完要同时核对两个独立量
（围栏内声明数 == 0 **且** 全文 `var(--radius-lg)` == 0）。

### 门禁复跑 + 指纹重验（不是刷新）
**Source:** `.planning/phases/idi-09-card-containers/gate-logs/` + `idi-09-VERIFICATION.md` 的 `re_verification:`
**Apply to:** 本阶段的验证波次

- 五条浏览器门：`check-05`（**必须** `.venv/bin/python` + `--browser bundled`；全量 `exit=2` 是
  item 5 两条 `--ai-smoke` 腿按设计 BLOCKED，**不是回归**）/ `check-06` / `check-07` / `probe-05` / `probe-07`
- 四个静态门：`check-01` / `check-02` / `check-03` / `check-04`（全部打印 `PASS`）
- `node --check frontend/app.js`
- pytest **必须**用项目 `.venv`（环境 `python3` 是 miniconda，会让 4 个 `ai_caller` 测试假失败）：
  基线 **219 passed / 6 skipped**
- 仓库卫生：`git status --porcelain frontend/` 仅预期文件、`frontend/vendor/` 仍只有 `marked.min.js`

### 零新增 / 零放宽（本阶段的硬边界）
**Source:** `scripts/check-01-token-conformance.sh` + `scripts/check-02-contrast.py:24-25`
**Apply to:** 全部改动

```python
TEXT_MIN = 4.5
NON_TEXT_MIN = 3.0
```
`check-02` 的 `TEXT_MIN` / `NON_TEXT_MIN` 必须与 HEAD **逐字节相同**。零新增颜色值、
零新增 tier-1 primitive、零新增 `!important`、零令牌化 `display`、零 `@layer` / `@property` /
`var(--x, #fallback)`、零新增运行时依赖、零构建步骤（DESIGN.md D-06）。

### 门禁环境事实（省得重踩）
**Source:** 09-CONTEXT.md §门禁环境事实 + MEMORY.md
**Apply to:** 验证波次

- `check-05` **必须**走 `.venv/bin/python` + `--browser bundled`；该机 `channel="chrome"` + headless 会**挂死**
- macOS **没有 `timeout` 命令**
- 本机 `grep` 是 **ugrep**，`-` 算词字符 ⇒ `\b` 对含连字符的令牌名不可靠；改名判据要**锚内容、逐行核对**，别只数个数
- 8765 端口可能存在先前遗留的 uvicorn 进程；浏览器门走「复用，不新起」分支是既有事实
- `frontend/style.css` 与 `scripts/check-05-ui-uat.py` **不得**在本阶段改动后者（改了会把 `idi-08` 也拖进指纹名单）

---

## 影响面 / 回归面（规划期实测，供 planner 直接引用）

### 表格：无门断言（已核实）
`grep` 全部 7 个门脚本 + 2 个探针，**没有任何一条**断言表格的边框 / 底色 / 布局。
唯一接触点是 `scripts/check-05-ui-uat.py:1126`（`td font-size`），断言的不是本阶段要改的属性。

### 圆角：门禁几乎不设防（已核实）
- `scripts/check-09-idi09-validation.py:136` / `:186` **动态解析** `--radius-md` 再与卡片的
  计算 `border-top-left-radius` 比对 ⇒ **令牌相对，改值不破；但删该令牌会破**
- `scripts/check-06-idi05-validation.py:224` 读 `borderTopLeftRadius`，但只经 `info()` 打印，**不断言**
- 其余门与探针：零圆角断言。**无任何门引用 `--radius-lg`** ⇒ 删除它是安全的

### 语义耦合：无（已核实）
后端解析的是**原始 markdown 文件**，渲染是前端 `frontend/app.js:119` 的 `renderMarkdown()` 经
marked 转 HTML 注入 `.markdown-body`。改 CSS 只影响呈现，**不触碰任何解析路径**。

---

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| — | — | — | 本阶段无「无先例」文件。唯一的新文件 `scripts/check-10-idi10-validation.py` 有 exact 先例（`check-09-idi09-validation.py`，同型运行时门）；其余全是既有文件的就地改写或既有产物目录的同规格复制。 |

---

## Metadata

**Analog search scope:** `frontend/`（`style.css` 全文分区读）、`scripts/`（9 个门/探针的头部与关键段）、
`.planning/phases/idi-09-card-containers/`（3 份 PLAN + VERIFICATION + screenshots + gate-logs）、
`.planning/milestones/v1.13-phases/` 与 `v1.14-phases/` 的 VERIFICATION frontmatter
**Files scanned:** `frontend/style.css`（1869 行，分区读 8 段）、`scripts/check-09-idi09-validation.py`（552 行，读 3 段）、
`scripts/check-05-ui-uat.py`（选定 5 段）、`scripts/check-01/02/03/04`（全文）、
`idi-09-01-PLAN.md` / `idi-09-02-PLAN.md`（全文）、`idi-09-03-PLAN.md`（头部 + 结构）、
`idi-09-VERIFICATION.md`（frontmatter + 正文头部）、11 份 VERIFICATION 的 frontmatter
**Tracked-source gate:** 全部类比路径已用 `git ls-files --` 核对为 **git-tracked**；
未引用任何 `.gsd/capabilities/` 镜像路径（本仓库不存在该形态的同步树）
**Pattern extraction date:** 2026-09-27
