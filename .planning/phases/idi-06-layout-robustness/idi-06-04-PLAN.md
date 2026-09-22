---
phase: idi-06-layout-robustness
plan: 04
type: execute
wave: 4
depends_on: [idi-06-01, idi-06-02, idi-06-03]
files_modified:
  - scripts/check-05-ui-uat.py
  - .planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md
  - .planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md
autonomous: true
gap_closure: true
gap_ids: [G-idi-06-1, G-idi-06-2]
requirements: [LAYOUT-01, LAYOUT-02, LAYOUT-03, LAYOUT-04, A11Y-07]
estimate:
  tokens: 28000
  raw_tokens: 28000
  tasks: 3
  confidence: low
must_haves:
  truths:
    - "scripts/check-05-ui-uat.py 的 768px 分支(只读 info() 那一支)不再声称 badge × banner 断言覆盖了 LAYOUT-02 的「无内容遮挡」承诺;它改写成显式「未覆盖」,并携带实测数值(h1 439.0–481.0 × 8–28 vs banner 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px)。"
    - "打开 :1931-1946 的读者能读出四件事:LAYOUT-02 的 768px 承诺原本是什么、它被收窄了、证伪它的精确数值是什么、收窄登记在哪里(idi-06-UI-SPEC.md §L-2 / A-10)。"
    - "idi-06-UI-SPEC.md 的契约修正登记表新增 A-10 行(不改 A-1…A-9 的编号),登记 768px 承诺收窄为「badge 不被横幅遮挡」、收窄理由(范围锁把几何修复排除在阶段可修范围外)、实测证伪数值与 768–855px 相交带,并显式声明它跟随 A-5 先例、是有意偏离而非静默通过。"
    - "idi-06-UI-SPEC.md §L-2 的判据表(:192)被就地注解:明说三对判据里只有 badge × banner 被测量过,另两对(表头 × 正文、按钮 × 视口)在本阶段从未被测量、收窄后的承诺也不主张它们;表格行不被删除、不被重排。"
    - "idi-06-VERIFICATION.md frontmatter 的 overrides: 数组里存在一条 must_have 为「LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡」的条目,accepted_by 与 accepted_at 均已填实(不再是「{待人工填写}」),且 overrides_applied 仍为 0(留给复验时应用)。"
    - "idi-06-03-PLAN.md 与 idi-06-03-SUMMARY.md 里那三处失效的覆盖主张被就地追加【更正 2026-09-22】注记,原句仍可见,注记点明实测真相与收窄的登记处;两文件不被重排、不被删句。"
    - "本计划执行后,check-05-ui-uat.py 的既有通过断言一条未弱化、未删除、未被放宽标签:--item 8 的断言数 ≥13、--item 9 的断言数 ≥16,且 1440/1024 两条硬断言逐字保留。"
    - "零 diff 不变量成立:frontend/style.css、frontend/index.html、frontend/app.js、frontend/vendor/、.planning/REQUIREMENTS.md、.planning/ROADMAP.md 在本计划结束后均无改动。"
  artifacts:
    - path: "scripts/check-05-ui-uat.py"
      provides: "768px 分支的诚实覆盖主张(显式「未覆盖」+ 实测数值)"
    - path: ".planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md"
      provides: "A-10 收窄登记行 + §L-2 判据表注解"
    - path: ".planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md"
      provides: "填实的 override 条目"
    - path: ".planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md"
      provides: "失效覆盖主张的就地更正注记"
    - path: ".planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md"
      provides: "失效覆盖主张的就地更正注记"
  key_links:
    - from: "scripts/check-05-ui-uat.py:1931-1946"
      to: ".planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md §L-2 / A-10"
      via: "覆盖主张文本里显式点名收窄的登记处"
      status: "must be wired"
    - from: "idi-06-VERIFICATION.md overrides[0].must_have"
      to: "idi-06-VERIFICATION.md gaps[0].truth(「LAYOUT-02 后半句:≥768px 无内容遮挡」)"
      via: "复验时按 fuzzy matching(≥80% token 重叠)匹配到该 truth"
      status: "must be wired"
  prohibitions:
    - "MUST NOT 触碰 frontend/style.css 里 #stream-banner 的任何声明(:709-723)—— 那是 UI-SPEC :665 的范围锁,理由是「不得靠移动横幅来通过」。"
    - "MUST NOT 改动 --doc-panel-w 的值(frontend/style.css:224-227 记载其值由用户裁决,执行器不得自行改动)。"
    - "MUST NOT 写出任何 @media 守卫(唯一合法形态需要面板 ≤285.3px,低于 340px 的 clamp 下限,几何上不可能)。"
    - "MUST NOT 在本计划中改动 frontend/style.css、frontend/index.html、frontend/app.js、frontend/vendor/(三者必须零 diff)。"
    - "MUST NOT 为让措辞编辑更容易而弱化、删除或放宽 check-05-ui-uat.py 里任何既有的通过断言(尤其 1440/1024 两条硬断言与 :1834 的 badge × banner 断言)。"
    - "MUST NOT 编辑 .planning/REQUIREMENTS.md 或 .planning/ROADMAP.md(改会作废已通过的验证指纹;跟随 A-5 先例,收窄只登记在计划与验证记录里)。"
    - "MUST NOT 把 768px 分支从只读 info() 升为断言(那是被本次用户裁定排除的 remediation (a))。"
    - "MUST NOT 把 overrides_applied 从 0 改成 1 —— 该计数由复验器在应用 override 时更新。"
  decisions:
    - "D-USER-idi06-close-(b):项目所有者本次会话显式选择 remediation (b)「Narrow the promise, fix the claim」。本计划是该选择的完整实现,范围已封闭。"
    - "D-01(本计划honor):以磁盘 HEAD 为唯一现实基线;不动 04-UI-SPEC.md / ROADMAP.md 正文。本计划据此只登记收窄、不改路线图。"
    - "D-06(本计划honor):check-05 item 8 的 badge × banner 三宽度不相交断言逐字保留;本计划只更正围绕它的覆盖主张,不弱化断言。"
    - "D-08(本计划honor):L-2 的判据在 1440 / 1024 / 768 三处量,遮挡与溢出一同是 768px 的判据;本计划把遮挡半句的实测真相写进覆盖主张,而不是把它读窄后静默通过。"
    - "D-19(本计划honor):本计划不编辑 frontend/style.css,故不新增对 idi-04.1-radix 指纹的扰动;既有的连带复验义务由 plan 03 履行。"
    - "其余 CONTEXT 决策(D-02…D-05、D-07、D-09…D-18、D-20)由已完成的 plan 01 / 02 / 03 实现与覆盖(验证报告已确认 20/20 被已交付产物覆盖);本计划是 gap-closure 轮,不重新实现它们。"
