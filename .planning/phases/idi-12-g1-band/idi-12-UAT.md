---
status: complete
phase: idi-12-G1 表头 band 与里程碑收口
source: [idi-12-VERIFICATION.md]
started: 2026-09-29T12:35:41Z
updated: 2026-09-29T13:05:00Z
---

## Current Test

[testing complete]

## Tests

### 1. G1 band 的观感确认(局部特写)
expected: |
  打开 .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png。
  `核查报告 2` 下方的表头行(`编号 | 级别 | 位置 | 问题 | 建议修法`)呈现为一档**浅灰底**,
  与周围白色报告面可辨;表头行不再与数据行读感相同。
  合格 = band 看得出是一条独立的横带,而不是与数据行塌成一片。
  注:机械判据只证明两者计算底色不同(rgb(255,255,255) vs rgb(249,249,249));
  band 强度 1.053 是**已被显式接受**的读数,本项只判「看得出」。
result: pass

### 2. VIS-01 整窗观感确认(5 张)
expected: |
  逐张打开 .planning/phases/idi-12-g1-band/screenshots/ 下的
  p1.png / p12.png / p3.png / checking.png / archive.png(各 1440×900)。
  合格 = 整站读作**一张连续白面 + 发丝分隔线**,无卡片边界、无灰缝残留
  —— 即「分块割裂感已消除」。
result: pass

## Summary

total: 2
passed: 2
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps
