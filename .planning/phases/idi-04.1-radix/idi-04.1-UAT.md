---
status: testing
phase: idi-04.1-radix
source: [idi-04.1-VERIFICATION.md]
started: "2026-09-20T03:32:23Z"
updated: "2026-09-20T03:32:23Z"
---

# Phase idi-04.1 — UAT

> 本文件只承载 **VERIFICATION.md 明确标为 `human_verification` 的 3 项**。其余 37 条 must-have 已由验证代理以代码/命令证据逐条核实(`37/38`,`gaps_remaining: []`),不在此重复。
>
> 三项均为**裁决项**(需要人决定,而非"跑一下看通不通"),其中第 3 项是验证代理主动升级的:它不同意 `REQUIREMENTS.md` 对 TOKEN-07 的 `Complete` 标记。

## Current Test

number: 1
name: UI-SPEC 28 条 backstop 陈述
expected: |
  每条陈述在其描述的极端输入下成立;其中 7 条已由 check-02 实测证据覆盖,其余裁切/滚动/换行/缩放行为无自动化证据
awaiting: user response

## Tests

### 1. UI-SPEC `## UI Considerations` 的 28 条 backstop 陈述
expected: 每条陈述在其描述的极端输入下成立;其中 7 条只含 CHECK-02 比值的一半已由 check-02 实测证据覆盖(E1 芯片 4.61–16.29 / E2 闸门标签 11.00 / E4 徽标 4.53 / E6 弱化灰 5.19–5.82 / E7 冻结标记 10.80 / E13 归档 0.75 压暗 6.97 / E10 .tier-desc 满不透明度 4.77),其余裁切/滚动/换行/缩放行为无自动化证据。E1 七芯片不换行/200% 缩放、E2 六按钮行换行与最长闸门标签不裁切、E3 窄面板实心标签不裁切、E4 最长 streaming 串不裁切、E5 文档面板滚动与 #f9f9f9/#fcfcfc 可区分、E6 折行 .hint 与长引用不裁切、E7 冻结轮滚动与琥珀竖线钉边、E8 长致命错误折行、E9 不可断消息撑高与 --shadow-composer 边缘、E10 模态适配视口、E11 大量长批注滚动列表、E12 大量检查项滚动面板、E13 长归档文档不裁切、E14 选区菜单重定位与长菜单项不截断、E15 最长路由标签不截断、E16 跨行 mark 连续段与长 mark 文字可读
why_human: 这些是渲染几何与极端输入下的视觉行为(裁切、换行、滚动归属、200% 缩放、菜单重定位),grep 与 computed-style 读数都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自行标为 `human_judgment: true`,验证报告不把它们静默转绿。
result: [pending]

### 2. E16 的 `--color-text ON --color-surface-mark` 比值归属
expected: ≥ 4.5:1(验证报告实测 15.0:1,通过)
why_human: 该配对**不在**围栏清单里(check-02 因此看不见它),而 plan 01 的 E16 backstop 陈述引用「CHECK-02: --color-text on --color-surface-mark = 15.88」—— 15.88 实为 `--color-text on --color-surface-page` 的数,该引用在 check-02 输出里不存在(见 W-4)。人工须决定是否把该对补进清单,以及该引用如何修正。
result: [pending]

### 3. TOKEN-07 的「断言序关系」半场
expected: 人工决定其一:(a) 接受 `VALIDATION.md` 已记录的 manual-only 处置,并把 `REQUIREMENTS.md` 的 `Complete` 降级/加注,使两文档不再表面一致;或 (b) 按 `check-02-contrast.py` 的 `ORDER` 形式补一条机械断言,把 `--z-badge (10) < --z-banner (20) < --z-overlay (100) < --z-selection-menu (200)` 钉死
why_human: 验证报告已实测:把四个值重新排序后 `check-01`…`check-05` 全部仍会通过。该不变量只存在于 `frontend/style.css:229-231` 的散文注释里(该注释自称 `z-index ordering assertion (TOKEN-07)`,但断言并不存在);`check-05-ui-uat.py:771-776` 断言的是「元素 `z-index` **等于**其令牌」,不是「令牌之间的大小序」。用户已在 `VALIDATION.md` 里裁定本阶段不加断言,故这是裁决项而非验证报告单方面翻转的缺口 —— 但 `Complete` 的标记在机械层面**不成立**,不得静默调和。
result: [pending]

## Summary

total: 3
passed: 0
issues: 0
pending: 3
skipped: 0
blocked: 0

## Gaps

<!-- 尚无失败项。若第 3 项裁定为 (b) 补断言,则在此追加一条 gap 供 /gsd-plan-phase --gaps 消费。 -->