---

<!-- planner-discipline-allow: 不相交断言覆盖 -->
<!-- planner-discipline-allow: 439.0 -->
<!-- 上述两个 allowlist 的必要性:本计划的 action 必须逐字给出被替换的旧主张片段(否则执行器无法定位)与实测数值(否则执行器无从写对);而 verify 的负向门与正向门必然以同一字面量为判据。这不是注释文风问题,是「改的就是这段字面量」的任务性质。 -->

<objective>
把 LAYOUT-02 的 768px 承诺按项目所有者的显式裁定收窄,并更正本阶段新增的失效覆盖主张 —— 让阶段自己的验收门说实话。

Purpose: 项目既定纪律是「不看就报 PASS 的门比没有门更糟」。`scripts/check-05-ui-uat.py` 的 768px 分支声称 LAYOUT-02 的「无内容遮挡」承诺已被 badge × banner 不相交断言覆盖,而该断言(:1834)只测 `#state-badge`,在真实遮挡存在的宽度上干净地 PASS。这条主张阻止下一个读者去看,是 `idi-06-VERIFICATION.md` 两条 `gaps` 中 G-idi-06-2 的对象,也是 `idi-06-REVIEW.md` CR-01 的同一发现。几何本身(768–855px 下 fixed 居中横幅盖住 `#doc-panel-header` 的 h1)是既有的,且被 UI-SPEC 的范围锁排除在阶段可修范围之外,故按用户裁定登记为已知缺口、不修。

