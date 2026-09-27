---
phase: idi-10-tables-and-radius-scale
plan: 04
subsystem: ui
tags: [verification, fingerprint, staleness, carry-forward, known-limitation, table, radius]

# Dependency graph
requires:
  - phase: idi-10-tables-and-radius-scale
    provides: 本阶段对 frontend/style.css 的两处改动(表格规则改造 + 圆角刻度收敛)与其五条浏览器门复跑证据(计划 01 / 02 / 03)
  - phase: idi-09-card-containers
    provides: 待重验的报告 .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md 及其 10 条 covered_files / 24 条 must-have
provides:
  - 连带指纹真实形状的逐份实测落定:覆盖 frontend/style.css 的 passed 报告恰 10 份,其中 covered_files 路径全部可解析的恰 1 份(idi-09)
  - idi-08 不在名单的独立证据(其 frontmatter 命中 0 / 全文命中 19)⇒ 判据必须锚 frontmatter 逐行匹配而非全文 grep
  - 9 份归档/quick 报告 fail-closed stale 的逐份成因(路径归档迁移)+ 逐份缺失数(12/41…2/7)+ 抽查 ≥2 份的一一对应
  - idi-09-VERIFICATION.md 以 HEAD 内容重新验证:24 条 must-have 逐条复核、covered_digest 重算、status 由 stale 回到 passed
affects: [idi-10 收口验证, 未来任何改动 frontend/style.css 的计划]

# Actuals (#2632) —— 同一 estimateTokens 口径(chars/4 over the realized diff)。
# 口径:本计划**零产品代码、零门代码**改动,手写产物 = 1 份新日志 + 1 份就地改写的报告。
# 按「实际产出的文本 diff」计量:git diff a131568..HEAD -- <两个文件> = 39775 字符 / 4 = 9943。
actuals:
  tokens: 9943
  tasks: 2
  commits: 2
  plan_head_before: a13156802d81924a67017aa6f0dec7624b940581

tech-stack:
  added: []
  patterns:
    - "「覆盖面」与「可执行面」是两个不同的问题:前者锚报告 frontmatter 的 covered_files 逐行匹配,后者额外要求那些路径仍在盘上;只看前者会把 10 份都算成债务,只看后者会把唯一该重验的那份漏掉"
    - "判定一份报告是否 stale,「内容真变」与「路径不可解析」两种成因的补救方向相反:前者要重新验证(重跑判据 + 重算摘要),后者要修归档路径引用;机器判据 `verification.status` 对两者都返回 stale,必须逐份实测成因"
    - "重新验证的凭据是「旧摘要 ≠ 新摘要」并排留证 —— 相同就说明内容没变、重验不必要;不同才证明覆盖输入真的变了,故刷新指纹是不实陈述"
    - "被移动的历史读数(计划改变量必然移动)必须在重验正文里逐条给出机制,不能静默沿用;判据是「主张的实质是否仍成立」,而不是「那个数字是否仍相等」"

key-files:
  created:
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/verification-recheck.log
  modified:
    - .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md

key-decisions:
  - "覆盖面判据锚 frontmatter 的 covered_files 逐行匹配 `  - frontend/style.css` 且 status: passed —— 全文 grep 会把只在正文提及该文件的报告算进来(idi-08 就是那个假阳性:其 frontmatter 命中 0、全文命中 19)"
  - "真实形状是「10 份覆盖,1 份可执行」:9 份归档/quick 报告的 covered_files 路径在归档时由 .planning/phases/<id>/… 迁到 .planning/milestones/<ver>-phases/<id>/… ⇒ 重算失败关闭 ⇒ 它们在 Phase 10 之前就已是 stale,与本次改动无关"
  - "本阶段只重验 idi-09 一份,处置法是「以 HEAD 内容重新验证」而不是刷新指纹:frontend/style.css 确实变了,刷新等于断言「自验证以来覆盖输入无变化」"
  - "idi-09 的 covered_files 10 条逐条未变(条数判据 == 10 且其中 frontend/style.css == 1);只重算 covered_digest —— 删条目是让报告假装新鲜的典型手法"
  - "两条被本阶段改动移动的历史读数逐条给出机制而非静默重述:truth 5 的 --color-border 消费者计数 3→2(第三个消费者被 D-10-1 就地改写)、truth 24 的顶层选择器计数 173→174(Phase 10 追加了一条 .markdown-body th)"
  - "idi-09 正文对 #round-doc 绝对高度的引用为零 ⇒ 计划 03 登记的 -3px 几何变化不触及本报告任何判据;其唯一的几何引用 #doc-panel 的 scrollHeight 2488 > clientHeight 898 在 HEAD 上复测仍为 2488/898"

