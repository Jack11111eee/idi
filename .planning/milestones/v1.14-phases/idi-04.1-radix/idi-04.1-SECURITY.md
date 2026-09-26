---
phase: "idi-04.1"
slug: "radix"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
# block_on = high; the only high-severity threat (T-idi041-09) is CLOSED, so 0 threats block advancement.
threats_open: 0
asvs_level: 1
created: "2026-09-20"
---

# Phase idi-04.1 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

**Phase:** Radix 颜色族重写 (INSERTED) — 值层重写,4 个 plan(含 gap-closure plan 04)
**Register origin:** authored at plan time — all four PLAN.md files carried a parseable `<threat_model>` block.
**Audit depth:** ASVS L1 (grep-depth). Short-circuit applied per `secure-phase.md` §3: `threats_open: 0` AND `register_authored_at_plan_time: true` AND `asvs_level == 1` → no auditor spawn required.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 仓库内静态文本 → 本地浏览器 | `frontend/style.css` 的围栏 `:root` 是唯一输入;应用不写 CSS 变量、不拼接 `style` 属性 | 无(仓库内静态文本,无运行时注入路径) |
| 守卫脚本 → 仓库工作树 | `check-01`…`check-04` 全部只读:不写文件、不跑 git、不联网 | 无(只读 `frontend/style.css`) |
| 本地应用 → Playwright harness | harness 起本地 uvicorn,浏览器进入 `scripts/ui-states/` 的磁盘状态样本;样本复制到 `mktemp` 临时目录 | 本地磁盘状态样本(无凭据、无用户数据、不外联) |
| 变异探针 → 浏览器侧被拦截的 `/style.css` 响应 | 唯一「不可信输入」是探针自己构造的那份被删掉一处声明的 CSS;**不落盘** | 探针自构造的 CSS 文本(不进入仓库工作树) |
| 断言记录器 → 验收结论 | `ok()` 的判定类别(PASS / FAIL / BLOCKED)决定 harness 退出码,即本阶段头条证据 `0 FAIL` 的语义 | 判定类别(决定证据的语义,不承载数据) |

**本阶段不存在网络面、认证路径、输入解析、新依赖或新文件。** 四个 PLAN 的 `<threat_model>` 结论一致:无外部可利用的 high / critical 威胁。

---

## Threat Register

> **⚠️ 威胁 ID 在本阶段内不唯一。** 四个 plan 各自独立编号,导致 `T-idi041-11` / `T-idi041-12` / `T-idi041-13` 与 `T-idi041-SC` 在 Plan 03 与 Plan 04 中被**复用为不同的威胁**。下表按「plan + ID」区分并保留两处定义。这是登记表编写上的缺陷(应做阶段级统一编号),已如实记录而非静默合并 —— 合并会让两个不同的威胁共享一条结论。