Decision traceability: 本计划实现用户本次会话的显式裁定 remediation (b)(D-USER-idi06-close-(b)),并 honor 06-CONTEXT 的 D-01(磁盘 HEAD 为唯一基线,不动 ROADMAP 正文)、D-06(item 8 的 badge × banner 三宽度断言逐字保留)、D-08(1440 / 1024 / 768 三处量,遮挡与溢出一同是 768px 的判据)、D-19(不编辑 `frontend/style.css`,不新增指纹扰动)。其余 CONTEXT 决策由已完成的 plan 01 / 02 / 03 实现与覆盖(验证报告确认 20/20),本 gap-closure 轮不重新实现它们。

Output:
- `scripts/check-05-ui-uat.py` 的 768px 分支改为显式「未覆盖」并携带实测数值
- `idi-06-UI-SPEC.md` 新增 A-10 收窄登记行 + §L-2 判据表注解
- `idi-06-VERIFICATION.md` frontmatter 填入 override 条目(accepted_by / accepted_at 填实,overrides_applied 仍为 0)
- `idi-06-03-PLAN.md` / `idi-06-03-SUMMARY.md` 的就地更正注记
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md
@.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md
@.planning/phases/idi-06-layout-robustness/idi-06-REVIEW.md
@.planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md
@scripts/check-05-ui-uat.py
@.claude/gsd-core/references/verification-overrides.md
</context>

<gap_context>
`idi-06-VERIFICATION.md` 的 frontmatter 恰有两条 `gaps`(均 `status: failed`,均无 `id` 字段,本计划分别铸为 **G-idi-06-1** / **G-idi-06-2**):

**G-idi-06-1** — truth:「LAYOUT-02 后半句:≥768px 无内容遮挡」。实测证伪:768px 视口下 `#stream-banner`(`position: fixed`、`z-index: 20`、不透明 `rgb(255,247,194)`)完整压住 `#doc-panel-header h1`(文本「文档区」)。h1 = 439.0–481.0 × 8–28;banner = 285.3–482.7 × 12–39;水平 42/42px 全覆盖、垂直 16/20px 覆盖;四次 `elementFromPoint` 采样全部返回 `#stream-banner`。相交带 768 ≤ vw ≤ 855(856 起不相交)。几何既有,`frontend/index.html` 本阶段零 diff。

**G-idi-06-2** — truth:「本阶段的验收门自身诚实:item 8 的 768px 分支声称的覆盖范围 == 它实际测量的范围」。主张措辞为本阶段新增(`git diff` 确认 :1932-1933 与 :1945-1946 为 `+` 行),它把事实说反了。

**用户裁定(绑定,范围已封闭):** remediation **(b)「Narrow the promise, fix the claim」** —— 登记 768px 承诺收窄到 badge 对(A-5 风格,只登记在计划与验证记录),更正 :1932-1933 / :1945-1946 的失效覆盖主张使其陈述实测真相,并把 768–855px 遮挡登记为已知缺口。**不做任何布局改动**,留在 UI-SPEC 范围锁之内。

**明确不做:** remediation (a)(不新增会 FAIL 的 banner × header 相交断言)、不动 `#stream-banner` 声明、不改 `--doc-panel-w` 的值、不写 `@media` 守卫。`frontend/style.css` / `index.html` / `app.js` 本计划结束时必须零 diff。

**复验说明(供下一个读者):** 编辑 `idi-06-03-PLAN.md` / `idi-06-03-SUMMARY.md` / `idi-06-VERIFICATION.md` 会改变验证记录 `covered_files` 里列出的文件,故下次验证时 `covered_digest` 必然不同。**这是 gap-closure 轮的预期结果** —— 后续验证是一次全新的复验(`re_verification.previous_status` 会记录上一次状态),不是漂移失败。不要把指纹变化误读为缺陷。
</gap_context>