patterns-established:
  - "连带指纹分诊的三步法:①锚 frontmatter 逐行匹配枚举覆盖名单;②逐份跑 verification.status 与 verification.fingerprint(后者失败关闭,不产出部分指纹);③对失败份逐份实测「缺失数/总数」并抽查成因,把「已知限制」落到逐份证据上"
  - "「以 HEAD 内容重新验证」的机器判据是 verification.status 由 stale 回到 passed;其内容判据是 covered_digest 与重算值逐字符相同、且与旧值不同"
  - "计划里声称「零改动 / 逐值相同」时,把**被改动文件自身的历史读数**与**其余读数**分开核:本计划实测到两条历史读数被本阶段改动移动,而它们指向的事实并未改变"

requirements-completed: [REG-03]

coverage:
  - id: D1
    description: "连带指纹的真实形状以逐份实测落定:覆盖 frontend/style.css 的 passed 报告恰 10 份,其中 covered_files 路径全部可解析的恰 1 份(idi-09);idi-08 不在名单内且有两条并排计数作独立证据(frontmatter 命中 0 / 全文命中 19)"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "find .planning/{phases,milestones/*-phases,quick} -name '*VERIFICATION.md' + awk 取 frontmatter 逐份判定 ⇒ 11 份报告,恰 10 份 status:passed 且 frontmatter 含 '  - frontend/style.css';idi-08 为 fm_style=0 / fulltext=19"
        status: pass
      - kind: other
        ref: "gate-logs/verification-recheck.log §A(枚举表)/§B(idi-08 探测器)"
        status: pass
    human_judgment: false
  - id: D2
    description: "9 份归档/quick 报告的 stale 成因是路径而非内容,逐份取证:每份 verification.status = stale、verification.fingerprint 以 'could not compute fingerprint' 失败关闭、缺失数逐份实测(12/41、11/26、13/31、8/13、8/12、8/11、8/10、6/9、2/7),并抽查 3 份核实原 .planning/phases/<id>/… 与归档 .planning/milestones/<ver>-phases/<id>/… 一一对应"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <9 个 phase dir> ⇒ 9/9 stale;query verification.fingerprint ⇒ 9/9 fail-closed rc=1"
        status: pass
      - kind: other
        ref: "gate-logs/verification-recheck.log §C(逐份缺失数 + idi-04 / quick 260925-iin / idi-01 三份的归档对应件实测)"
        status: pass
    human_judgment: false
  - id: D3
    description: "idi-09-VERIFICATION.md 以 HEAD 内容重新验证:24 条 must-have 逐条复核(24/24 成立)、covered_files 10 条逐条未变、covered_digest 由 6e811a11… 重算为 7b82f8d1…、status: passed、score: 24/24、re_verification 块三个空列表;verification.status 由 stale 回到 passed"
    requirement: "REG-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5 ⇒ exit=0,c1:26 / c2:13 / c3:3 / c4:4 / c5:5,0 FAIL / 0 BLOCKED"
        status: pass
      - kind: other
        ref: "node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers ⇒ {\"status\": \"passed\"}"
        status: pass
      - kind: other
        ref: "query verification.fingerprint 重算值 == frontmatter 的 covered_digest(逐字符相同)且 != 旧值 6e811a11…"
        status: pass
    human_judgment: false
  - id: D4
    description: "未越界:本计划只改动 idi-09-VERIFICATION.md 一个既有文件;其余 9 份报告、frontend/ 全部文件、scripts/ 全部文件(尤其 scripts/check-05-ui-uat.py)零字节改动"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "git diff -- scripts/check-05-ui-uat.py 为空;git status --porcelain .planning/milestones/ .planning/quick/ frontend/ scripts/ 为空;git diff --stat <报告> 只列该一个文件"
        status: pass
    human_judgment: false

duration: 14 min
completed: 2026-09-27
status: complete
---

# Phase 10 Plan 04: 连带指纹收口(10 份覆盖 / 1 份可执行)与 `idi-09` 的 HEAD 重验 Summary

**实测落定连带指纹的真实形状是「10 份覆盖 `frontend/style.css`,1 份可执行」—— 9 份归档/quick 报告因 `covered_files` 路径归档后不可解析而 fail-closed stale(与本次改动无关,属 2026-09-14 登记的已知限制),唯一可执行的 `idi-09` 以 HEAD 内容重新验证(非刷新指纹):24 条 must-have 逐条复核 24/24 成立,`covered_digest` 由 `6e811a11…` 重算为 `7b82f8d1…`,`verification.status` 由 `stale` 回到 `passed`**

## Performance

- **Duration:** 14 min
- **Started:** 2026-09-27T12:22:52Z
- **Completed:** 2026-09-27T12:36Z
- **Tasks:** 2
- **Files modified:** 2(1 新建日志 + 1 就地改写的报告);产品代码与门代码**零改动**

## Accomplishments

