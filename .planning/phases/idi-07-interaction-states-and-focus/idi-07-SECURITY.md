---
phase: "idi-07"
slug: "interaction-states-and-focus"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-23"
---

# Phase idi-07 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**Scope of this phase:** `frontend/style.css` 的声明式 CSS(焦点环、交互态叠层、过渡与减弱动效块)加 `scripts/check-05-ui-uat.py` / `scripts/probe-07-focus-composite.py` 里的断言。**零新增网络端点、零新增输入面、零新增依赖、零新增构建步骤。** `frontend/app.js`、`frontend/index.html`、`frontend/vendor/`、`scripts/ui-states/` 逐字节未改。

**Audit depth:** ASVS L1,`block_on: high`。`register_authored_at_plan_time: true`(三份 PLAN 均带可解析的 `<threat_model>` 块)。按短路规则,`threats_open: 0` 在 L1 下 grep 深度验证即为充分 —— **未派发 security-auditor 子代理**。下表的全部证据由编排器于 2026-09-23 在 HEAD 上逐条重跑。

**本阶段的威胁面性质:** 这是一次**声明式 CSS + 测试脚本**的改动,不含网络、认证、文件访问或信任边界上的 schema 变更。因此下表的 STRIDE 条目绝大多数落在两类:**(a) 无障碍契约被削弱**(环不可辨、禁用态被软化),**(b) 假 PASS**(断言看起来在测它声称要测的东西,实际空转)。第二类是本阶段的主要风险形态 —— 一个恒绿的门比没有门更危险。

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 键盘用户 → 焦点环 (**主边界**) | 键盘焦点环是纯键盘用户的**唯一**位置信号。本阶段把环从「无作者化样式」升为一条声明式规则;若环不可辨(对比度不足 / 被祖先 `opacity` 合成冲淡 / 被裁切),该用户即失去导航能力 | 视觉信号;无数据 |
| 人类 → 授权门 (**核心价值边界**) | `#btn-authorize` 的禁用态是「未经用户明确授权,流程绝不进入撰写总设计文档」这条核心价值红线**唯一的视觉信号**。本阶段新增的 hover / active 叠层若把禁用态点亮成可点,即削弱该红线 | 视觉信号;无数据 |
| 断言 → 读者 (假 PASS 边界) | `check-05` 的逐项结论是后续所有验证与评审的事实依据。一个空转的 `info()` + `return` 会以 PASS 形态出现,使「已验证」变成不可信的主张 | 判定结果;无数据 |
| 包管理器 (供应链边界) | 本阶段不触及 —— 零安装调用进入范围 | 无 |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-idi-07-01 | Information disclosure / DoS(无障碍) | `:focus-visible` 规则 vs 祖先 `opacity` | medium | mitigate | 三条 PAIR 覆盖 `--color-surface-page` / `--color-surface` / `--color-surface@0.75`;`--color-surface-sunken` 明确不进验证面并在注释里说明理由。**实测:** `check-02` 三条全 PASS(5.72 / 5.57 / 3.45) | closed |
| T-idi-07-02 | Tampering | 焦点规则的几何(`border` / `padding`) | medium | mitigate | 规则体只声明 `outline` 与 `outline-offset`;静态守卫断言焦点规则块内 `border` / `padding` 计数为 0;几何与 `CLEARANCE_MIN_PX = 4.0` 双向绑定。**实测:** `style.css:1508-1517` 规则体仅两行声明;块内 `border\|padding` 计数 0;`outline: none` 计数 0 | closed |
| T-idi-07-03 | Tampering / DoS | 环色的「顺手修正」(`#1f63bd` → `--radix-blue-11`) | medium | mitigate | 围栏注释逐字写明这是对 S-4 已签核契约的字面遵从;`--color-surface@0.75` 的 3.45 余量是选它的实测依据。**实测:** `style.css:248-252` 逐字含 "This is LITERAL COMPLIANCE … Do NOT \"fix\" it to --radix-blue-11" | closed |
| T-idi-07-04 | Spoofing(假 PASS) | `item10` 的普查探针与 SC4 探针 | high | mitigate | `data is None` ⇒ `blocked`;判定集为空集 ⇒ `blocked`(不是 `info()` + `return`);SC4 的空集 / 元素不可见同样 ⇒ `blocked`;元素读不到 ⇒ `blocked`。**实测:** `check-05-ui-uat.py:2806-2844`(普查)、`:3043-3050`(SC4)均走 `blocked` 支;三样本判定集非空(9 / 8 / 9),`item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)` | closed |
| T-idi-07-05 | Repudiation | 归档半场的运行时断言 | medium | accept | 五个样本的 `#round-doc` 内 `a[href]` 计数为 0 ⇒ 今天无服务对象。**显式登记该事实**(不假装覆盖),由常驻算术门 + 一次性反事实探针共同承担。见下方 Accepted Risks Log | closed |
| T-idi-07-06 | Tampering | 填充按钮 hover 规则的选择器特异性 | high | mitigate | 十条选择器逐条列出具体特异性数值并要求逐条跨过对应既有规则。**实测:** `SC5` 在真实浏览器里读 `box-shadow`,五条断言 PASS(inset 999px 计数 2、hover 色、active 色、按下 ≠ hover) | closed |
| T-idi-07-07 | Elevation of privilege(禁用态响应交互) | L587 的 `button:hover` vs `.verdict-buttons button:disabled` | high | mitigate | gate 落在 L587 的选择器上(`:where(:not(:disabled))`),特异性逐位不变。**实测:** `SC5′` 用真实 `renderVerdictCard` + 真实 `.disabled` 切换断言「hover 背景 == 静默背景」(均 `rgb(249,249,249)`)且 `opacity` 仍为 0.5 | closed |
| T-idi-07-08 | Tampering | 朴素 `:active` 与 L587 hover 的配对 | high | mitigate | 朴素 active 停在 `:where(button:not(:disabled)):active` 的 0-1-0 —— 升到 0-1-1 就会靠源码顺序夺走 `button.primary` / `.overlay-card button` 的填充;让位由 L587 的 `:where(:not(:active))` 承担,两半必须同提交。**实测:** `SC5-朴素按下` 三条读数 ① `rgb(249,249,249)` → ② `rgb(240,240,240)` → ③ `rgb(232,232,232)`,且 ③ ≠ ② | closed |
| T-idi-07-09 | Information disclosure / Repudiation | 围栏外的裸 `rgba()` | medium | mitigate | alpha 值收进围栏内的 `--color-overlay-hover` / `--color-overlay-active`;判据取**围栏外**取样。**实测:** `awk` 取围栏外后 `grep -c 'rgba('` == **0** | closed |
| T-idi-07-10 | Spoofing(假 PASS) | SC5 / SC5-朴素按下 / SC5′ 探针 | high | mitigate | 读值前先断言目标元素存在且可见;造不出裁决卡 ⇒ `blocked`;期望侧用 `resolve_color` 解析令牌而非硬编码 rgb;朴素按下读完先 `page.mouse.move(0, 0)` 再抬手(避免误发 `POST /api/checks/verdict` 污染其后各项)。**实测:** 裁决卡构造成功(`{'buttons': 2, 'notes': 1}`),期望侧全部来自令牌解析,`0 FAIL / 0 BLOCKED` | closed |
| T-idi-07-11 | Tampering | 值碰撞被后来者「修正」 | low | mitigate | `--color-surface-active` 的注释点名 04.1-N-4 与 `--color-surface-user`,并同步扩写第 3 条。**实测:** `style.css:196-208`、`:375` 登记齐备 | closed |
| T-idi-07-12 | Tampering | 减弱动效块采用行业标准片段 | high | mitigate | 围栏注释逐字点名该片段带两个 `!important` 会让 `check-04` 从 1 变 3。**实测:** `style.css:1685` 逐字写明「本阶段不得采纳任何带 !important 的减弱动效写法」;`check-04` 输出 `PASS`(`!important;` 声明数恒为 1) | closed |
| T-idi-07-13 | DoS(门恒红 / 恒绿) | `EXPECTED_MEDIA_QUERIES` 与 `@media` 实际计数 | high | mitigate | 常量、注释、断言标签三处与 media 块同一次提交。**实测:** 常量 == `1`(`check-05-ui-uat.py:1674`);`grep -c '^@media (prefers-reduced-motion' frontend/style.css` == **1**;`--item 8` PASS(13 条断言) | closed |
| T-idi-07-14 | Tampering | 既有的 `.event-list` 300ms 声明 | medium | mitigate | 断言该行未出现在 diff 中;运行时探针把「例外仍在」变成可观测事实。**实测:** `style.css:1666-1669` 声明保留 300ms「一个字节不动」;探针在 p1 读到 `.event-list` 的 `0.3s`(`check-05-ui-uat.py:98`) | closed |
| T-idi-07-15 | Spoofing(假 PASS) | 「同提交」的静态断言 | medium | mitigate | 断言退化为「两者同时存在」并**在 `info()` 里逐字声明它不证明同提交**。**实测:** `check-05-ui-uat.py:3576-3583` 逐字含「本断言**不证明同提交**」 | closed |
| T-idi-07-16 | Tampering | 焦点环被加进过渡列表 | medium | mitigate | 围栏注释写明「过渡焦点环是已知的无障碍反模式」;静态断言计数为 0。**实测:** `grep -c 'transition:.*outline' frontend/style.css` == **0**;`style.css` 注释逐字含该反模式说明 | closed |
| T-idi-07-17 | Repudiation | 本阶段作废的验证指纹 | high | mitigate | 以 HEAD 内容重算四份报告的 digest,逐份判定「重新验证 / 重算 + 披露」。**实测:** `idi-07-VERIFICATION.md:167-183` 逐份登记四份报告的记录值与 HEAD 重算值,结论均为 **stale ⇒ 重新验证**;并明令禁止用 `query verification status` 判定 stale | closed |
| T-idi-07-18 | Repudiation | 人工验收项 5″ | medium | mitigate | 逐字写进 VERIFICATION 的 manual list,并写明机器半场覆盖了什么、人工半场要回答什么;不得换成机器代理量。**实测:** `idi-07-VERIFICATION.md:24-27, 146-148` 具名登记;该项已于 2026-09-23 由用户在 UAT 中确认 **pass** | closed |
| T-idi-07-19 | Spoofing(假 PASS) | 朴素按下读数可能只是 hover 读数的回声 | high | mitigate | SC5-朴素按下同时断言 ③ == `--color-surface-active` **与** ③ ≠ ②(同一元素的 hover 读数);只断言前者时,让位未生效的实现会读到 hover 值而不会变红。**实测:** `check-05-ui-uat.py` 含 3 处 `!= ②` 对照断言,全部 PASS(③ `rgb(232,232,232)` ≠ ② `rgb(240,240,240)`) | closed |
| T-idi-07-SC | Tampering | npm / pip / cargo 安装 | low | accept | 零新增运行时依赖、零构建步骤(硬规则 6):无包管理器调用进入范围。见下方 Accepted Risks Log | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-idi-07-01 | T-idi-07-05 | 归档半场(`.archive-mode` 0.75 合成)的运行时焦点环断言今天**无服务对象**:五个样本的 `#round-doc` 内 `a[href]` 计数为 0,生产路径没有等价物。常驻算术半场(`check-02` 的 `--color-focus@0.75 = 3.45 >= 3`)不依赖该 fixture,故本条只降级**探针的可外推性**,不降级结论。缓解:探针 `scripts/probe-07-focus-composite.py` 以一次性注入交付(注入确实发生 0 → 1、归档态确实生效、注入链接确实被环覆盖、用运行时实测值复算合成算术);`idi-07-VERIFICATION.md` 的 `coincidental_reliance_items` 逐字登记。**Phase 8 给 `#round-doc` 加 `tabindex="0"` 后该场景变为活体,届时须复跑探针** | 用户(阶段授权) | 2026-09-23 |
| AR-idi-07-02 | T-idi-07-SC | 本阶段零新增运行时依赖、零构建步骤,故无供应链面。若执行期出现安装需求,即为计划偏差与停止条件。实测:`git log --grep='idi-07' -- requirements.txt package.json pyproject.toml setup.py` 为空 | 用户(阶段授权) | 2026-09-23 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-23 | 20 | 20 | 0 | Claude (gsd-verify-work orchestrator) — ASVS L1 grep-depth, short-circuit (no auditor spawned) |

**审计方式:** State B(无既有 SECURITY.md,由三份 PLAN 的 `<threat_model>` 块重建寄存器)。全部 20 条威胁的缓解面由编排器于 2026-09-23 在 HEAD 上**逐条重跑**,未采信 SUMMARY 的自述。关键复跑证据:`check-01`…`check-04` 全 `PASS`;`check-05 --item 10` `PASS (41 条断言, 0 FAIL, 0 BLOCKED)`;`check-05` 既有九项 9/9 PASS;`probe-07` exit 0 `ratio=3.45`;围栏外裸 `rgba()` 计数 0;`transition:.*outline` 计数 0。

**两条 `accept` 的处置:** 均已在 Accepted Risks Log 逐条登记理由与缓解面,并附 Phase 8 的复核触发条件。

**阻断判定:** `block_on: high`。无 `high` 及以上严重度的 OPEN 威胁 ⇒ `threats_open: 0` ⇒ **不阻断阶段推进**。

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-23