<carried_advisories>
以下五项在 `idi-06-VERIFICATION.md` 的 `advisory:` 里已登记,且明确不阻塞本阶段。**本计划不为它们排任何工作,也不调查它们** —— 一行登记,然后继续:

- **WR-01** — `_idi06_reach` 的前提链只拒绝 `injected is None`;整数 `0` 会通过,故末条断言可能记一次空转 PASS。潜伏项(今日注入 40/60)。
- **WR-02** — L-5 clearance 断言测的是滚动位置而非裁切。**作为陈述已被推翻**(见下方禁令):该过滤恰恰排除了部分滚出容器的行,评审自引的证据(`#btn-authorize`、`intersects=False`)正证明该排除。真正的残留关切是:三个样本之所以确定,只因 `enter_project` 重载页面、面板恒从 `scrollTop = 0` 开始 —— 这条性质没有任何断言守着。
- **WR-03** — `DOC_PANEL_W_MIN_PX / _VW / _MAX_PX` 是 `frontend/style.css:228` 的硬编码镜像、无绑定;收窄 clamp 会让探针静默失去判别力。
- **IN-01** — `_idi06_census` 的 docstring 声称 item 9 消费其返回值;item 9 从不调用它,唯一调用点丢弃返回值。
- **IN-02** — `@media` 守卫统计的是任意位置的子串 `@media`(含注释),标签却声称它编码了 L-2 决策。
</carried_advisories>

<flagged_assumptions>
本阶段五个需求 ID 的确定性边界探针(ADR-857 Phase 6 的无 SPEC 回退)全部返回 `unclassified` / `unresolved`。这是探针在中文散文上的已知局限(其 cue 匹配是英文的),与本阶段此前各规划波次的结果一致。按回退规则的 **no-silent-drop equality**:`unclassified` 行保持 `unresolved`,**绝不**用 backstop 自动解决,**绝不**静默丢弃。逐行登记如下,并**不**由这些行铸造任何边界谓词:

- **LAYOUT-01** — 探针无法分类(英文 cue vs 中文散文的局限);该需求的真实验证状态取决于本阶段自己的 harness(check-05 item 8 的流内机制断言),不取决于任何探针派生的谓词。
- **LAYOUT-02** — 探针无法分类(同上局限);真实验证状态取决于本计划收窄后的覆盖主张与 item 8 的硬断言,不取决于探针谓词。
- **LAYOUT-03** — 探针无法分类(同上局限);真实验证状态取决于 item 8 的 `position == static` + `right == auto` 两条断言。
- **LAYOUT-04** — 探针无法分类(同上局限);真实验证状态取决于 item 9 的滚动者 DOM 普查。
- **A11Y-07** — 探针无法分类(同上局限);真实验证状态取决于 item 9 的命中区普查(其覆盖边界见 `carried_advisories` 之外的 verification advisory 末条)。
</flagged_assumptions>

<tasks>