- **覆盖面判据锚对了。** 判据定义为「报告 **frontmatter** 的 `covered_files` 里恰有一行匹配 `  - frontend/style.css`,且 `status: passed`」—— 不是全文 grep。在 `.planning/phases/` + `.planning/milestones/*-phases/` + `.planning/quick/` 下全部 **11 份** `*VERIFICATION.md` 上逐份判定,命中**恰 10 份**。
- **`idi-08` 假阳性探测器的两条并排计数落证。** 其 frontmatter 段内对 `frontend/style.css` 命中 **0**;全文命中 **19**。文件确在盘(排除「文件缺失导致 0」这一伪因)。⇒ 全文 grep 会把 `idi-08` 误算进来,故判据不能锚全文。
- **9 份归档/quick 报告的 stale 成因是路径,不是内容 —— 逐份取证。** 每份 `verification.status` 返回 `stale`,`verification.fingerprint` 以 `Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root` **失败关闭**(`rc=1`,不产出部分指纹)。逐份缺失数实测为 **12/41、11/26、13/31、8/13、8/12、8/11、8/10、6/9、2/7**,与 `10-CONTEXT.md` 的规划期读数**逐字相符**。
- **成因抽查 3 份,一一对应。** `idi-04`(v1.14)、quick `260925-iin`、`idi-01`(v1.13)的每一条缺失路径,其原位置 `.planning/phases/<id>/…` 的归档对应件都在 `.planning/milestones/<ver>-phases/<id>/…` 上存在 ⇒ 归档迁移,不是内容变化。
- **`idi-09` 是唯一可执行的一份,且它的 stale 是「内容真变」。** `covered_files` 10/10 全部在盘(缺失 0),`verification.fingerprint` 成功返回 `v1:sha256:7b82f8d1…`,与 frontmatter 现存的 `v1:sha256:6e811a11…` **不同** ⇒ 覆盖输入确实变了(本阶段改了 `frontend/style.css`),故必须**重新验证**而不是刷新指纹。
- **`idi-09-VERIFICATION.md` 以 HEAD 内容重新验证完成。** 24 条 must-have **逐条**以 HEAD 重新推导,24/24 成立;`covered_files` 10 条逐条未变;`covered_digest` 重算;`status: passed`;`score: 24/24 must-haves verified`;`re_verification:` 块记录 `previous_status: passed` / `previous_score: 24/24` 与三个空列表;正文新增「Phase 10 re-verification」一节,**点名 `frontend/style.css`** 为唯一被本阶段改动的 `covered_file` 并逐条记明改了什么。
- **机器判据达成:** `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` 由 `stale` 回到 **`passed`**。
- **零越界。** `git diff -- scripts/check-05-ui-uat.py` 为空;`git status --porcelain .planning/milestones/ .planning/quick/ frontend/ scripts/` 为空;本计划只改动 `idi-09-VERIFICATION.md` 一个既有文件。

## Task Commits

Each task was committed atomically:

1. **Task 1: 连带指纹的「10 份覆盖 / 1 份可执行」分诊 —— 逐份实测证据** - `35f046e` (test)
2. **Task 2: `idi-09-VERIFICATION.md` 以 HEAD 内容重新验证(不是刷新指纹)** - `82211b2` (docs)

**Plan metadata:** 见本次收口的 docs 提交

## Files Created/Modified

- `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/verification-recheck.log`(新建,435 行 / 20933 字节)- 10 份报告的逐份原始输出(`verification.status` + `verification.fingerprint`)+ frontmatter 命中计数 + 逐份缺失数 + §A 枚举表 / §B idi-08 探测器 / §C 成因抽查 / §D 已知限制原文 / §E 新旧摘要并排
- `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md`(+96 / −8)- frontmatter 重签(`verified` / `covered_digest` / `re_verification`) + 正文新增「Phase 10 re-verification (2026-09-27)」一节 + truth 5 / truth 24 两行的 HEAD 复核注 + Gaps Summary 一段

## Gate Evidence(原始输出,不是摘录)

### 覆盖面枚举(11 份报告逐份)

```
REPORT                                                                                status  fm_style  fulltext
.planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md                        passed     1          2
.planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md                         passed     1          2
.planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md                         passed     1          1
.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md         passed     1         11
.planning/milestones/v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md               passed     1         18
.planning/milestones/v1.14-phases/idi-05-.../idi-05-VERIFICATION.md                     passed     1         15
.planning/milestones/v1.14-phases/idi-06-.../idi-06-VERIFICATION.md                     passed     1         19
.planning/milestones/v1.14-phases/idi-07-.../idi-07-VERIFICATION.md                     passed     1         15
.planning/milestones/v1.14-phases/idi-08-.../idi-08-VERIFICATION.md                     passed     0         19   <-- FALSE POSITIVE
.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md                          passed     1          8
.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md                   passed     1          6
```

### `verification.status` × 10(原始 JSON,tr -d '\n')