| Threat ID | Plan | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|------|----------|-----------|----------|-------------|------------|--------|
| T-idi041-01 | 01 | Tampering | `frontend/style.css` 围栏内的令牌值 | low | accept | 令牌值是仓库内静态文本,无运行时注入路径;篡改者需要写权限,而写权限已等于完全控制 | closed (accepted) |
| T-idi041-02 | 01 | Tampering | 令牌值流向 `url()` / `content:` 汇点 | none | accept | 本阶段不新增任何 `url()` / `content:` 汇点;新增值只流向 `background` / `color` / `border-*` / `box-shadow` | closed (accepted) |
| T-idi041-03 | 01 | Spoofing | tier-1 改名 `--radix-*` 后围栏外可冒充 primitive | low | mitigate | Plan 01 以「围栏外 `comm -23` 未解析 `var()` 为空」+ 人工 diff 复核作过渡证据,守卫加固与变异证明交 Plan 02 | closed |
| T-idi041-04 | 01 | Repudiation | 「渲染未变」被断言而非证明 | low | mitigate | 本计划不主张「渲染未变」,主张的是**刻意的渲染变更**(Delta Ledger);逐条运行时证据由 `item_smoke` 三条断言给出,完整携带项 #9 清单在 Plan 03 收口 | closed |
| T-idi041-05 | 02 | Tampering | `check-01-token-conformance.sh` 的 tier-1 交替式 | medium | mitigate | 交替式加宽到含 `radix`,并以变异测试证明「有泄漏时会 FAIL、旧交替式会 PASS」。实测 `check-01` 打印 `PASS`,exit 0 | closed |
| T-idi041-06 | 02 | Tampering | 变异测试误改真实工作树 | medium | mitigate | 全部变异在 `mktemp -d` 临时仓库根上进行;每任务末尾以 `git status --porcelain` 断言工作树无多余改动。实测 `git status --porcelain -- frontend/` 为空 | closed |
| T-idi041-07 | 02 | Repudiation | 守卫被断言为「有效」而非被证明 | medium | mitigate | 每条守卫断言都配一条变异运行;「旧交替式打印 PASS」的对照证据写进 SUMMARY | closed |
| T-idi041-08 | 02 | Information disclosure | 守卫脚本读取的内容 | none | accept | 两个脚本只读仓库内 `frontend/style.css`,不含凭据、网络调用或用户数据 | closed (accepted) |
| T-idi041-09 | 03 | Repudiation | 「运行时验证」被断言而非执行 | **high** | mitigate | 携带项 #9 的九组具名检查逐条落到 `item_smoke` / `item3` / `item4` / `item5`,每条配可运行 `<automated>` 命令与 `<fails_when>`。**编排器独立复跑**:全量 harness 0 FAIL,`item 1 PASS (45,0,0)` / `2 PASS (5,0,0)` / `3 PASS (15,0,0)` / `4 PASS (24,0,0)` / `5 BLOCKED (9,0,2)` / `6 PASS (2,0,0)`,`exit=2`;两条 BLOCKED **恰为**已记录的两条交互冒烟,未被任何手段「变绿」 | closed |
| T-idi041-10 | 03 | Repudiation | 令牌接线断言掩盖「值本身错了」 | medium | mitigate | ①每条接线断言旁 `info()` 打印运行时解析值;②值的仲裁者是 `check-02-contrast.py` 的 43 对实测比值。实测 `check-02` `PASS: 0 failures`(含 `ORDER 0.363`),exit 0 | closed |
| T-idi041-11 | 03 | Tampering | 为让断言通过而改 `frontend/style.css` | medium | mitigate | 本阶段 `files_modified` 不含 `frontend/style.css`;verify 断言 `git status --porcelain -- frontend/...` 为空。实测为空,`git diff --exit-code -- frontend/style.css` exit 0 | closed |
| T-idi041-12 | 03 | Spoofing | 用无头系统 Chrome 或静态分析冒充真实渲染 | low | mitigate | `.venv` Python 是 x86_64,系统 Chrome 走 Rosetta,`channel="chrome"` + headless 在本机 CDP 180s 连不上而挂死;harness 默认 `--browser bundled`(arm64 原生、零下载)。编排器复跑未传 `--browser`,全量通过 | closed |
| T-idi041-13 | 03 | Information disclosure | harness 读取的内容 | none | accept | 只读本地磁盘状态样本与本地应用的 computed style,不含凭据、不外联 | closed (accepted) |
| T-idi041-11 | 04 | Tampering | 变异证明污染真实 `frontend/style.css` | medium | mitigate | 变异只在 `page.route("**/style.css", …)` 拦截到的响应里构造,**不写任何磁盘文件**;Task 2/3 各有一条 `git diff --exit-code -- frontend/style.css` / `git status --porcelain -- frontend/` 门。实测两条门均通过 | closed |
| T-idi041-12 | 04 | Tampering | 空转变异(变异其实没发生,证明变成空转) | medium | mitigate | 本机 darwin,BSD `sed` 的 `0,/re/` 地址会静默不替换,故探针**禁用 `sed`**,改用 Python 字符串操作,并显式断言 `mutated != 原始 body` 且不再含 `--color-text-muted:`,必须打印 `PROBE mutation-applied=yes`。实测该行输出 | closed |
| T-idi041-13 | 04 | Repudiation | 修复被断言为「有效」而非被证明 | medium | mitigate | 每条修复断言都配一条变异运行:同一份被删掉声明的副本上,修复前记 PASS、修复后记 BLOCKED。实测 `mutated-prefix-verdict=PASS` / `mutated-postfix-verdict=BLOCKED` | closed |
| T-idi041-14 | 04 | Tampering | 修复把断言变成**恒 BLOCKED**(另一种空转) | medium | mitigate | PASS B(未变异对照)断言同一条断言仍记 PASS;全量 harness 门要求 item 1/2/3/4/6 的 BLOCKED 计数为 0。实测 `control-verdict=PASS`,四项 BLOCKED 计数均为 0 | closed |
| T-idi041-15 | 04 | Tampering | `ok()` 的新分支吞掉真实 FAIL(把真缺陷降级成 BLOCKED) | medium | mitigate | 该分支**只在 `expected is None` 时生效**;真实树上全部令牌已声明、两个 resolver 均返回非 None 值。全量 harness 门要求逐项结论与 VERIFICATION.md P3.7 基线**逐项一致**。实测逐项一致,任何降级都会让计数偏移而被抓住 | closed |
| T-idi041-16 | 04 | Repudiation | 新探针被当成门禁而长期腐烂 | low | mitigate | 探针顶部注释明写「变异证明,不是门」;`grep` 确认四条守卫命令均不引用它。实测无引用 | closed |
| T-idi041-SC | 01–04 | Tampering | npm / pip / cargo 安装(供应链) | none | accept | **四个 plan 均不安装任何包。** Plan 01 明禁 vendor Radix CSS(色值手工转抄 hex);Plan 03 明禁 `playwright install`(捆绑 chromium-1243 已在本机缓存)。实测本 run 未新增依赖,`frontend/vendor/` 仍只含 `marked.min.js` | closed (accepted) |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (`high`) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**Blocking-gate arithmetic:** the only threat at or above the `high` threshold is **T-idi041-09** (high). Its mitigation is present and was independently re-run by the orchestrator. `threats_open: 0`.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-01 | T-idi041-01 | 令牌值是仓库内静态文本,无运行时注入路径(应用不写 CSS 变量、不拼接 `style` 属性)。篡改者需要写权限,而写权限已经等于完全控制 —— 制造一条「高危」项会是对威胁模型的注水 | plan 01 `<threat_model>` | 2026-09-19 |
| AR-02 | T-idi041-02 | 本阶段不新增任何 `url()` / `content:` 汇点,故 CSS 值注入无可达汇点 | plan 01 `<threat_model>` | 2026-09-19 |
| AR-03 | T-idi041-08 | 两个守卫脚本只读仓库内静态文件,不含凭据、网络调用或用户数据 | plan 02 `<threat_model>` | 2026-09-19 |
| AR-04 | T-idi041-13 (plan 03) | harness 只读本地磁盘状态样本与本地应用的 computed style,不含凭据、不外联 | plan 03 `<threat_model>` | 2026-09-19 |
| AR-05 | T-idi041-SC | 四个 plan 均零新增依赖。本机已装 Playwright 1.63.0 与捆绑 chromium-1243,本 run 未跑 `playwright install` | plan 01–04 `<threat_model>` | 2026-09-20 |