<task type="tracer">
  <name>Task 1: 让 768px 分支说出实测真相(检查门自身诚实)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <action>
    改 `scripts/check-05-ui-uat.py` 的两处覆盖主张,使其陈述实测真相。**追加式编辑,不重排周围代码块**(项目纪律「Hard Rule 3 追加,不重排」)。← D-08(768px 的遮挡判据必须诚实)/ D-06(badge × banner 断言逐字保留)

    第一处 —— `:1931-1933` 的注释块。它的前两行(L-2 字面承诺「≥1024px 无横向溢出」升为硬断言)逐字保留;只重写第三行(即声称 768px 处承诺已被前文那条断言覆盖的那一行)。第二处 —— `:1944-1946` 的 `info()` 串(768px 走 `else` 分支时打印的运行时文本)。

    两处替换文本必须满足:

    1. 明说 badge × banner 断言**只覆盖 badge 那一对**;768px 下真正发生遮挡的那一对(banner × `#doc-panel-header` 的 h1)**不在覆盖范围内**,写成显式「未覆盖」。
    2. 携带实测数值,让下一个读者不必重测:h1 = 439.0–481.0 × 8–28,banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px。
    3. 点名这是**已知缺口**,并说明收窄已登记在 `idi-06-UI-SPEC.md` §L-2(A-10 行)。
    4. **不得读成 PASS。**读者读完必须知道 LAYOUT-02 的 768px 遮挡半句**既未满足、也未断言**。
    5. 768px 分支**保持只读** —— 仍是 `info()`,不是新的断言(这是选项 (b),不是 (a))。

    以下东西**逐字不动**:`:1934` 的 `if width >= 1024:` 与 `:1935-1942` 的 `ok_true(...)`(1440/1024 两条硬断言);`:1947-1964` 的 `#doc-panel` 判别性探针;`:1968-1969` 的 `_l2_guard_shape(item)`;`:1834` 的 badge × banner 断言(既不改标签也不改判据)。

    **禁止:** 改动本文件任何既有的通过断言(弱化 / 删除 / 放宽标签);新增断言;触碰 `frontend/style.css` / `index.html` / `app.js` / `vendor/`;写出 `@media` 守卫。

    运行时验证(硬规则 7):实跑 `--item 8` 与 `--item 9`,确认两者仍 PASS 且断言数不降(当前 13 / 16);再把逐项结论与两处新措辞抄进 SUMMARY。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8</automated>
    <fails_when>非零退出,或输出里出现 "FAIL" / "BLOCKED",或总结行的断言数小于 13</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 9</automated>
    <fails_when>非零退出,或输出里出现 "FAIL" / "BLOCKED",或总结行的断言数小于 16</fails_when>
    <automated>grep -c '不相交断言覆盖' scripts/check-05-ui-uat.py</automated>
    <fails_when>输出不是 0(该失效主张在注释与代码里各有一处,两处都必须消失)</fails_when>
    <automated>grep -c '439.0' scripts/check-05-ui-uat.py; grep -c '285.3' scripts/check-05-ui-uat.py; grep -c '855' scripts/check-05-ui-uat.py</automated>
    <fails_when>任一条输出为 0(实测数值未落进措辞)</fails_when>
    <automated>git diff --name-only -- frontend/</automated>
    <fails_when>输出里出现任意一行(frontend 下出现了改动)</fails_when>
  </verify>
  <done>768px 分支的两处覆盖主张都改写成显式「未覆盖」并携带实测数值与 768–855px 相交带,点名已知缺口与 §L-2 / A-10 的登记处;`:1934-1942` 的 1440/1024 硬断言与 `:1834` 的 badge × banner 断言逐字未动;`--item 8` 与 `--item 9` 仍 PASS 且断言数为 13 / 16;`frontend/` 零 diff。</done>
</task>

