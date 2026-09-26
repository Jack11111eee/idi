---
phase: "idi-05"
slug: "typography-and-visual-hierarchy"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-21"
---

# Phase idi-05 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**Scope of this phase:** `frontend/style.css` declaration values (font-size / font-weight / line-height / colour-ramp values) plus assertions in `scripts/check-05-ui-uat.py`. **Zero new network surface, zero new input surface, zero new dependencies, zero new files.** `frontend/app.js`, `frontend/index.html`, `frontend/vendor/` and `frontend/ui-states/` are byte-unchanged.

**Audit depth:** ASVS L1, `block_on: high`. `register_authored_at_plan_time: true` (all three PLANs carry a parseable `<threat_model>` block). Per the short-circuit rule, `threats_open: 0` at L1 means grep-depth verification is sufficient — no security-auditor subagent was spawned. All evidence below was re-run by the orchestrator on 2026-09-21.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 人类 → 流程 (**主边界**) | G3 授权按钮的**视觉形态**是核心价值红线的机器可读信号(未经用户明确授权,流程绝不进入撰写总设计文档)。本阶段把三段坡道落地,使 `#btn-authorize` 在**形态**上就与五只例行/承诺按钮不同(淡底 vs 实心),不依赖色深对比 | 视觉信号(形态区分);无数据 |
| 围栏 `:root` → 浏览器 | `frontend/style.css` 是唯一被消费的样式来源;围栏 `:root` 是令牌的唯一事实源。任何绕过围栏的字面量都会削弱「值层改动不产生假 FAIL」这条 idi-04.1 已立的性质 | 令牌值 |
| `:not(.hidden)` → `.hidden` 机制 | 新增的活动面板标记规则**读取**面板显隐状态,不修改它。`.hidden { display: none !important }` 承载六个元素、压制三个 1-0-0 竞争者 | 显隐状态(只读) |
| 围栏内 data-URI → 浏览器渲染 | 两个手写 SVG data-URI 是唯一的新内容来源;不进 DOM、无脚本执行面、无外部 URL 抓取。零颜色信息是撤掉字面量例外 L-3 的唯一依据 | 内联字形位图;无外部请求 |
| `scripts/check-02-contrast.py` → 上游文档 | 比值的唯一仲裁者是本脚本的实算值,Radix 与两份 UI-SPEC 的 AA 论断**一律不采信** | 对比度实算值 |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-idi-05-01 | Elevation of Privilege | `#btn-authorize`(G3 授权门)的视觉形态 | high | mitigate | `#btn-authorize` 按 D-12 保持 `font-weight: var(--fw-semibold)`(600)是 D-09「按钮统一 500」的唯一已登记例外(`style.css:1058`,逐字带注释说明);`--color-action-irreversible*` 保持单消费者(D-15:3 条声明在围栏内 `:143-145`,3 条消费者 `:1052-1054` 全在 `#btn-authorize` 规则体内);`check-05 --item 4` 六条字重断言 PASS(五只动作按钮 = 500、`#btn-authorize` = 600) | closed |
| T-idi-05-02 | Tampering | `frontend/style.css` 围栏与四条守卫的不变量 | medium | mitigate | `bash scripts/check-01-token-conformance.sh` exit 0;`bash scripts/check-03-hidden-uniqueness.sh` exit 0(`^\.hidden {` == 1);`bash scripts/check-04-important-count.sh` exit 0(`!important;` 声明数 == 1);围栏标记 1/1(`:5` START / `:431` END);`.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`,47 对,`ORDER 0.363` 逐字在位 | closed |
| T-idi-05-03 | Tampering | 全局 `h1, h2, h3` 规则泄漏到 chrome | medium | mitigate | `grep -oE '(^\|[,{ ])[[:space:]]*h1[[:space:]]*,[[:space:]]*h2' frontend/style.css \| wc -l` == **0**;六条 chrome 字面 px 守卫保持不动,`check-05 --item 4` 的四条 chrome 守卫 PASS(`.panel-header h2` 14px、`#draft-view h2` 18px、`#brainstorm-view h2` 令牌接线、`.overlay-card h3` 24px) | closed |
| T-idi-05-04 | Denial of Service | 渲染回归(标题 / 字重) | medium | mitigate | 每个 `style.css` 任务带运行时验证(硬规则 7):`.venv/bin/python scripts/check-05-ui-uat.py --item 4` PASS(65 条断言,0 FAIL / 0 BLOCKED)、`--item smoke` PASS(8 条);本审计追加 `scripts/check-06-idi05-validation.py` PASS(40 条断言,含 g1 逐宿主 `h1>h2>h3` 序断言、g2 全页最大字号扫描) | closed |
| T-idi-05-05 | Information Disclosure | 本阶段的改动内容 | low | accept | 改动只有字号与字重两个声明值,无用户数据、无网络请求、无外部资源;`ls frontend/vendor/` 仍只含 `marked.min.js`。见 Accepted Risks Log | closed |
| T-idi-05-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增任何依赖、文件或构建步骤。`ls frontend/vendor/` == `marked.min.js`;`git status --porcelain -- frontend/` 输出为空。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**threats_open: 0.** No open threat at any severity.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-idi-05-01 | T-idi-05-05 | 本阶段的改动面是 `frontend/style.css` 的声明值(字号、字重、行高、颜色坡道)与 `scripts/check-05-ui-uat.py` 的断言。不存在用户数据、凭据、网络请求或外部资源引用;工具本身是单机单人本地运行(D-03),样式表内容对攻击者无价值。**风险接受,不设缓解措施。** | 用户(经 `/gsd-verify-work idi-05` UAT 全数通过确认) | 2026-09-21 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-21 | 6 | 6 | 0 | orchestrator (L1 grep-depth; auditor not spawned per short-circuit rule) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-21