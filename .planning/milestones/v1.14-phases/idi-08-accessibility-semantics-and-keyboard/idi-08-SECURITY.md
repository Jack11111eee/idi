---
phase: "idi-08"
slug: "accessibility-semantics-and-keyboard"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-24"
---

# Phase idi-08 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**Register origin:** authored at plan time — all three plans (`idi-08-01/02/03-PLAN.md`) carry a parseable `<threat_model>` block, so `register_authored_at_plan_time: true`. No `## Threat Flags` entries were added by any SUMMARY.

**Verdict: `threats_open: 0`.** All three **high**-severity threats (T-idi08-05, T-idi08-10, T-idi08-SC) are verified closed, so nothing at or above `workflow.security_block_on: high` remains open. Two **medium** threats produced findings below the block threshold and are registered below.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 服务端 / AI 产出的 markdown → DOM | 轮次文档与批注内容经 `marked` 渲染 + `stripUnsafeNodes` 过滤后进入页面;本阶段**不改**这条链路 | untrusted markdown → DOM |
| 服务端错误消息 → 内联错误节点 | `showInlineError` 的 `textContent`-only 规则是 XSS 缓解(T-260916-01),**不是风格选择**(硬规则 5) | error text → DOM |
| 弹窗标题文案 → 无障碍名称 | `aria-labelledby` 指向弹窗内既有的 `<h3>`;本阶段**不新写任何字符串** | static label → a11y name |
| 背景惰性属性 → 背景可交互性 | `inert` 决定背景在键盘与指针两个层面是否可及;挂错节点会把打开的弹窗自身锁死 | attribute → interactivity |
| Escape 键 → 应用决定 | 分派器决定 Escape 是否触发关闭、以及是否触发任何业务决定(如「拒绝」) | key event → app decision |
| 浏览器选区 API → 焦点管理 | 新增的 Shift 监听器读 `window.getSelection()` 状态并调用 `.focus()` | selection state → focus |
| 验证记录 → 门 | 门的**算术**决定阶段能否在未验证时宣告通过;基线取错会造出永不失败或必然失败的假门 | measured values → gate |
| 验证 harness → 6 份 live 报告 | `scripts/check-05-ui-uat.py` 在 6 份 live 报告的 `covered_files` 里;改它会作废那些指纹 | shared instrument → fingerprints |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-idi08-01 | Tampering | `initSelectionMenu()` 新增的 Shift keyup 监听器 | low | mitigate | 只读 `window.getSelection().isCollapsed` 并调 `annotateBtn.focus()`;不写 DOM 文本、不拼字符串、不构造选择器。**实测复核**:该监听器体内零 `textContent`/`innerHTML`/`insertAdjacentHTML` | closed |
| T-idi08-02 | Tampering | `hideSelectionMenu()` 新增的焦点交还 | low | mitigate | 只加 `selectionMenu.contains(document.activeElement)` 布尔判据与 `roundDoc.focus()`。**实测复核**:体内唯一 DOM 副作用是 `if (hadFocus) roundDoc.focus();`,无文本写入 | closed |
| T-idi08-03 | Elevation of Privilege | `#round-doc` 获得 `tabindex="0"` | low | accept | 元素是既有 markdown 渲染容器,不含新输入 sink;`stripUnsafeNodes` 的 `on*` 属性与 `javascript:` 链接剥离不受影响。**实测复核**:`frontend/index.html` 中 `tabindex` 计数 = 1 | closed (accepted) |
| T-idi08-04 | Denial of Service | 焦点环的可辨性判定 | low | mitigate | 落成具名人工步骤 + D-02 强制升级分支,不允许静默降级。**实测复核**:`probe-07-focus-composite.py` 读数 ratio **3.45 ≥ 3.0**(archive 态,`links-before=0` / `links-after=1` 证明变异已施加);plan 01 中 D-02 被引用 18 处 | closed |
| **T-idi08-05** | Denial of Service | `syncBackgroundInert()` 的挂载点 | **high** | mitigate | 属性**只**挂 `appEl`(`#app`,`app.js:90`)。**实测复核**:全仓无 `document.body[.inert]` / `documentElement.inert` / 共享祖先写法(仅注释中的禁令);`check-07 --item g2` 行为验证 —— 弹窗开 ⇒ `#app` 同时具 attribute 与 IDL `inert`,且 `#ai-route-select.focus()` 成为 no-op;两弹窗皆关 ⇒ 属性摘除且同一 focus 调用生效。`document.body`、打开的弹窗自身、`#selection-menu` 均不带 | closed |
| T-idi08-06 | Spoofing | `#confirmation-modal` / `#tier-modal` 的 `aria-modal="true"` | medium | mitigate | **实质成立,字面要求被证伪 —— 见下「偏差登记」D-1**。HEAD 上宣告与实现一致,且 `check-07 --item g2` 行为验证了配对(两弹窗各自 `role="dialog"` + `aria-modal="true"` + `aria-labelledby` **解析到弹窗内**非空标题;`inert` 随开启/关闭切换) | closed (deviation D-1) |
| T-idi08-07 | Tampering | Escape 分派器的确认分支 | medium | mitigate | Escape **只关闭、零决定**(D-12)。**实测复核**:分派器内(剥注释后)无 `rejectAuthorization()` / `window.prompt` 实际调用;`check-07 --item g1` 行为验证 —— 受信 Escape 后原生对话框 0 个、写批注/授权 POST 计数不变 | closed |
| T-idi08-08 | Elevation of Privilege | 新增的 2 个 id 与 `aria-labelledby` | low | accept | 无障碍名称指向既有 `<h3>`,不新写字符串、不拼接、不构造选择器;新增 id 不引入输入 sink。**实测复核**:`frontend/index.html` 共 82 个 `id="`,两个新 id 为 `confirmation-modal-title` / `tier-modal-title` | closed (accepted) |
| T-idi08-09 | Information Disclosure | `#confirm-error` 的错误文案 | low | mitigate | 错误文案仍只经 `textContent` 写入(XSS 缓解 T-260916-01)。**实测复核**:`showInlineError` 体内为 `p.textContent = message;`,无 `innerHTML`;`frontend/style.css` 中 `inline-error` 计数 = 1 | closed |
| **T-idi08-10** | Repudiation | REG-02 门②与 pytest 的基线算术 | **high** | mitigate | 基线一律取**实测值**。**实测复核**:门② `grep -c 'clearInlineError();' frontend/app.js` 期望 `>= 9`,实测 **9**(plan 明文拒绝 `08-CONTEXT.md` D-21 那个来自 `b9664e0` 时代的旧「6」,照抄会造出永不失败的假门);门① `inline-error` 实测 **1**;pytest 实测 **219 passed / 6 skipped / 225 collected**,与 plan 的判据口径逐字一致(219 是通过数、225 是收集数) | closed |
| T-idi08-11 | Tampering | `scripts/check-05-ui-uat.py` 的断言与常量 | medium | mitigate | **被证伪 —— 见下「偏差登记」D-2**。该文件本阶段**并非**零改动:`63fba08` 改动了它(+46/−2,用户裁定的 L-5 缺口收口)。其后果(5 份先前报告的指纹作废)已实测发生并登记为 Accepted Risk AR-01 | **open — below high threshold (non-blocking)** |
| T-idi08-12 | Information Disclosure | `showInlineError` 的 `textContent`-only 规则 | medium | mitigate | 本计划零改动该函数(硬规则 5)。**实测复核**:`showInlineError` 体内仅 `p.textContent = message;`;两条 REG-02 门(门① `inline-error` == 1、门② `clearInlineError();` >= 9)守住该路径未被改写 | closed |
| T-idi08-13 | Repudiation | 人工验收项的「继承而非重跑」 | medium | mitigate | REG-03 第 4 条**按 D-05 的新手势重写**,并逐条记录步骤与观察结果。**实测复核**:`idi-08-03-SUMMARY.md` 中 D-05 被引用 4 处,§REG-03 observation record 逐条记录;`idi-08-UAT.md` test 3 已由用户确认 pass | closed |
| **T-idi08-SC** | Tampering | npm / pip / cargo 安装 | **high** | mitigate | **本阶段零新增运行时依赖、零构建步骤**。**实测复核**:`frontend/vendor/` 恰为 1 个文件(`marked.min.js`);无 `package.json`、无 `node_modules`;`requirements.txt` / `pyproject.toml` 在本阶段窗口内零改动 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## 偏差登记 (Deviation Log)