<task type="auto">
  <name>Task 2: 在 UI-SPEC 登记收窄(A-10 行 + §L-2 判据表注解)</name>
  <files>.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md</files>
  <action>
    跟随 **A-5 先例**(本文件 `:568`):措辞收窄只登记在计划与验证记录里 —— **不编辑 `.planning/REQUIREMENTS.md` 与 `.planning/ROADMAP.md`**,因为改它们会作废已通过的验证指纹。全部编辑**追加式**,不重排、不删除。← D-01(磁盘 HEAD 为唯一基线;不动 ROADMAP 正文)

    **(1) 契约修正登记表(`:560-575`)** 追加新行 **A-10**(表内既有 A-1…A-9,**不重排、不重新编号**)。A-10 行记录:

    - 收窄对象:LAYOUT-02 的 768px 承诺,由「无内容遮挡」收窄为「badge 不被横幅遮挡」。
    - 理由:该遮挡是**既有几何**,且被本阶段自己的范围锁排除在可修范围之外 —— `#stream-banner` 的声明被锁(`:665`)、`--doc-panel-w` 的值由用户裁决(`frontend/style.css:224-227`)、唯一合法的 `@media` 形态在几何上不可能(需面板 ≤285.3px,而 clamp 下限是 340px)。
    - 实测证伪数值与相交带:h1 439.0–481.0 × 8–28 vs banner 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px。
    - 它跟随 A-5 先例,且是**已登记的偏离,不是静默通过**;依据一栏写「用户本次会话显式裁定 remediation (b)」。

    **(2) §L-2(`:185-200`)** 就地注解,使判据表不再暗示它并不具备的覆盖。`:192` 的表格行在「无内容被遮挡」下列了三对:「badge × banner、表头 × 正文、按钮 × 视口」。验证报告已确立:**只有 `badge × banner` 被测量过**,另两对在 `scripts/check-05-ui-uat.py` 或任何探针里零命中。**不删该行、不重排表格**;在该行下方(或紧邻)加注解,逐对说明:这两对在本阶段**从未被测量**,且收窄后的承诺**不主张**它们 —— 因为 768px 承诺已收窄到 badge 对。注解须让读者看出「原承诺是什么、收窄到什么、由谁授权」。

    写法是**可见的登记**,不是静默改动:读者打开 UI-SPEC 必须能看到承诺原本是什么、被收窄成了什么、依据谁的裁定。
  </action>
  <verify>
    <automated>grep -c 'A-10' .planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md</automated>
    <fails_when>输出为 0(A-10 行未落盘)</fails_when>
    <automated>grep -n 'badge 不被横幅遮挡' .planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md</automated>
    <fails_when>无输出(收窄后的措辞未落盘)</fails_when>
    <automated>grep -c '表头 × 正文' .planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md</automated>
    <fails_when>输出为 0(判据表行被删而不是被注解)</fails_when>
    <automated>git diff --name-only -- .planning/REQUIREMENTS.md .planning/ROADMAP.md</automated>
    <fails_when>输出里出现任意一行(改了会作废验证指纹的文件)</fails_when>
  </verify>
  <done>UI-SPEC 的契约修正登记表新增 A-10 行(不重排 A-1…A-9),登记收窄对象、理由(含范围锁三处依据)、实测数值与 768–855px 相交带、A-5 先例与用户裁定;§L-2 的判据表行被就地注解,明说三对里只有 badge × banner 被测量过、另两对从未测量且收窄后的承诺不主张它们;`REQUIREMENTS.md` / `ROADMAP.md` 零 diff。</done>
</task>

