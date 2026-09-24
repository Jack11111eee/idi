---
status: testing
phase: idi-08-accessibility-semantics-and-keyboard
source: [idi-08-VERIFICATION.md]
started: 2026-09-24T13:23:27Z
updated: 2026-09-24T13:23:27Z
---

## Current Test

number: 1
name: A11Y-08 — Tab 序到达每一个交互控件
expected: |
  每一个交互控件都能被 Tab 到达;新增的 #round-doc 停靠点位于第 2 位(紧接 #round-switcher 之后,
  #authorize-row 可见时紧邻 #btn-authorize 之前)。
awaiting: user response

## Tests

### 1. A11Y-08 — Tab 序到达每一个交互控件

**步骤:** 打开一个 phase-3 项目与一个 phase-5 自检项目,各按一轮 Tab,逐格核对。

expected: |
  每一个交互控件都能被 Tab 到达;#round-doc 停靠点位于第 2 位
  (紧接 #round-switcher 之后、#authorize-row 可见时紧邻 #btn-authorize 之前)。

why_human: |
  机器半场已完成且全绿(check-05 --item 10:`[p3] 判定集 10 个元素,未覆盖 []`;SUMMARY 自报
  p3 10/10、checking 8/8),但「每一个交互控件」是**跨状态的屏幕枚举**,而 harness 不采样
  archive 状态(item 10 的样本集硬编码为 p1/checking/p3,到不了 archive)。

result: [pending]

### 2. A11Y-03 键盘划词那一半 — Shift+方向键扩选,再松开 Shift

**步骤:** Tab 到文档区 → 按住 Shift 按方向键扩选到超过一个字符 → 松开 Shift → 再按 Escape。

expected: |
  选区扩到超过一个字符,菜单出现,焦点落在 #btn-annotate;随后 Escape 关闭菜单、
  把焦点交还 #round-doc,且**选区存活**(还能接着 Shift+方向键继续扩选)。

why_human: |
  本环境无法自动化键盘文本选区(连 contenteditable 都选不中)。按 ROADMAP Phase 8 §Manual checks,
  这一条上的自动非结果**不构成功能缺陷判定**。

result: [pending]

### 3. REG-03 — b9664e0 五条修复的人工验收项重跑

**步骤:** 按 idi-08-03-SUMMARY.md §REG-03 observation record 逐条重跑第 1、2、3、5、6 条,
以及重写后的第 4 条 step 3。

expected: |
  六条 b9664e0 人工验收项的表现与 SUMMARY 03 §REG-03 observation record 所记录的一致。

why_human: |
  依赖键盘选区的几条(第 4 条的扩选步、其余几条的键盘起点变体)无法自动化;执行器已机器观测
  1/2/4/5 条通过,并显式把 step 3 交给人。

result: [pending]

### 4. 六条 backstop UI-consideration 真值(E1…E6)

**步骤:** 对 E1 (#round-doc) / E2 (#selection-menu) / E3 (#confirmation-modal) / E4 (#tier-modal) /
E5 (#app) / E6(其余三个弹窗),逐条确认 loading / error / overflow / long-text / empty / partial
六种考虑项。

expected: |
  每一条被声明为 backstop 的考虑项,要么有可观察的契约,要么被确认对该元素**不适用**。

why_human: |
  这些在计划 frontmatter 里被声明为 `verification: backstop` —— 规划期**弃权**而非承诺判据,
  故没有可对照的规格。多数确实不适用(静态 div、两按钮菜单、#app),但那是**裁定**不是**测量**。

result: [pending]

### 5. phase-5 视图下零高度的 #round-doc Tab 停靠点

**步骤:** 打开一个 phase-5 自检态项目(SUMMARY 03 §Deviation 2),Tab 到 #round-doc。

expected: |
  裁定:一个 351 × 0 的 Tab 停靠点(环渲染成一条细横线)是可接受的,还是应当把该属性改为条件性挂载。

why_human: |
  执行器登记但未修(条件性属性会改变计划 01 的交付物)。这是**设计决策**,不是测量。

result: [pending]

## Summary

total: 5
passed: 0
issues: 0
pending: 5
skipped: 0
blocked: 0

## Gaps

(none — the single automated gap, Phase 6's L-5 clearance gate, was adjudicated by the user and
resolved in `63fba08`; see `idi-08-VERIFICATION.md` §Gap Resolution)
