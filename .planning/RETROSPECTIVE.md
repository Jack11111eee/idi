# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.13 — 交互式讨论迭代系统 MVP

**Shipped:** 2026-09-13
**Phases:** 3 | **Plans:** 13 | **Tasks:** 28

### What Was Built

- **行走骨架(Phase 1)**:FastAPI 服务器 + 单界面;双轨 AICaller(SDK / `claude -p --output-format stream-json`)界面契约一致;SSE 事件直播(说/读/写/命令/结果/错误/完成七种 kind)+ 中止;`derive_state()` §7.4 八行推导表(文件即状态);阶段 1-2 连续会话与 transcript 恢复;发散模式;G1 定稿为 `discuss-round-1.md`。
- **轮次收敛循环(Phase 2)**:划词批注与大白话即时答双轨;批注回应表回写 `answer`/`status`(AI 不碰 JSON);轮次冻结只读;`grammar.py` §6.4 六条文法解析器 + 正反例测试矩阵。
- **授权、自检与终点(Phase 3)**:G3 四处机械校验 + 确认词 + 后端写 `AUTHORIZATION.md`;`DESIGN.md.tmp` 原子落盘;宽松/严格两档自检、核查者/修复者双角色自动循环;D-22 残余裁决制(纯 P2 轮转用户逐条裁决);崩溃自愈;使命完成只读归档。

**规模:** 155 commits,2026-09-08 → 2026-09-13;13,322 LOC(不含 vendor);15 个测试文件,219 passed / 6 skipped(慢速真 CLI E2E 由 `IDI_E2E=1` 门控)。

### What Worked

- **纵向 MVP 切阶段**:P1 骨架 → P2 收敛循环 → P3 门与终点,每阶段结束都能用真实目录跑通一段端到端流程,验证永远有真实对象可用。
- **真浏览器 UAT(原始 CDP)**:三个阶段的 UAT 共抓出 6 处机器级验证与静态读码都漏掉的真实缺陷,包括一处高危的无界自动链(实测 84 跳/1.5s)。这是本项目最有性价比的验证手段。
- **验证器 + 缺口修复 + 原验证器复验的闭环**:`gaps_found` → 独立复现确认 → 修复分支 → 原验证器复验 → 翻状态,三次(Phase 1/2/3)全部一次收敛。
- **指纹漂移的诚实处理**:Phase 1 与里程碑收口的 Phase 1/2 `covered_digest` 漂移,一律以重新验证刷新指纹收口,而非覆盖状态字段。

### What Was Inefficient

- **plan-checker 三轮迭代**:Phase 3 计划经 3 轮才通过(3B+5W+2I → 1B+3W+1I → PASS),其中多条(如 `AuthorizeBody` 空体 422 陷阱、路由交付权归属)本可在计划阶段一次说清。
- **STATE.md 在 `phase.complete` 后出现字段异常**(`completed_phases: 1`、By-Phase 表重复、进度条 0%),需人工修正——工具侧的状态写入与派生视图未完全对齐。
- **CLI 耗尽窗口**:真实 CLI 调用偶发停滞 20+ 分钟零事件,只能中止重试,期间无法区分"慢"与"死"。
- **用户全局 `settings.json` 的 allow 规则**一度绕过 §5.4 权限门,直到实测才暴露——环境依赖类风险靠读码发现不了。

### Patterns Established

- **两路线必须 `setting_sources=[]`(SDK)/`--setting-sources=`(CLI)**:屏蔽全局 allow 规则,权限矩阵才成立。
- **AI 不写结构化文件**:annotations 字段、`AUTHORIZATION.md`、`DESIGN.md` 改名全由后端执行,AI 只产出内容,格式漂移归零。
- **纯模块 + 薄路由**:`grammar.py`/`annotations.py`/`g3.py`/`checks.py` 无 I/O 依赖、可独立测;路由只做接线与 409 分流。
- **锁定模块的增量演进**:Phase 3 新增解析器只在 `grammar.py` 文件末尾追加,Phase 2 的六个解析器与 `_VERDICT_RE` 字节不变。
- **缺口修复只碰必要文件**:G-idi03-1~4 全部修复仅 3 个文件(session.py/app.js/测试),grammar/state/checks/g3/main/prompts 零改动。

### Key Lessons

1. **门通过 ≠ 语义成立。** D-P3-16 的决策覆盖 gate 报 30/30(它只扫 PLAN/SUMMARY 文本),而同一条决策在运行时是活偏差(G-idi03-1 无界自动链)。任何"文本级 gate"必须配行为验证佐证。
2. **文件即状态的推论要推到边界。** "冻结 = 纯磁盘推导(轮号 < current_round)"和"半成品报告重跑覆盖"这类推论,一旦落到实现就省掉整个状态机——但推论必须在计划期显式写出,否则实现者会各自发明。
3. **锚点与配对空间必须单一口径。** 裁决行的"结论行取末一处"锚点若与展示层的扫描口径不一致(G-idi03-2),界面就会静默隐藏用户必须看到的问题。
4. **预算纪律前置**:单跳调用必须有明确的 hop 上界,否则 `finally` 守卫写反就是无界循环。
5. **Prompt 契约要测**:"函数接受了参数"不等于"参数进了 prompt"(`build_check_prompt` 的 tier 注入缺陷靠真 E2E 才抓到)。

### Cost Observations

- Model mix: 编排器与执行器以 sonnet 为主,验证/审计类子代理用 sonnet 或 opus(按任务深度)
- Sessions: 跨多个会话,期间遭遇 503/429/ENOTFOUND 与 600s 流看门狗停滞,均以恢复或重启代理收敛
- Notable: 真 CLI E2E 是耗时大头(单次真实调用数分钟起),但正是它抓到了 prompt 注入缺陷;慢速测试用 `IDI_E2E=1` 门控,日常套件保持秒级

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.13 | 多会话 | 3 | 首次引入:真浏览器 UAT(原始 CDP)作为强制验证层;验证器+缺口修复+复验闭环;里程碑收口时对漂移指纹做诚实复验 |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.13 | 225(219 passed / 6 skipped) | 20/20 REQ 覆盖(三阶段 VERIFICATION + UAT 全 passed) | vendor 仅 marked.min.js |

### Top Lessons (Verified Across Milestones)

1. 只有一次里程碑,以下为单里程碑内已验证的教训(待后续里程碑复核):门通过须以行为验证佐证;结构化文件由后端写、AI 只产内容;锁定模块只做末尾追加式演进。