<task type="auto">
  <name>Task 3: 填实 override 条目 + 更正历史记录里的失效主张</name>
  <files>.planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md, .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md, .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md</files>
  <action>
    **(1) 填实 override(`idi-06-VERIFICATION.md` frontmatter)。** 验证器已在报告正文(约 `:276-282`)写下模板,并**刻意留空** `accepted_by: "{待人工填写}"` / `accepted_at: "{待人工填写}"`,因为验证器不是接受方。接受方是项目所有者 —— 他本次会话通过**显式选择 remediation (b)** 完成了接受。按 `.claude/gsd-core/references/verification-overrides.md` 的格式,在 frontmatter 的 `overrides:` 数组里写入这一条(字段值逐字如下,`must_have` 字符串已核对可 fuzzy-match 到 `gaps[0].truth`):

    ```yaml
    overrides:
      - must_have: "LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡"
        reason: "768–855px 下 fixed 居中横幅盖住 #doc-panel-header 的标题;几何既有且被 UI-SPEC 范围锁(#stream-banner 声明不得触碰 / --doc-panel-w 值由用户裁决)排除在阶段可修范围之外。经项目所有者本次会话显式选择 remediation (b)(收窄承诺 + 更正覆盖主张)后,本条登记为已知缺口,收窄为「badge 不被横幅遮挡」。"
        accepted_by: "Jack11111eee"
        accepted_at: "2026-09-22T06:43:50Z"
    ```

    `accepted_by` 取仓库的 git 身份(`git config user.name`),这是接受方唯一可用的标识;`accepted_at` 是本次会话裁定的时间戳。

    **不要**设置 `overrides_applied: 1` —— 该计数由复验器在应用 override 时更新,本计划**保持它为 0**,以便复验时应用该 override 并产出 `PASSED (override)`。

    **provenance 必须显式可见**(在报告正文模板处补一行,并在 SUMMARY 里重述):本次接受来自用户对 remediation (b) 的**显式选择**,不是执行器的单方裁定。后续读者必须能看出这一点。

    **(2) 就地更正历史记录(`idi-06-03-PLAN.md` 与 `idi-06-03-SUMMARY.md`)。** 同一失效主张被抄进了三处:`idi-06-03-PLAN.md:37`、`:212`,以及 `idi-06-03-SUMMARY.md:150`(均声称 768 处的只读诊断已被 badge × banner 不相交断言覆盖)。该措辞是本阶段新增的且事实为假 —— **记录里的假主张与代码里的同害**(它让下一个读者不再去看)。

    更正方式:**就地追加式**。保留原句可见,紧接其后追加一条可见的 **「【更正 2026-09-22】」** 注记,写明:(i) 原句的覆盖主张为假;(ii) 实测真相(h1 439.0–481.0 × 8–28 vs banner 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px);(iii) 收窄登记在 `idi-06-UI-SPEC.md` §L-2 / A-10,并指向 `idi-06-04-PLAN.md`。

    **不重排、不重构、不删原句** —— 记录应同时显示「当时声称了什么」与「它实际是什么」。两个文件其余部分零改动。← D-01(只登记,不改会作废指纹的文件)
  </action>
  <verify>
    <automated>grep -c 'accepted_by: "Jack11111eee"' .planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md</automated>
    <fails_when>输出不是 1(override 条目的接受方未填实)</fails_when>
    <automated>grep -c '待人工填写' .planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md</automated>
    <fails_when>输出不是 0(仍有未填的占位)</fails_when>
    <automated>grep -c 'overrides_applied: 0' .planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md</automated>
    <fails_when>输出不是 1(计数被越权改成 1)</fails_when>
    <automated>grep -c '【更正 2026-09-22】' .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md; grep -c '【更正 2026-09-22】' .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md</automated>
    <fails_when>任一条输出为 0(历史记录里的失效主张未更正)</fails_when>
    <automated>grep -c '不相交断言覆盖' .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md</automated>
    <fails_when>输出不是 2(原句被删除而非保留+更正;两处原句必须仍在)</fails_when>
  </verify>
  <done>VERIFICATION.md frontmatter 的 overrides 数组含一条 must_have 为「LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡」的条目,accepted_by / accepted_at 填实、无「{待人工填写}」残留、overrides_applied 仍为 0,且正文里 provenance 显式说明接受来自用户对 (b) 的显式选择;idi-06-03-PLAN.md 与 idi-06-03-SUMMARY.md 的三处失效主张各带一条可见的「【更正 2026-09-22】」注记,原句仍在,两文件其余部分零改动。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 本计划 → 验收门自身 | 被修改的对象正是「判定改动是否合格」的那段代码/文本;执行器可以在此处制造一个更安静而非更诚实的门 |