两条 medium 威胁的计划期缓解措施**字面被证伪**。两条都低于 `block_on: high`,故均不阻塞阶段推进;登记在此以备复核。

### D-1 — T-idi08-06:「`aria-modal` 与 `syncBackgroundInert()` 在同一次提交落地」未成立

- **计划要求**:两者**同一次提交**,使宣告与实现在结构上一致(SC3)。
- **实测**:`aria-modal` 由 `41f1289` 引入;`syncBackgroundInert()` 由 `b9f775e` 引入 —— **两个不同提交**。故历史中存在一个「已宣告 `aria-modal="true"` 但尚无背景惰性」的中间状态。
- **为何仍判 closed**:威胁的**安全实质**是「宣告必须被实现兑现」。在 HEAD 上两者俱在,且 `check-07 --item g2` **行为性**验证了配对(而非只读属性):`inert` 随弹窗开/关切换,开启期间背景元素的 `focus()` 确为 no-op。中间态窗口在单人本地工具、提交之间无部署的语境下不可利用。
- **性质**:过程偏差,非开放性漏洞。

### D-2 — T-idi08-11:「该文件本阶段零改动」被证伪,且后果已发生

- **计划要求**:`scripts/check-05-ui-uat.py` 本阶段**零改动**,以 `git status --porcelain` 为空为证据;它是 5 份 live 报告 `covered_files` 的成员,改它会作废那些指纹。
- **实测**:`63fba08`(「declare tall focusable content regions in L-5, per user ruling」)改动了该文件,+46/−2。**这并非擅自改门** —— 计划对「门变红」的处置要求(先判「真缺陷 vs 普查集变化」再动门)被遵守了:L-5 门因把一个高的可聚焦**内容区**当控件断言而变红,用户裁定修改门的**范围**(把这类行**声明**出来而非断言,并加 fail-closed 兜底:若声明集吃掉整个判定集则记 `blocked` 而非 PASS)。
- **后果已实测发生**:`check-05-ui-uat.py` 出现在 **6** 份 `*-VERIFICATION.md` 的 `covered_files` 中。其中 **5 份**现在读到 **`status: stale`**。**但这 5 份里只有 1 份是本阶段造成的** —— 逐份比对「该报告写入时 → 阶段 8 起点(`126646e`)」与「阶段 8 起点 → HEAD」两个窗口内其 `covered_files` 的实际变化:

  | Phase | verification 写入于 | 阶段 8 **之前**已被改动 | 阶段 8 内被改动 | 归因 |
  |-------|--------------------|------------------------|----------------|------|
  | idi-04-tokens-contract | `812a224` (09-20) | `REQUIREMENTS.md`, `frontend/style.css` | `REQUIREMENTS.md` | **本阶段之前就已 stale** |
  | idi-04.1-radix | `812a224` (09-20) | `REQUIREMENTS.md`, `frontend/style.css`, `check-05` | `REQUIREMENTS.md`, `check-05` | **本阶段之前就已 stale** |
  | idi-05-typography | `e396c66` (09-21) | `REQUIREMENTS.md`, `frontend/style.css`, `check-05` | `REQUIREMENTS.md`, `check-05` | **本阶段之前就已 stale** |
  | idi-06-layout-robustness | `5bc3b88` (09-22) | `REQUIREMENTS.md`, `frontend/style.css`, `check-05` | `REQUIREMENTS.md`, `check-05` | **本阶段之前就已 stale** |
  | idi-07-interaction-states | `f0f0c31` (09-23) | *(无)* | `REQUIREMENTS.md`, `check-05` | **本阶段造成** |
  | idi-08-accessibility | — | — | — | `passed` |

  **准确的结论:阶段 8 使 `idi-07` 从 fresh 变为 stale;`idi-04 / 04.1 / 05 / 06` 在阶段 8 开始之前就已经 stale**(它们的 `frontend/style.css` 与 `REQUIREMENTS.md` 在阶段 5/6/7 期间已变,`check-05` 亦在阶段 7 被多次改动)。把 5 份全部归因于 `63fba08` 是**过度归因**,已在本次审计中实测更正。

  这个 `stale` 读数在两种情形下都是**准确**的,不是假警报:共享仪器或覆盖内容确实变了,那些报告的验证结论相对 HEAD 不再自动成立。**补救方向是重跑那些阶段的验证,不是去改指纹**(改指纹会掩盖真实的仪器变更)。