```
v1.13/idi-01-1-2  {"status": "stale", "next_action": "Verification is stale. Re-run verify-work before transition.", "next_command": "/gsd-verify-work"}
v1.13/idi-02-g2   {"status": "stale", ...}
v1.13/idi-03-g3   {"status": "stale", ...}
v1.14/idi-04      {"status": "stale", ...}
v1.14/idi-04.1    {"status": "stale", ...}
v1.14/idi-05      {"status": "stale", ...}
v1.14/idi-06      {"status": "stale", ...}
v1.14/idi-07      {"status": "stale", ...}
phases/idi-09     {"status": "stale", ...}     # ← 重验前;Task 2 之后为 passed
quick/260925-iin  {"status": "stale", "next_command": "/gsd-verify-work 260925"}
phases/idi-10     {"status": "missing"}        # 本阶段自身尚未收口(上下文,非名单成员)
```

### `verification.fingerprint` × 10(9 份失败关闭 / 1 份成功)

```
# 9 份归档 / quick 报告,逐份:
Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root
rc=1

# idi-09(成功):
{
  "covered_files": [ ... 10 条,逐条与 frontmatter 相同 ... ],
  "covered_digest": "v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031"
}
rc=0
```

### 逐份缺失数(本次实测,与 10-CONTEXT 的规划期读数逐字相符)

```
#  report                                  missing/total
1  idi-01-1-2 (v1.13)                        12/41
2  idi-02-g2 (v1.13)                         11/26
3  idi-03-g3 (v1.13)                         13/31
4  idi-04-tokens-contract (v1.14)             8/13
5  idi-04.1-radix (v1.14)                     8/12
6  idi-05-typography-and-visual-hierarchy     8/11
7  idi-06-layout-robustness                   8/10
8  idi-07-interaction-states-and-focus        6/9
9  idi-09-card-containers                     0/10    <-- 全部在盘
10 quick/260925-iin-v1-14-ai-999-1            2/7
```

### 新旧摘要并排(「内容确实变了」的直接证据)

```
stored in idi-09-VERIFICATION.md frontmatter (before this re-verification):
  v1:sha256:6e811a1122c2e6d5c63308554a39c5d2d8dce462abef73847f0c7be39e2bb89e
recomputed on HEAD:
  v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031
```

### 重验时重跑的判据(原始读数)

```
$ .venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5
item c1: PASS  (26 条断言,0 FAIL,0 BLOCKED)
item c2: PASS  (13 条断言,0 FAIL,0 BLOCKED)
item c3: PASS  (3 条断言,0 FAIL,0 BLOCKED)
item c4: PASS  (4 条断言,0 FAIL,0 BLOCKED)
item c5: PASS  (5 条断言,0 FAIL,0 BLOCKED)
exit=0

$ .venv/bin/python scripts/probe-card-border-token.py
PASS 令牌可区分: --color-border != --color-border-subtle(rgb(206, 206, 206) != rgb(217, 217, 217))
PASS 卡片边界 #session-panel / #annotations-panel / #checks-panel / #ai-panel / #doc-panel: 5/5 rgb(206, 206, 206)
PASS 非卡片边界对照 .event-list / #latest-check: 2/2 rgb(217, 217, 217)
PROBE RESULT: PASS(exit=0)

$ bash scripts/check-01-token-conformance.sh   → PASS (rc=0)
$ bash scripts/check-03-hidden-uniqueness.sh   → PASS (rc=0)
$ bash scripts/check-04-important-count.sh     → PASS (rc=0)
$ .venv/bin/python scripts/check-02-contrast.py
PASS  15.48  --color-text on --color-surface                    # 表头新绘制面的既有条目
PASS  4.77  --color-marker-active on --color-surface-card       # 修正案重归属的两条
PASS  3.32  --color-border-strong on --color-surface-card
ORDER 0.363  --color-text-muted before --color-text on --color-surface
PASS: 0 failures

$ .venv/bin/python -m pytest backend/tests -q --tb=short
219 passed, 6 skipped, 1 warning in 6.29s

$ node --check frontend/app.js                                   (exit=0,零输出)
$ .venv/bin/python scripts/probe-05-resolve-color.py             (exit=0;control-verdict=PASS)
$ .venv/bin/python scripts/probe-07-focus-composite.py           (exit=0;ratio=3.54 (>= 3.0))
```

`check-05` / `check-06` / `check-07` 三份引用 `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` 里计划 03 的本阶段新鲜输出(`check-05` `exit=2` 按设计、十项 0 FAIL、BLOCKED 仅 item 5 两条 `--ai-smoke` 腿;`check-06` g1…g6 = 9/2/12/5/5/7 条 0 FAIL;`check-07` g1…g4 = 21/39/10/3 条 0 FAIL)。**该引用成立:** `git diff --stat a98c788..HEAD -- frontend/ scripts/` **为空** ⇒ 那些门读取的输入与 HEAD 逐字节相同。