| 本计划 → 验证记录 | 填入 override 会让一条失败的 must-have 在复验时计为通过;越权填 `overrides_applied` 会跳过复验的应用步骤 |
| 执行器 → 范围锁 | 措辞编辑可能顺手「修好」几何,越过 UI-SPEC :665 的锁 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-06-04-01 | Tampering | `scripts/check-05-ui-uat.py:1931-1946` | high | mitigate | Task 1 的 `<verify>` 同时把「旧主张计数 == 0」与「实测数值计数 > 0」都做成可执行门;`--item 8` / `--item 9` 的断言数下限(13 / 16)机器化地抓「顺手弱化既有断言」 |
| T-idi-06-04-02 | Repudiation | `idi-06-VERIFICATION.md` overrides 条目 | medium | mitigate | `accepted_by` 必须是仓库 git 身份、`accepted_at` 是本次会话时间戳,且 provenance 在正文与 SUMMARY 双处显式写明「来自用户的显式选择」;`overrides_applied` 保持 0,强制复验器走应用路径 |
| T-idi-06-04-03 | Elevation of Privilege | `frontend/style.css` 范围锁 | high | mitigate | Task 1 的 `<verify>` 含 `git diff --name-only -- frontend/` 必须无输出;`must_haves.prohibitions` 显式登记四条范围锁禁令 |
| T-idi-06-04-04 | Tampering | `.planning/REQUIREMENTS.md` / `ROADMAP.md` | medium | mitigate | Task 2 的 `<verify>` 含对这两文件的 `git diff --name-only` 必须无输出(A-5 先例:改它们会作废验证指纹) |
| T-idi-06-04-05 | Information Disclosure | — | low | accept | 本计划只改仓库内的规划与探针文本,不引入新数据面、无网络面、无用户输入面;无适用威胁 |
| T-idi-06-04-SC | Tampering | 依赖安装 | low | accept | 本计划零新增依赖、零包管理器调用,故包合法性门不适用 |
</threat_model>

<verification>
**本计划结束时的整体验收(全部可执行):**

1. `git diff --name-only` 的输出**恰为**五个文件:`scripts/check-05-ui-uat.py`、`.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md`、`idi-06-VERIFICATION.md`、`idi-06-03-PLAN.md`、`idi-06-03-SUMMARY.md`。
2. `git diff --name-only -- frontend/ .planning/REQUIREMENTS.md .planning/ROADMAP.md` 无任何输出行。
3. `.venv/bin/python scripts/check-05-ui-uat.py --item 8` PASS 且断言数 == 13;`--item 9` PASS 且断言数 == 16。
4. `.venv/bin/python scripts/check-05-ui-uat.py`(无参全量门)PASS。
5. `bash scripts/check-01-token-conformance.sh`、`.venv/bin/python scripts/check-02-contrast.py` 与 `check-03` / `check-04` 全 PASS(措辞编辑不得扰动任何静态门)。
6. 负向门:`grep -c '不相交断言覆盖' scripts/check-05-ui-uat.py` == 0;正向门:`grep -c '439.0' scripts/check-05-ui-uat.py` > 0。
7. override 门:`accepted_by: "Jack11111eee"` 命中 1 次;`待人工填写` 命中 0 次;`overrides_applied: 0` 命中 1 次。
8. 更正门:两个历史文件各命中「【更正 2026-09-22】」≥1 次,且 `idi-06-03-PLAN.md` 里原句仍命中 2 次(被保留而非删除)。
</verification>

<success_criteria>
**读者测试(本计划唯一的成功判据):** 任何人在本计划执行后打开 `scripts/check-05-ui-uat.py:1931-1946`,都能读出四件事 ——(1) LAYOUT-02 的 768px 承诺原本是什么;(2) 它被收窄了;(3) 证伪它的精确实测数值;(4) 收窄登记在哪里。底层布局**零改动**。

**门的诚实性:** 768px 分支不再声称它不具备的覆盖;既有的通过断言一条未弱化、未删除;断言计数不降。

**登记的可见性:** UI-SPEC 的读者能看到承诺原本是什么、收窄成什么、依据谁的裁定(A-10 行 + §L-2 注解);验证记录的读者能看到接受来自用户对 remediation (b) 的显式选择,而非执行器的单方裁定。

**零 diff 不变量:** `frontend/style.css` / `index.html` / `app.js` / `vendor/`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md` 全部零 diff。
</success_criteria>

<output>
Create `.planning/phases/idi-06-layout-robustness/idi-06-04-SUMMARY.md` when done.

SUMMARY 必须重述:override 的 provenance(接受来自用户对 remediation (b) 的显式选择,`accepted_by` = 仓库 git 身份、`accepted_at` = 本次会话时间戳、`overrides_applied` 保持 0 留给复验),以及复验说明(编辑 `idi-06-03-*` / `idi-06-VERIFICATION.md` 会改变 `covered_files` 的指纹,这是 gap-closure 轮的预期结果,不是漂移失败)。
</output>