- **性质**:验证完整性债务,非漏洞。已登记为 AR-01。

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-01 | T-idi08-11 | `63fba08` 对共享 harness `scripts/check-05-ui-uat.py` 的改动(用户裁定的 L-5 缺口收口)使 **`idi-07` 的 VERIFICATION 由 fresh 转为 `stale`**(实测归因,见 D-2 表)。该改动本身经用户授权、且是必要的(门确实变红);`stale` 读数准确反映共享仪器已变。`idi-04 / 04.1 / 05 / 06` 的 `stale` 在阶段 8 开始**之前**就已存在,不归因于本阶段。**补救路径(非阻塞,待用户决定)**:对这 5 个阶段各重跑一次 `/gsd-verify-work` 以刷新指纹;其中 `idi-07` 是唯一因本阶段而 stale 的。本阶段**不**代为修改那些报告。 | orchestrator (secure-phase audit) | 2026-09-24 |
| AR-02 | T-idi08-03, T-idi08-08 | `#round-doc` 的 `tabindex="0"` 与两个新 id / `aria-labelledby` 属「accept」处置:不引入新输入 sink,渲染面既有 XSS 防线不变。已逐项实测复核。 | orchestrator (secure-phase audit) | 2026-09-24 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-24 | 14 | 13 | 1 (below high threshold — non-blocking) | orchestrator (secure-phase; `asvs_level: 1`, L1 depth) |

**Short-circuit applied:** `threats_open (high) == 0` AND `register_authored_at_plan_time: true` AND `asvs_level == 1` ⇒ the `gsd-security-auditor` spawn was skipped by the workflow's own rule (L1 grep-depth is sufficient at ASVS L1 with a plan-time register). Verification was nonetheless performed at **behavioral** depth rather than grep depth for the three high threats, since this phase's Nyquist audit had just produced live runtime harnesses (`check-07`) that could prove the two most consequential controls (T-idi08-05 background inert, T-idi08-07 zero-decision Escape) by observation instead of by reading source.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed (no open threat at or above `block_on: high`)
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-24