*Accepted risks do not resurface in future audit runs.*

---

## Residual Gaps (not open threats — recorded for the record)

These are adjacent gaps surfaced by the incremental code review of plan 04 (`idi-04.1-REVIEW.md`, commit `e3ee082`). They do **not** reopen any threat above: each threat's *stated* mitigation is implemented and verified. They are recorded because they narrow the evidence a future reader might otherwise over-trust.

| Ref | Related Threat | Gap | Current impact |
|-----|----------------|-----|----------------|
| WR-01 | T-idi041-12 (plan 04) | 探针无法区分「自己构造的变异生效了」与「样式表压根没加载」:`route.fulfill(response=resp, body=mutated)` 继承了原始 `content-length` 却发送更短的 body。若该响应被拒绝、CSS 从未应用,四条 `PROBE …` 行仍会全部打印、探针仍 exit 0。 | **当前不成立** —— 实测记录的 `rgb(32, 32, 32)` 是 `--color-text` / `#202020`(`style.css:345-351`),未加样式的页面不可能产生该值(UA 默认 `rgb(0,0,0)`),故变异后的样式表确实生效了。加固建议:剥掉 `content-length` 并补一条 PASS-A 正向对照(`require(h5.resolve_color(page, "--color-text") is not None)`)。 |
| WR-02 | T-idi041-15 (plan 04) | 新的 `expected is None` 分支同时把 4 处 `resolve_token` 期望从 **FAIL** 重新归桶为 **BLOCKED**。`resolve_token` 此前就会返回 `None`,故被删除的 `--z-badge` / `--z-selection-menu` / `--z-banner` 现在读作环境缺口,而非令牌接线断裂。 | 不改变任何实测结论:真实树上没有令牌被删除,`item 4` 仍为 `PASS (24,0,0)`。但这是 plan 04 授权范围(仅修假 PASS)之外的附带判定变更。 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-20 | 21 (20 unique IDs; 4 IDs reused across plans) | 21 | 0 | orchestrator (ASVS L1, short-circuit; register authored at plan time) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-20