### 重签的机器判据

```
$ node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers
{"status": "passed", "next_action": "Verification passed — continue.", "next_command": ""}

$ awk '/^---$/{n++} n==1' <报告> | grep -c '^  - frontend/style.css$'   → 1
$ awk '/^---$/{n++} n==1' <报告> | grep -c '^  - '                        → 10
stored covered_digest   = v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031
computed covered_digest = v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031   MATCH
```

## 24 条 must-have 的逐条复核结论(判据 / 本次读数或引用来源 / 成立与否)

全部 **24/24 成立**。下表是每条判据与本次在 HEAD 上的读数或来源。

| # | 判据(缩写) | 本次读数 / 来源 | 结论 |
|---|---|---|---|
| 1 | 左栏 4 section 计算底色 = 卡片白 | 本进程重跑 `check-09 --item c1`:4/4 `rgb(255,255,255)`,26 条断言 0 FAIL | ✓ |
| 2 | 4 section 圆角 10px / 四边 1px solid / 阴影非 none | 同上 c1:`border-top-left-radius=10px`、`border-top=1px solid`、两层 `box-shadow` | ✓ |
| 3 | 卡片间隙 = 12px 且透出 gray-3 | 本进程重跑 `check-09 --item c4`:`#main-pane` gap = 12px PASS | ✓ |
| 4 | 卡片边界色 = `--color-border`(206) | 本进程重跑 `probe-card-border-token.py`:5/5 卡片 `rgb(206,206,206)`,令牌可区分 PASS | ✓ |
| 5 | 修正案改动面严格两处卡片;四处非卡片 subtle 消费者一字未动 | 四处仍为 `.event-list`(`:929`)/ `.annotation-item`(`:1320`)/ `.badge-answered`(`:1371`)/ `#latest-check`(`:1530`),计数仍 **4**;`--color-border` 消费者现为 2(两处卡片)—— 第三处被 Phase 10 的 D-10-1 就地改写,**见下方说明** | ✓ |
| 6 | `#doc-panel` 与左栏同族卡片 | 本进程重跑 `check-09 --item c2`:13 条断言 0 FAIL;`grep -n 'border-left: 1px solid'` 零命中 | ✓ |
| 7 | `#doc-panel-header` 底色卡片白 + sticky 保持 | `frontend/style.css` 的 `#doc-panel-header` 规则仍 `background: var(--color-surface-card)`;`check-05 --item 8` 的 sticky 读数(计划 03 日志)与 Phase 9 逐字相同 | ✓ |
| 8 | `#doc-panel` 计算 `overflow-y` 仍 `auto` | c2 与 c5 各一条 PASS;c5 的可滚前提复测为 `scrollHeight=2488 clientHeight=898` —— **与报告引用的 2488/898 逐值相同** | ✓ |
| 9 | `body` 底色 = gray-3 且来自令牌 | c3 两条互为对照 `rgb(240,240,240)` PASS | ✓ |
| 10 | 三档亮度严格递增 | c3 令牌级 `0.871367 < 0.947307 < 1.000000` 与报告逐位吻合 | ✓ |
| 11 | D-9-2 密度:`gap` 12px / `.panel-body` 16px | c4 四条 PASS(含两条对照组) | ✓ |
| 12 | 卡片令牌落在围栏 `:root` 内 + check-01 | 令牌 `:334` / `:335` 落在围栏 `:5` → `:695` 之间;`check-01` 本进程重跑 `PASS` | ✓ |
| 13 | 零新增 tier-1 原语 | `--color-surface-card: var(--white)`(`:334`)、`--white: #ffffff`(`:47`);`git diff -U0 27fbf20..HEAD` 新增行里 `--radix-` 计数 = **0**;`check-01` PASS | ✓ |
| 14 | 卡片圆角取自既有刻度、零新增圆角值 | `--radius-sm: 8px` / `--radius-md: 10px` / `--radius-pill: 999px` 三条值未变;`var(--radius-lg)` 全文计数 = **0** | ✓ |
| 15 | `--shadow-card` 零位移 | `:335` 逐字两层值,两层 offset-x 均 `0`;c1/c2 分量断言 PASS | ✓ |
| 16 | 卡片规则体不含九项禁令属性 | 本次重新按块边界提取:`#main-pane > section` = width/max-width/background/border/border-radius/box-shadow;`#doc-panel` = flex/display/flex-direction/overflow-y/border/background/border-radius/box-shadow/min-width;禁令属性 **NONE** | ✓ |
| 17 | `check-02` 全部对比度对达标 | 本进程重跑:`PASS: 0 failures`;53 PASS + 1 ORDER;`^FAIL` 计数 0 | ✓ |
| 18 | 登记是「重算」而非「刷新」 | 台账比值本次实跑复现:`14.30`(page)/`5.19`(muted on page)/`4.18`(marker-active on page)/`4.77`/`3.32`(卡片白侧);`git diff 27fbf20..HEAD -- scripts/check-02-contrast.py` 为空 | ✓ |
| 19 | 两条跌破阈值的配对重归属到卡片底色 | 两条 `PAIR … ON --color-surface-card` 在 `:632` / `:643`(报告写 `:624` / `:635`,同 +8 行漂移);check-02 打印 `PASS 4.77` / `PASS 3.32`;`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同;`PAIR=53` / `ORDER=1` | ✓ |
| 20 | `check-05` 全量十项 FAIL 计数全 0、exit 2、BLOCKED 仅 item 5 | 计划 03 的 `gate-logs/check-05-full.log`(输入与 HEAD 逐字节相同):十项 0 FAIL、`exit=2`、仅有的 2 条 BLOCKED 都带 `--ai-smoke` 提示 | ✓ |
| 21 | `check-06` / `check-07` / `probe-05` / `probe-07` 退出码全 0 | `check-06`(g1…g6 = 9/2/12/5/5/7 条 0 FAIL)/ `check-07`(g1…g4 = 21/39/10/3 条 0 FAIL)引计划 03 日志;`probe-05` / `probe-07` **本进程重跑**均 exit=0 | ✓ |
| 22 | 四个静态门 PASS + pytest 基线 + `node --check` | 本进程重跑:`check-01/03/04` 三 × PASS;`check-02` `PASS: 0 failures`;pytest **219 passed, 6 skipped**;`node --check` exit=0 零输出 | ✓ |
| 23 | 无门被弱化;两条守卫是真守卫 | `git diff -- scripts/check-05-ui-uat.py` **为空**;`check-09` 的 `ok(` / `ok_true(` / `blocked(` 调用点计数 = **21 / 6 / 6**;`SHADOW_CARD_LITERAL` 仍是裁定值且以严格等值比较;探针的令牌可区分前置判据仍在(206 ≠ 217) | ✓ |
| 24 | 编辑纪律:追加不重排、`app.js`/`index.html`/`vendor/` 零字节改动、截图交付、开放项清单 | 相位基线 vs **Phase 9 HEAD** 的顶层选择器序列仍 **173 = 173**;今日 HEAD 为 **174**(Phase 10 自己追加的唯一一条 `.markdown-body th`,零删除零重排);`git diff 27fbf20..HEAD -- frontend/app.js frontend/index.html` 为空;`ls frontend/vendor/` 仅 `marked.min.js`;两个截图目录各 5 张 PNG、IHDR 全 `1440x900`、相位 9 的字节数逐张相同(88685/123949/123449/68115/124136);4 条开放项静态复核仍为开放 | ✓ |

**Score: 24/24 truths verified(0 present-behavior-unverified)**

## 两条被移动的历史读数(逐条给出机制,不静默重述)

本计划对 `frontend/style.css` **零改动**,但它重验的是一份写于 Phase 9 的报告,而 Phase 10 的计划 01/02 改过该文件。逐条核 24 条判据时,发现**两条历史读数**被那些改动移动 —— 它们指向的事实未变,数字变了:

| # | 读数 | 报告值 | HEAD 值 | 机制 |
|---|---|---|---|---|
| 1 | `grep -c 'border: 1px solid var(--color-border);'`(truth 5) | 3 | **2** | 第三个消费者 `.markdown-body th, .markdown-body td` 被 Phase 10 的 D-10-1 就地改写为 `border: none` + `border-bottom`。它**不属于**该行主张的「四处非卡片 `--color-border-subtle` 消费者」—— 那四处仍是 4 条、仍是同样四个规则,故该行主张的**实质**成立 |
| 2 | 顶层选择器序列(truth 24) | 173 = 173 | Phase 9 对仍 173 = 173;今日 HEAD **174** | 多出的 1 条是 Phase 10 自己**追加**的 `.markdown-body th`(唯一新增、零删除、零重排)。`173 = 173` 那一对比较的是 `3ec6558` 与 `27fbf20`,今天仍然相同;今日 HEAD 之所以是 174 是因为其上又叠了 Phase 10 的合规追加 |

两处都**不是**「主张不再成立」,故 `gaps_remaining` / `regressions` 为空;两处都已在报告正文与 truth 5 / truth 24 两行的证据格里显式标注(保留原读数 + 追加 HEAD 读数与机制)。

## 计划 03 登记的 `#round-doc` −3px 是否触及本报告的判据 —— 核实结论:不触及

计划 03 实测 `#round-doc` 高度由 `778.640625` 变为 `775.640625`(3 张表各矮 1px)。**本报告对 `#round-doc` 绝对高度的引用为零**(`grep -nE '#round-doc|778|775'` 在报告里只命中 truth 8 的 `#doc-panel` 一处,且那是**另一个元素**)。其唯一几何引用 `#doc-panel` 的 `scrollHeight 2488 > clientHeight 898` 本次重跑 c5 复测为 **2488 / 898** —— 逐值不变。其余几何读数(`check-05 --item 8` 的 sticky 坐标、`L-2` 三宽度溢出 0px、`docPanelWidth` 432/340/340)都在 `#doc-panel` / `#doc-panel-header` 上,且在计划 03 与 Phase 9 的 `check-05-full.log` 里逐字相同。⇒ **−3px 不触及本报告任何判据**,已写入报告的「Phase 10 re-verification」一节。

## 为什么本阶段只重验 1 份(以及为什么其余 9 份不在边界内)

1. **覆盖 ≠ 债务。** 10 份报告**声明**覆盖 `frontend/style.css`,但只有 1 份的 `covered_files` 路径全部可解析。9 份的 `verification.fingerprint` 因路径缺失而**失败关闭**,不产出部分指纹 ⇒ 它们的 `covered_digest` 在归档那一刻起就已无法复核,**在 Phase 10 之前就是 stale**,与本次改动无关。
2. **这是已登记的已知限制。** `.planning/STATE.md` 的 `## Deferred Items` 有一条 `known-limitation`(Deferred At **2026-09-14**):「已归档阶段的 `covered_digest` 不可解析:`covered_files` 声明 `.planning/phases/...` 路径,归档后移至 `.planning/milestones/v1.13-phases/`,重算返回 `null`(fail-closed=stale)。归档后的阶段报告不再被 staleness 机制消费,故记为已知限制而非回填重算」。
3. **修补它们是另一件已登记的 backlog 事项,不是本阶段的活儿。** 要让那 9 份重新可复核,须先把它们 `covered_files` 里的归档前路径引用改写到归档后位置 —— 那会改动 9 份已归档报告的内容,属独立事项。本阶段**不得**改动它们的任何字节(已用 `git status --porcelain .planning/milestones/ .planning/quick/` 为空核实)。
4. **Phase 9 的先例同形。** Phase 9 改同一文件时也只在 live 树内重验了 `idi-09` 一份(见 `idi-09-VERIFICATION.md` 的 `re_verification:` 块与正文),其余覆盖该文件的报告同批因路径原因被排除。

## Decisions Made

- **覆盖面判据锚 frontmatter 逐行匹配,不锚全文 grep。** `idi-08` 的两条并排计数(frontmatter 0 / 全文 19)是这条判据的**探测器** —— 它证明全文 grep 会误报,故判据必须锚结构化的 `covered_files` 列表行。
- **「10 份覆盖」与「1 份可执行」必须分开报。** 只报 10 会把 9 份已登记的已知限制重新算成债务;只报 1 会掩盖「理论上 10 份都受影响」这一事实。两条判据都要给,且都要逐份证据。
- **重验 = 重跑判据 + 重算摘要 + 正文点名被改动的覆盖输入,不是刷新指纹。** 旧摘要与新摘要并排留证(`6e811a11…` → `7b82f8d1…`)是「内容确实变了」的直接凭据;刷新等于断言「自验证以来覆盖输入无变化」,那是不实陈述。
- **`covered_files` 10 条逐条未变,只重算 `covered_digest`。** 删条目是让报告假装新鲜的典型手法,故把「条数 == 10 且其中 `frontend/style.css` == 1」写成机器判据。
- **两条被移动的历史读数在报告正文与对应证据格里都显式标注,保留原读数并追加 HEAD 读数与机制。** 不删、不改判据、不静默沿用。
- **`check-05` / `check-06` / `check-07` 允许引用计划 03 的日志,前提是给出「输入未变」的机器证据。** 该证据是 `git diff --stat a98c788..HEAD -- frontend/ scripts/` 为空 —— 不是记忆,也不是「看起来没变」。

## Deviations from Plan

**None —— 计划逐条执行。** 两条任务的所有 `<verify>` 与 `<acceptance_criteria>` 均在 HEAD 上实跑通过;零产品代码改动、零门改动、零范围变化。计划对两条「历史读数会被移动」的情况没有预判(它只预警了 `#round-doc` 的 −3px),本计划按 prohibition「不得静默重述过期数字」的要求把它们作为**重验发现**逐条写进报告正文与 SUMMARY,未改任何判据。

## Issues Encountered

- **首版日志里 `idi-09` 的 fingerprint 被误记为失败关闭。** 首轮生成日志的 shell 循环里,`$args` 在 zsh 下**不做单词切分**(zsh 与 bash 的差异),10 条路径被当成**一个**参数传入 ⇒ 命令看到一条不存在的路径 ⇒ 假 fail-closed。发现方式:同一条命令在循环外逐字手打 10 个路径时**成功**返回 `v1:sha256:7b82f8d1…`。修法:改用 zsh 数组 `cfiles=(${(f)"…"})` 展开,并**整份重生成**日志(未做局部修补,避免同一文件里两种口径并存)。⇒ 与 STATE.md 已登记的「先怀疑自己的探针」同族:门报红先逐字复测原命令。
- **`gsd-tools windows append` 未使用。** 本计划零 stub、零跳过测试、零未跑的 `<verify>`、零 deviation,无跨阶段缺陷需登记进 `WINDOWS.md`。
- **`state.*` 动词第十五次复现**(见 STATE.md 本次新增条目),已逐条核盘修正。核盘放在收口序列的**最后一个动词之后**。

## Known Stubs

None —— 本计划未引入任何 stub、占位文案或硬编码空值。新增的日志是 10 份报告查询输出的**完整原文**(含失败关闭的完整报错);报告的重签只改 frontmatter 的四个字段与正文的增补段落,24 条 must-have 一条未删、一条未改判据。

## Threat Flags

None —— 本计划**零产品代码改动、零新增依赖、零网络调用**。`<threat_model>` 的五条 `mitigate` 项逐条落地:

| Threat ID | 缓解计划 | 实测 |
|---|---|---|
| T-idi-10-01(刷新指纹冒充重验) | 正文新增节点名被改动的 `covered_file`;`<verify>` 强制重跑 `check-09 c1…c5` 且要求 `exit=0`;24 条逐条复核并写进 SUMMARY;`covered_files` 条数判据 == 10;新旧摘要并排留证 | ✅ 全部落地:`exit=0`、10 条未变、`6e811a11…` ≠ `7b82f8d1…`、24/24 逐条表在 SUMMARY |
| T-idi-10-02(误改 `check-05-ui-uat.py` 把重验面从 1 变 2) | `<prohibitions>` 明令;`<verify>` 要求 `git diff -- scripts/check-05-ui-uat.py` 为空;并给出 `idi-08` 的独立证据 | ✅ `git diff` 为空;`idi-08` frontmatter 命中 0 |
| T-idi-10-03(误改其余 9 份报告) | 只写 `idi-09-VERIFICATION.md`;`<verify>` 要求 `git status --porcelain .planning/milestones/ .planning/quick/` 为空 | ✅ 输出为空;9 份零字节改动 |
| T-idi-10-04(报告与日志内容) | 只含令牌值 / 几何读数 / 本地路径 | ✅ 无用户数据、无凭据、无网络内容 |
| T-idi-10-05(权限提升) | 不触碰鉴权 / 权限门 / 服务端路径 / API | ✅ 本计划零代码改动 |
| T-idi-10-SC(安装) | 本阶段零安装 | ✅ 零 pip / npm 安装;`frontend/vendor/` 仍只有 `marked.min.js` |

## Next Phase Readiness

- **Phase 10 的四个计划全部收口。** 计划 04 是本阶段最后一个:`verification.status idi-09` 已由 `stale` 回到 `passed`;`REG-03` 由本计划触发勾选(`requirements.ready-ids` 实测 `ready: [REG-03]`,其余四条已由计划 03 勾选)。
- **读者可用 `gate-logs/verification-recheck.log` 独立复现「10 份覆盖 / 1 份可执行」的每一步**:§A 枚举表 → §B `idi-08` 探测器 → §C 逐份缺失数与成因抽查 → §D 已知限制原文 → §E 新旧摘要并排;重签的机器判据在 `## Gate Evidence` 的「重签的机器判据」块。
- **待决出口(非缺陷):** 用户评审(表格形态是否读作「白卡片内的一个内陷块」、`.chat-user` 的 10px 圆角是否与卡片语言同族、四条 Phase 9 开放项是否另开 phase)与 `/gsd-verify-work idi-10`。本计划不代其收口。
- **给未来改 `frontend/style.css` 的计划的提示:** 该文件在 10 份 `passed` 报告的 `covered_files` 里,但只有 `idi-09` 一份是 live 且可复核的;其余 9 份是已登记的已知限制。**不要**为了让 `verification.status` 变绿去改写它们的归档路径 —— 那是独立 backlog 事项。

## Self-Check: PASSED

- `gate-logs/verification-recheck.log` 与 `idi-09-VERIFICATION.md` 均在盘
- `git log --oneline --all` 含 `35f046e`(Task 1)/ `82211b2`(Task 2);`commits: 2` 由 `git rev-list --count a131568..HEAD` **实测**(非叙述),`plan_head_before: a131568…` 取自落盘 ledger
- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` 返回 `"status": "passed"`
- 报告的 `covered_files` 条数 = 10、其中 `frontend/style.css` = 1;`covered_digest` == 重算值且 != 旧值
- 零越界:`git diff -- scripts/check-05-ui-uat.py` 为空、`git status --porcelain .planning/milestones/ .planning/quick/ frontend/ scripts/` 为空

---

*Phase: idi-10-tables-and-radius-scale*
*Completed: 2026-09-27*
