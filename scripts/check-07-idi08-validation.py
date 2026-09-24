#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-07-idi08-validation.py — idi-08 的 Nyquist 验证缺口补齐(4 条**行为**断言)。

为什么另开一个文件
    idi-08 的三个计划,其 `<verify>` 块对 A11Y-05 / A11Y-06 / A11Y-03 只有**静态 grep**
    (数某个词在源文件里出现几次)。计数门能证明「一个词出现在文件里」,不能证明
    「行为在运行时存在」——它分辨不出属性落在**哪个**元素上、也分辨不出监听器是否真的
    响应按键(本阶段已实测记录过:锚在行号上会去改错的弹窗,而五个计数门全部照旧为绿)。
    在 check-07 之前,`Escape` 这个词在 `scripts/` 与 `backend/tests/` 里出现次数为 **0**,
    即这三条需求在本文件之前**零自动化覆盖**。

    本文件的四条断言全部是真实浏览器里的**行为/几何**读数,不是源码文本匹配。

四条断言与需求的映射
    g1 → A11Y-05   受信 Escape 真的关闭三个可关对象(两个阻塞弹窗 + 划词菜单),
                   且其余三个弹窗**刻意不响应**(范围锁);含「非 Escape 按键不关闭」的判别控制
    g2 → A11Y-06   两个弹窗各自带 dialog 语义三件套,且无障碍名称**解析得出来**
                   (指向存在的元素、文本非空、在弹窗内 —— 悬空的 aria-labelledby 是经典静默失效);
                   #app 的背景惰性属性随两个弹窗的开/关**真的切换**,且只挂 #app
    g3 → A11Y-03   划词菜单被 Escape 关掉后**保持隐藏** —— 后续 keyup 不得把菜单弹回来
                   (这正是 03-SUMMARY 记录、由 62dfd3e / 09b170d 两次提交修复的回归点),
                   且关闭**不清空选区**(D-08)
    g4 → F1-d(成功路径)
                   选档成功后**真的**把焦点交还 #btn-continue-check —— 判据是
                   document.activeElement 的**读数**(源码里含 .focus() 不构成证据:
                   那正是本缺陷第一次溜过去的原因,源码里早就有、行为上没有)

每条断言都配了「判别控制」——本文件的纪律是:**不能区分「行为在」与「行为不在」的断言是废的**。
    g1:非 Escape 按键(Control)不得关闭弹窗 —— 排除「任何按键都关」的假绿
    g2:①摘掉 inert 属性后读数必须变假;②把 aria-labelledby 指向不存在的 id 后解析必须为空;
       ③非惰性时同一个背景元素必须**能**被聚焦 —— 排除恒真/恒假的读数
    g3:把关闭态守卫置空(= 修复前的代码路径)后,**同一个 keyup 必须把菜单弹回来** ——
       这是唯一能证明「上面的绿不是恒绿」的手段(变异测试)
    g4:把 #btn-continue-check 实例的 focus 方法置空(= 把待修的那一行变成 no-op)后,
       同一条真实路径的 activeElement 必须**不再**落在它上面 —— 排除恒绿

未覆盖(如实记录,不伪装成已覆盖)
    **键盘来源的文本选区(Shift+方向键)本环境无法自动化**:受信 `Shift+ArrowRight` 连按
    12 次后 `window.getSelection()` 仍为 `{collapsed: true, len: 0}`(03-SUMMARY 的实测记录,
    本文件不重复该实验)。故 A11Y-03 的「键盘用户能选中多于一个字符」这一半、以及 A11Y-08 的
    整条键盘划词路径,**必须**是具名人工验收 —— ROADMAP Phase 8 §Manual checks 明文规定
    不得因自动测试 FAIL 判定功能缺陷。本文件的 g1/g3 用**真实鼠标拖拽**产生选区
    (拖拽是真实输入路径,不是伪造选区),并在每次断言里注明来源是鼠标而非键盘;
    「键盘来源的同一路径」仍是人工项。

与 check-05 的关系
    复用 check-05 的模块级设施(服务生命周期 / fixture 隔离 / enter_project / ok /
    ok_true / blocked / info / item_verdict / ROWS),不重复实现,也不改动 check-05 一行。

运行方式
    .venv/bin/python scripts/check-07-idi08-validation.py
    .venv/bin/python scripts/check-07-idi08-validation.py --item g1,g3
    .venv/bin/python scripts/check-07-idi08-validation.py --keep

退出码语义(与 check-05 / check-06 一致)
    0 = 全 pass;1 = 至少一条 FAIL;2 = 无 FAIL 但至少一条 BLOCKED
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK05 = ROOT / "scripts" / "check-05-ui-uat.py"


def load_check05():
    """把 check-05 当模块加载(文件名含连字符,不能用 import)。"""
    spec = importlib.util.spec_from_file_location("check05_ui_uat", CHECK05)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c05 = load_check05()
ok = c05.ok
ok_true = c05.ok_true
blocked = c05.blocked
info = c05.info


# ---------------------------------------------------------------------------
# 共用读取器
# ---------------------------------------------------------------------------
# 三个可关对象与三个「刻意不响应」的弹窗(D-11 的范围锁,逐字取自 app.js 的分派器注释)
CLOSABLE = ("#selection-menu", "#confirmation-modal", "#tier-modal")
SCOPE_LOCKED = ("#permission-modal", "#mission-complete-modal", "#cli-check-overlay")

# 背景探测用的元素:在 #app 内、p3 与 phase5_awaiting_tier 两态都可见可聚焦
BG_PROBE = "#ai-route-select"


def _menu_state(page):
    """划词菜单 + 当前选区的快照。"""
    return page.evaluate("""() => {
        const menu = document.getElementById('selection-menu');
        const s = window.getSelection();
        return {
            menuHidden: menu.classList.contains('hidden'),
            selLen: s ? s.toString().length : 0,
            selText: s ? s.toString().slice(0, 16) : '',
            collapsed: s ? s.isCollapsed : null,
            active: document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null,
            dismissedGuardSet: !!dismissedSelectionRange,
        };
    }""")


def _settle_cli_check(page, timeout_ms=5000, settle_ms=600):
    """等 runCliCheck() 的在途往返彻底落地(响应到达 **且** 随后的 add/remove('hidden') 执行完)。

    app.js:1849 在页面加载时异步跑一次;它返回后按自检结果切换浮层可见性。若不等它落地就
    注入可见态,它随后的 add('hidden')(本机自检通过)会把注入**当场撤销** —— 实测竞态:
    同一命令连跑两次,一次绿一次红。注入前先让这一次往返落地,注入才是确定的。

    **两个条件都要满足,只满足一个仍会偶发假红**(实测:本函数早先只等「首个响应 + 3 个稳定
    采样(约 150ms)」时,仍偶发 `[#cli-check-overlay] Escape 后仍可见` 变红 —— 因为可能有
    **第二个**往返在途,它在我们退出**之后**才落地并撤销注入):

      ① 没有在途的 `/api/cli-check` 往返(用 Playwright 的 request/response 事件计数);
      ② 可见态在 `settle_ms` 内不再变化。

    只等「响应到达」不够 —— resp.json() 之后的 add/remove('hidden') 还没跑完;
    只等状态稳定也不够 —— 在途的第二个往返会在稳定窗口**之外**落地。
    """
    inflight = {"n": 0}

    def _on_request(req):
        if "/api/cli-check" in req.url:
            inflight["n"] += 1

    def _on_response(resp):
        if "/api/cli-check" in resp.url:
            inflight["n"] = max(0, inflight["n"] - 1)

    page.on("request", _on_request)
    page.on("response", _on_response)
    try:
        try:
            # 程序化点击而非 page.click:浮层此刻可能仍是 hidden,不可见元素点不动。
            with page.expect_response(lambda r: "/api/cli-check" in r.url, timeout=timeout_ms):
                page.evaluate("document.getElementById('cli-recheck-btn').click()")
        except Exception:  # noqa: BLE001 — 端点不可达不挡本项,下面的轮询仍会给出结论
            pass
        deadline = time.monotonic() + (timeout_ms / 1000.0)
        last, stable_since = None, None
        while time.monotonic() < deadline:
            cur = page.evaluate(
                "document.getElementById('cli-check-overlay').classList.contains('hidden')")
            now = time.monotonic()
            if cur != last:
                last, stable_since = cur, now
            if (inflight["n"] == 0 and stable_since is not None
                    and (now - stable_since) * 1000 >= settle_ms):
                return cur
            page.wait_for_timeout(50)
        return last
    finally:
        page.remove_listener("request", _on_request)
        page.remove_listener("response", _on_response)


def _drag_select(page, node_index):
    """真实鼠标拖拽产生一段非折叠选区(不是伪造 Range)。

    坐标由 Range 在 #round-doc 的文本节点上量出,再核对 elementFromPoint 确实落在
    #round-doc 的子树内 —— 探针期的教训:文档面板滚动过之后,量出的坐标会落到面板外,
    此时拖拽**不会**产生选区,而静默的空选区会让后面的断言变成假绿。
    """
    nodes = page.evaluate("""() => {
        const doc = document.getElementById('round-doc');
        const walker = document.createTreeWalker(doc, NodeFilter.SHOW_TEXT);
        const out = []; let n;
        while ((n = walker.nextNode())) {
            const t = n.data;
            if (!t || !t.trim()) continue;
            const r = document.createRange();
            r.setStart(n, 0);
            r.setEnd(n, Math.min(12, t.length));
            const b = r.getBoundingClientRect();
            out.push({x: b.left, y: b.top + b.height / 2, w: b.width});
        }
        return out;
    }""")
    if node_index >= len(nodes):
        return {"err": f"#round-doc 只有 {len(nodes)} 个非空文本节点,取不到 index={node_index}"}
    nd = nodes[node_index]
    x1, y1 = nd["x"] + 3, nd["y"]
    x2 = nd["x"] + nd["w"] - 3
    inside = page.evaluate(
        """([x, y]) => {
            const el = document.elementFromPoint(x, y);
            const doc = document.getElementById('round-doc');
            return !!(el && doc.contains(el));
        }""",
        [x1, y1],
    )
    if not inside:
        return {"err": f"拖拽起点 ({x1:.0f},{y1:.0f}) 不在 #round-doc 内(面板滚动过?)"}
    page.evaluate("window.getSelection().removeAllRanges()")
    page.wait_for_timeout(80)
    page.mouse.move(x1, y1)
    page.wait_for_timeout(50)
    page.mouse.down()
    page.mouse.move(x2, y1, steps=12)
    page.wait_for_timeout(50)
    page.mouse.up()
    page.wait_for_timeout(300)
    return _menu_state(page)


def _aria_probe(page, modal_id):
    """读一个弹窗的 dialog 语义三件套,并把无障碍名称**解析出来**。

    只断言「属性存在」是不够的:`aria-labelledby="no-such-id"` 同样让属性存在,
    而辅助技术拿到的名称是空 —— 这正是悬空引用的静默失效形态。故这里真的按 id 取元素、
    取它的文本、并核对它在弹窗**内部**(名称必须说的是这个对话框,不是别处借来的)。
    """
    return page.evaluate(
        """(id) => {
            const m = document.getElementById(id);
            if (!m) return {err: 'no modal'};
            const lb = m.getAttribute('aria-labelledby');
            let exists = false, name = '', inside = false, target = null;
            if (lb) {
                const ids = lb.trim().split(/\\s+/).filter(Boolean);
                const parts = [];
                exists = ids.length > 0;
                inside = ids.length > 0;
                for (const t of ids) {
                    const el = document.getElementById(t);
                    if (!el) { exists = false; continue; }
                    parts.push(el.textContent.trim());
                    if (!m.contains(el)) inside = false;
                }
                target = ids.join(' ');
                name = parts.join(' ').trim();
            }
            return {
                role: m.getAttribute('role'),
                ariaModal: m.getAttribute('aria-modal'),
                labelledby: lb,
                labelTarget: target,
                labelExists: exists,
                labelName: name,
                labelInsideModal: inside,
            };
        }""",
        modal_id,
    )


def _inert_probe(page):
    """背景惰性的挂载点读数:属性 + IDL + 三个**不得**挂载的节点。"""
    return page.evaluate("""() => {
        const app = document.getElementById('app');
        const has = (id) => { const e = document.getElementById(id); return e ? e.hasAttribute('inert') : null; };
        return {
            appAttr: app.hasAttribute('inert'),
            appIDL: app.inert,
            bodyAttr: document.body.hasAttribute('inert'),
            bodyIDL: document.body.inert,
            confirmAttr: has('confirmation-modal'),
            tierAttr: has('tier-modal'),
            menuAttr: has('selection-menu'),
        };
    }""")


def _bg_focus_probe(page, selector):
    """背景元素在惰性期间能不能被聚焦 —— 这是「宣告成真」的行为读数。

    原生 inert 的规范效果之一就是子树内元素不可聚焦;故 `el.focus()` 应当**无效**。
    读数带 before/after,故「没动」与「动了」是可区分的两种实测结果,不是推断。
    """
    return page.evaluate(
        """(sel) => {
            const el = document.querySelector(sel);
            if (!el) return {err: 'no element'};
            const before = document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null;
            el.focus();
            const after = document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null;
            return {
                before, after, moved: before !== after,
                visible: el.getClientRects().length > 0,
                disabled: !!el.disabled,
                appInert: document.getElementById('app').hasAttribute('inert'),
            };
        }""",
        selector,
    )


def _awaiting_tier_fixture(tmp_root):
    """phase5_awaiting_tier 样本:有 DESIGN.md、无 check 报告(backend/state.py 的判据)。

    直接复制 archive 样本再摘掉它的 check 报告 —— 不新造内容,只改状态判定所需的文件集。
    """
    src = ROOT / "scripts" / "ui-states" / "archive"
    dest = Path(tempfile.mkdtemp(dir=str(tmp_root), prefix="awaiting-")) / "awaiting"
    shutil.copytree(src, dest)
    for report in (dest / "docs").glob("DESIGN-check-*.md"):
        report.unlink()
    return dest


# ---------------------------------------------------------------------------
# g1 — A11Y-05:受信 Escape 真的关闭三个可关对象;其余三个弹窗刻意不响应
# ---------------------------------------------------------------------------
def g1(page, tmp_root):
    item = "g1"
    print("\n=== g1: A11Y-05 Escape 关闭两个阻塞弹窗 + 划词菜单;范围锁三弹窗不响应 ===", flush=True)
    dialogs = []
    posts = []
    page.on("dialog", lambda d: (dialogs.append({"type": d.type, "message": d.message}), d.dismiss()))
    page.on("request", lambda r: posts.append((r.method, r.url)) if r.method == "POST" else None)

    # —— 实例 1/3:#confirmation-modal(真实开启路径:点 #btn-authorize)——
    proj = c05.make_fixture("p3", tmp_root)
    c05.enter_project(page, proj)
    disabled = page.evaluate("document.getElementById('btn-authorize').disabled")
    if disabled:
        blocked(item, "g1 [#confirmation-modal] 真实开启路径可达", "#btn-authorize 可点",
                "disabled=true", "p3 样本下授权按钮未点亮,弹窗打不开")
    else:
        page.click("#btn-authorize")
        page.wait_for_timeout(300)
        opened = not page.evaluate(
            "document.getElementById('confirmation-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#confirmation-modal] 打开后弹窗可见(断言前提,防假绿)",
                opened, "hidden=false", f"hidden={not opened}")
        if opened:
            page.keyboard.press("Control")  # 判别控制:非 Escape 按键
            page.wait_for_timeout(200)
            still = not page.evaluate(
                "document.getElementById('confirmation-modal').classList.contains('hidden')")
            ok_true(item, "g1 [#confirmation-modal] 判别控制:非 Escape 按键不关闭弹窗",
                    still, "仍可见", f"hidden={not still}")
            posts_before, dialogs_before = len(posts), len(dialogs)
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            closed = page.evaluate(
                "document.getElementById('confirmation-modal').classList.contains('hidden')")
            ok_true(item, "g1 [#confirmation-modal] 受信 Escape 关闭弹窗",
                    closed, "hidden=true", f"hidden={closed}")
            ok_true(item, "g1 [#confirmation-modal] Escape 零决定:未弹出任何原生对话框(不等于「拒绝」)",
                    len(dialogs) == dialogs_before, f"{dialogs_before} 个", f"{len(dialogs)} 个")
            ok_true(item, "g1 [#confirmation-modal] Escape 零决定:未发出任何写批注/授权 POST",
                    len(posts) == posts_before, f"{posts_before} 个", f"{len(posts)} 个")
            focus = page.evaluate("""() => {
                const b = document.getElementById('btn-authorize');
                return {active: document.activeElement ? document.activeElement.id : null,
                        focusable: !b.disabled && b.getClientRects().length > 0};
            }""")
            info("g1 [#confirmation-modal] 焦点交还读数", str(focus))
            # A-8 已登记:目标不可聚焦时静默降级(Chrome 下 .focus() 对禁用按钮是 no-op)。
            # 故判据是「交还到 #btn-authorize ∨ 目标本身不可聚焦」——两条都是契约内的合法结果。
            ok_true(item, "g1 [#confirmation-modal] 焦点交还 #btn-authorize(目标不可聚焦时按 A-8 静默降级)",
                    focus["active"] == "btn-authorize" or not focus["focusable"],
                    "active=btn-authorize 或目标不可聚焦",
                    f"active={focus['active']} focusable={focus['focusable']}")

    # —— 实例 2/3:#tier-modal(真实开启路径:进入 phase5_awaiting_tier)——
    awaiting = _awaiting_tier_fixture(tmp_root)
    c05.enter_project(page, awaiting)
    page.wait_for_timeout(500)
    badge = page.evaluate("document.getElementById('state-badge').textContent")
    info("g1 [tier] 样本状态", badge)
    opened = not page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')")
    ok_true(item, "g1 [#tier-modal] phase5_awaiting_tier 下弹窗自动打开(断言前提,防假绿)",
            opened, "hidden=false", f"hidden={not opened}")
    if opened:
        page.keyboard.press("Control")
        page.wait_for_timeout(200)
        still = not page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#tier-modal] 判别控制:非 Escape 按键不关闭弹窗",
                still, "仍可见", f"hidden={not still}")
        posts_before = len(posts)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        closed = page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#tier-modal] 受信 Escape 关闭弹窗",
                closed, "hidden=true", f"hidden={closed}")
        ok_true(item, "g1 [#tier-modal] Escape 零决定:未发出任何 POST(不复位 selfcheck.tier、不发请求)",
                len(posts) == posts_before, f"{posts_before} 个", f"{len(posts)} 个")
        flag = page.evaluate("tierModalShown")
        ok_true(item, "g1 [#tier-modal] Escape 复位 tierModalShown(D-13 死状态的实质修复)",
                flag is False, "false", str(flag))
        active = page.evaluate(
            "document.activeElement ? document.activeElement.id : null")
        ok_true(item, "g1 [#tier-modal] 焦点交还 #btn-continue-check(F1-d)",
                active == "btn-continue-check", "btn-continue-check", str(active))
        # 复位是**行为性**的:下一个自检事件必须能重新弹出 —— 否则「档位未定且入口消失」的死状态仍在
        page.evaluate("refreshChecksAfterStream()")
        page.wait_for_timeout(900)
        reopened = not page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#tier-modal] 复位生效:下一个自检事件能重新弹出(死状态已消)",
                reopened, "hidden=false", f"hidden={not reopened}")
        page.keyboard.press("Escape")  # 收拾现场
        page.wait_for_timeout(200)

    # —— 实例 3/3:划词菜单 ——
    # 选区来源:**真实鼠标拖拽**(键盘来源的选区本环境不可自动化,见文件头「未覆盖」段)。
    c05.enter_project(page, proj)
    state = _drag_select(page, 1)
    if state.get("err"):
        blocked(item, "g1 [#selection-menu] 可打开(鼠标拖拽产生选区)", "非折叠选区 + 菜单可见",
                state["err"], "拖拽未落在 #round-doc 内")
    else:
        ok_true(item, "g1 [#selection-menu] 鼠标拖拽后菜单可见(断言前提,防假绿)",
                not state["menuHidden"], "hidden=false",
                f"hidden={state['menuHidden']} selLen={state['selLen']}")
        if not state["menuHidden"]:
            # 真实提交手势:松开 Shift ⇒ 焦点入菜单首按钮(与真实用户路径一致)
            page.keyboard.down("Shift")
            page.wait_for_timeout(80)
            page.keyboard.up("Shift")
            page.wait_for_timeout(250)
            focused = page.evaluate("document.activeElement ? document.activeElement.id : null")
            info("g1 [#selection-menu] 松开 Shift 后的焦点", str(focused))
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            closed = page.evaluate(
                "document.getElementById('selection-menu').classList.contains('hidden')")
            ok_true(item, "g1 [#selection-menu] 受信 Escape 关闭划词菜单",
                    closed, "hidden=true", f"hidden={closed}")
    info("g1 [#selection-menu] 选区来源", "真实鼠标拖拽(键盘来源的 Shift+方向键选区本环境不可自动化 ⇒ 人工项)")

    # —— 范围锁:其余三个弹窗刻意不响应 Escape(D-11;刻意的,不是漏项)——
    # #permission-modal:走它自己的开启函数(真实开启路径)
    page.evaluate(
        "showPermissionModal({summary: 'Nyquist g1 探针', tool: 'probe', id: 'g1-probe'})")
    page.wait_for_timeout(200)
    visible = not page.evaluate(
        "document.getElementById('permission-modal').classList.contains('hidden')")
    ok_true(item, "g1 [#permission-modal] 打开后可见(断言前提,防假绿)",
            visible, "hidden=false", f"hidden={not visible}")
    if visible:
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        still = not page.evaluate(
            "document.getElementById('permission-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#permission-modal] Escape 后仍可见(范围锁,刻意不响应)",
                still, "仍可见", f"hidden={not still}")
    page.evaluate("document.getElementById('permission-modal').classList.add('hidden')")  # 收拾现场

    # #cli-check-overlay:它的开启路径要求本机 cli 自检**失败**(runCliCheck),
    # 本环境 cli 自检通过 ⇒ 无法用真实开启路径。**注入可见态**并在 note 里说明:
    # 被测的行为是「分派器对它没有分支」,注入的是状态输入,不是被断言的输出。
    cli_hidden = page.evaluate(
        "document.getElementById('cli-check-overlay').classList.contains('hidden')")
    info("g1 [#cli-check-overlay] 开机后的默认态", f"hidden={cli_hidden}")
    _settle_cli_check(page)  # 必须先让在途的 runCliCheck() 落地,否则注入会被它撤销(见函数注释)
    page.evaluate("document.getElementById('cli-check-overlay').classList.remove('hidden')")
    page.wait_for_timeout(150)
    visible = not page.evaluate(
        "document.getElementById('cli-check-overlay').classList.contains('hidden')")
    ok_true(item, "g1 [#cli-check-overlay] 注入可见态成功(断言前提,防假绿)",
            visible, "hidden=false", f"hidden={not visible}",
            "开启路径要求 cli 自检失败,本环境不满足 ⇒ 注入状态输入")
    if visible:
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        still = not page.evaluate(
            "document.getElementById('cli-check-overlay').classList.contains('hidden')")
        ok_true(item, "g1 [#cli-check-overlay] Escape 后仍可见(范围锁,刻意不响应)",
                still, "仍可见", f"hidden={not still}")
    page.evaluate("document.getElementById('cli-check-overlay').classList.add('hidden')")

    # #mission-complete-modal:真实路径(进入 mission_complete 归档样本即弹一次)
    archive = c05.make_fixture("archive", tmp_root)
    c05.enter_project(page, archive)
    page.wait_for_timeout(500)
    visible = not page.evaluate(
        "document.getElementById('mission-complete-modal').classList.contains('hidden')")
    ok_true(item, "g1 [#mission-complete-modal] 进入归档态后自动弹出(断言前提,防假绿)",
            visible, "hidden=false", f"hidden={not visible}")
    if visible:
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        still = not page.evaluate(
            "document.getElementById('mission-complete-modal').classList.contains('hidden')")
        ok_true(item, "g1 [#mission-complete-modal] Escape 后仍可见(范围锁,刻意不响应)",
                still, "仍可见", f"hidden={not still}")


# ---------------------------------------------------------------------------
# g2 — A11Y-06:dialog 语义 + 无障碍名称可解析 + 背景惰性的**切换**
# ---------------------------------------------------------------------------
def g2(page, tmp_root):
    item = "g2"
    print("\n=== g2: A11Y-06 两个弹窗的 dialog 语义 + 背景 inert 的切换与挂载点 ===", flush=True)

    proj = c05.make_fixture("p3", tmp_root)
    c05.enter_project(page, proj)

    # —— 关闭态基线:两个弹窗都关着 ⇒ #app 不带惰性属性 ——
    inert = _inert_probe(page)
    info("g2 关闭态基线", str(inert))
    ok_true(item, "g2 关闭态基线:#app 不带 inert 属性",
            inert["appAttr"] is False, "false", str(inert["appAttr"]))
    ok_true(item, "g2 关闭态基线:#app.inert IDL 为 false",
            inert["appIDL"] is False, "false", str(inert["appIDL"]))

    # —— 实例 1/2:#confirmation-modal ——
    disabled = page.evaluate("document.getElementById('btn-authorize').disabled")
    if disabled:
        blocked(item, "g2 [#confirmation-modal] 真实开启路径可达", "#btn-authorize 可点",
                "disabled=true", "p3 样本下授权按钮未点亮,弹窗打不开")
    else:
        page.click("#btn-authorize")
        page.wait_for_timeout(300)
        opened = not page.evaluate(
            "document.getElementById('confirmation-modal').classList.contains('hidden')")
        if not opened:
            blocked(item, "g2 [#confirmation-modal] 打开后可见", "hidden=false",
                    "hidden=true", "点击授权按钮后弹窗未打开")
        else:
            _dialog_semantics(page, item, "confirmation-modal")
            _inert_open_assertions(page, item, "confirmation-modal", BG_PROBE)
            # 关闭 ⇒ 属性摘掉(切换的另一半)
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            after = _inert_probe(page)
            ok_true(item, "g2 [#confirmation-modal] 关闭后 #app 不再带 inert(切换的另一半)",
                    after["appAttr"] is False, "false", str(after["appAttr"]))
            ok_true(item, "g2 [#confirmation-modal] 关闭后 #app.inert IDL 为 false",
                    after["appIDL"] is False, "false", str(after["appIDL"]))
            # 行为控制:非惰性时同一个背景元素**能**被聚焦 ⇒ 上面那条「不可聚焦」不是恒假
            bg = _bg_focus_probe(page, BG_PROBE)
            info("g2 非惰性时的背景聚焦读数", str(bg))
            ok_true(item, "g2 行为控制:非惰性时同一背景元素可被聚焦(排除恒假读数)",
                    bg.get("moved") is True, "焦点移动",
                    f"moved={bg.get('moved')} before={bg.get('before')} after={bg.get('after')}")

    # —— 实例 2/2:#tier-modal ——
    awaiting = _awaiting_tier_fixture(tmp_root)
    c05.enter_project(page, awaiting)
    page.wait_for_timeout(500)
    opened = not page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')")
    if not opened:
        blocked(item, "g2 [#tier-modal] 打开后可见", "hidden=false", "hidden=true",
                "phase5_awaiting_tier 下弹窗未打开")
    else:
        _dialog_semantics(page, item, "tier-modal")
        _inert_open_assertions(page, item, "tier-modal", BG_PROBE)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        after = _inert_probe(page)
        ok_true(item, "g2 [#tier-modal] 关闭后 #app 不再带 inert(切换的另一半)",
                after["appAttr"] is False, "false", str(after["appAttr"]))

    # —— 范围锁:其余三个弹窗**不得**带 dialog 语义(D-11 的刻意窄切片)——
    scope = page.evaluate("""() => {
        const out = {};
        for (const id of ['permission-modal', 'mission-complete-modal', 'cli-check-overlay']) {
            const el = document.getElementById(id);
            out[id] = el ? {role: el.getAttribute('role'), ariaModal: el.getAttribute('aria-modal')} : null;
        }
        return out;
    }""")
    info("g2 其余三个弹窗的语义读数", str(scope))
    for mid in ("permission-modal", "mission-complete-modal", "cli-check-overlay"):
        rec = scope.get(mid)
        ok_true(item, f"g2 [#{mid}] 不带 dialog 语义(范围锁,刻意不响应)",
                rec is not None and rec["role"] is None and rec["ariaModal"] is None,
                "role=null aria-modal=null", str(rec))


def _dialog_semantics(page, item, modal_id):
    """一个弹窗的 dialog 语义三件套 + 无障碍名称的**可解析性**(每实例各跑一次)。"""
    a = _aria_probe(page, modal_id)
    if a.get("err"):
        blocked(item, f"g2 [#{modal_id}] 语义可读", "弹窗元素存在", a["err"], "元素不存在")
        return
    info(f"g2 [#{modal_id}] 语义读数", str(a))
    ok(item, f"g2 [#{modal_id}] role == dialog", "dialog", a["role"])
    ok(item, f"g2 [#{modal_id}] aria-modal == true", "true", a["ariaModal"])
    ok_true(item, f"g2 [#{modal_id}] aria-labelledby 的每个 id 都指向存在的元素",
            a["labelExists"] is True, "全部存在",
            f"labelledby={a['labelledby']} exists={a['labelExists']}")
    ok_true(item, f"g2 [#{modal_id}] 无障碍名称解析出非空文本(悬空引用会在这里变红)",
            bool(a["labelName"]), "非空", f"name={a['labelName']!r}")
    ok_true(item, f"g2 [#{modal_id}] 无障碍名称取自弹窗**内部**的标题元素",
            a["labelInsideModal"] is True, "在弹窗内",
            f"target={a['labelTarget']} inside={a['labelInsideModal']}")

    # 变异控制:把 aria-labelledby 指向不存在的 id,同一个解析器必须解析为空
    mutated = page.evaluate(
        """(id) => {
            const m = document.getElementById(id);
            const orig = m.getAttribute('aria-labelledby');
            m.setAttribute('aria-labelledby', 'no-such-id-nyquist-probe');
            return orig;
        }""",
        modal_id,
    )
    broken = _aria_probe(page, modal_id)
    ok_true(item, f"g2 [#{modal_id}] 变异控制:指向不存在的 id 时解析为空(解析器不是恒真)",
            broken["labelExists"] is False and broken["labelName"] == "",
            "exists=false name=''", f"exists={broken['labelExists']} name={broken['labelName']!r}")
    page.evaluate(
        """([id, v]) => document.getElementById(id).setAttribute('aria-labelledby', v)""",
        [modal_id, mutated],
    )
    restored = _aria_probe(page, modal_id)
    ok_true(item, f"g2 [#{modal_id}] 变异控制后属性已复原",
            restored["labelledby"] == mutated, str(mutated), str(restored["labelledby"]))


def _inert_open_assertions(page, item, modal_id, bg_probe):
    """一个弹窗打开期间:属性在、IDL 在、只挂 #app、且背景**真的**不可聚焦。"""
    inert = _inert_probe(page)
    info(f"g2 [#{modal_id}] 打开期间的惰性读数", str(inert))
    ok_true(item, f"g2 [#{modal_id}] 打开期间 #app 带 inert 属性",
            inert["appAttr"] is True, "true", str(inert["appAttr"]))
    ok_true(item, f"g2 [#{modal_id}] 打开期间 #app.inert IDL 为 true(原生布尔属性)",
            inert["appIDL"] is True, "true", str(inert["appIDL"]))
    ok_true(item, f"g2 [#{modal_id}] 挂载点边界:document.body 不带 inert(挂错节点会锁死弹窗自身)",
            inert["bodyAttr"] is False, "false", str(inert["bodyAttr"]))
    ok_true(item, f"g2 [#{modal_id}] 挂载点边界:打开的弹窗自身不带 inert",
            inert["confirmAttr"] is False and inert["tierAttr"] is False,
            "两个弹窗都不带", f"confirm={inert['confirmAttr']} tier={inert['tierAttr']}")
    ok_true(item, f"g2 [#{modal_id}] 挂载点边界:#selection-menu 不带 inert",
            inert["menuAttr"] is False, "false", str(inert["menuAttr"]))
    bg = _bg_focus_probe(page, bg_probe)
    info(f"g2 [#{modal_id}] 惰性期间的背景聚焦读数", str(bg))
    ok_true(item, f"g2 [#{modal_id}] 背景在惰性期间**不可聚焦**(宣告成真的行为读数)",
            bg.get("moved") is False, "焦点不移动",
            f"moved={bg.get('moved')} before={bg.get('before')} after={bg.get('after')}")

    # 变异控制:摘掉属性 → 读数必须变假;重跑派生函数 → 复原
    page.evaluate("document.getElementById('app').removeAttribute('inert')")
    stripped = _inert_probe(page)
    ok_true(item, f"g2 [#{modal_id}] 变异控制:摘掉属性后读数为假(读数不是恒真)",
            stripped["appAttr"] is False and stripped["appIDL"] is False,
            "false/false", f"attr={stripped['appAttr']} idl={stripped['appIDL']}")
    page.evaluate("syncBackgroundInert()")
    back = _inert_probe(page)
    ok_true(item, f"g2 [#{modal_id}] 变异控制:重跑派生函数后属性复原(派生式幂等)",
            back["appAttr"] is True, "true", str(back["appAttr"]))


# ---------------------------------------------------------------------------
# g3 — A11Y-03:Escape 关掉划词菜单后**保持隐藏**(03-SUMMARY 记录的回归点)
# ---------------------------------------------------------------------------
# 回归的机制(逐字取自 03-SUMMARY 的实测记录):分派器在 **keydown** 上跑,
# 调 hideSelectionMenu() 并把焦点交还 #round-doc(F1-a)⇒ keyup 到达时它的 target 已是
# #round-doc,而 #round-doc 上的 handleSelectionTrigger 挂在**每一次** keyup 上,
# 其守卫(状态 phase3、选区非折叠且在文档内)全部通过 ⇒ 菜单原样弹回。
# 09b170d 的修法是「关闭态守卫」:hideSelectionMenu() 记下被关掉的那份选区,
# keyup 那一路在**它之前**比对选区身份。故本项的判据是**行为**:关掉之后,
# 后续的 keyup 不得重开菜单,而选区仍须存活(D-08 禁清空)。
def g3(page, tmp_root):
    item = "g3"
    print("\n=== g3: A11Y-03 Escape 关闭划词菜单后保持隐藏(后续 keyup 不重开)===", flush=True)
    proj = c05.make_fixture("p3", tmp_root)
    c05.enter_project(page, proj)

    state = _drag_select(page, 1)
    if state.get("err"):
        blocked(item, "g3 可打开划词菜单(鼠标拖拽产生选区)", "非折叠选区 + 菜单可见",
                state["err"], "拖拽未落在 #round-doc 内")
        return
    ok_true(item, "g3 鼠标拖拽产生非折叠选区(断言前提,防假绿)",
            state["collapsed"] is False and state["selLen"] > 0, "非折叠且长度>0",
            f"collapsed={state['collapsed']} len={state['selLen']}")
    ok_true(item, "g3 拖拽后菜单可见(断言前提,防假绿)",
            not state["menuHidden"], "hidden=false", f"hidden={state['menuHidden']}")
    if state["menuHidden"] or state["collapsed"] or state["selLen"] == 0:
        return

    # 真实提交手势(计划 01 的交付):松开 Shift ⇒ 焦点送入菜单首按钮。
    # 这一步让后续 Escape 的 keydown target 落在菜单按钮上 —— 正是回归被实测复现的现场。
    page.keyboard.down("Shift")
    page.wait_for_timeout(80)
    page.keyboard.up("Shift")
    page.wait_for_timeout(250)
    focused = page.evaluate("document.activeElement ? document.activeElement.id : null")
    ok_true(item, "g3 松开 Shift 把焦点送入 #btn-annotate(真实手势,非程序化移焦)",
            focused == "btn-annotate", "btn-annotate", str(focused))

    # Escape(受信;press = keydown + keyup 成对,回归就在这对之间)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    after = _menu_state(page)
    ok_true(item, "g3 受信 Escape 关闭划词菜单",
            after["menuHidden"] is True, "hidden=true", f"hidden={after['menuHidden']}")
    ok_true(item, "g3 回归点:紧随其后的 Escape **keyup** 不得把菜单弹回来",
            after["menuHidden"] is True, "hidden=true", f"hidden={after['menuHidden']}")

    # 后续任意 keyup 也不得重开(方向键在只读容器里不改选区 ⇒ 没有守卫时必被弹回)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(300)
    k = _menu_state(page)
    ok_true(item, "g3 后续 ArrowRight 的 keyup 不重开菜单",
            k["menuHidden"] is True, "hidden=true", f"hidden={k['menuHidden']}")

    # 再按一次 Escape(SUMMARY 记录的另一种失败形态)也不得重开
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    k2 = _menu_state(page)
    ok_true(item, "g3 再按一次 Escape 仍不重开菜单",
            k2["menuHidden"] is True, "hidden=true", f"hidden={k2['menuHidden']}")

    # D-08:关闭**不得清空选区**(廉价「修法」= 清空选区,会毁掉「Escape 后接着 Shift+→ 继续扩选」)
    ok_true(item, "g3 关闭后选区仍存活(D-08 禁清空选区;清空式修法会在这里变红)",
            k2["collapsed"] is False and k2["selLen"] > 0, "非折叠且长度>0",
            f"collapsed={k2['collapsed']} len={k2['selLen']}")

    # —— 变异测试:把关闭态守卫置空(= 修复前的代码路径),同一个 keyup 必须把菜单弹回来 ——
    # 这是唯一能证明「上面的绿不是恒绿」的手段:若守卫被删掉,断言就会变红。
    page.evaluate("dismissedSelectionRange = null")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(300)
    mut = _menu_state(page)
    ok_true(item, "g3 变异控制:守卫置空后同一 keyup 重新弹开菜单(证明上面的绿不是恒绿)",
            mut["menuHidden"] is False, "hidden=false(菜单弹回)",
            f"hidden={mut['menuHidden']}")

    # —— 正向控制:菜单未被永久锁死;换一份新选区后仍能弹出(守卫按选区身份自清)——
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    again = _drag_select(page, 2)
    ok_true(item, "g3 正向控制:新的选区仍能弹出菜单(守卫按选区身份自清,菜单未被锁死)",
            not again.get("err") and again["menuHidden"] is False,
            "hidden=false", str(again))

    info("g3 选区来源", "真实鼠标拖拽;键盘来源(Shift+方向键)本环境不可自动化 ⇒ 人工项")


# ---------------------------------------------------------------------------
# g4 — F1-d 的**成功**路径落点:选档成功 ⇒ 交还 #btn-continue-check
# ---------------------------------------------------------------------------
# 为什么单列一项:g1 覆盖的是 Escape 分支的交还(F1-d 的「取消」路径),而 chooseTier()
# 的**成功**路径此前不移焦 —— 被聚焦的 #btn-tier-loose 随弹窗隐藏变成 display:none,
# document.activeElement 回落到 <body>。这打破 F1(焦点不得因隐藏回落到 <body>),
# 且它发生在 D-11 判定为「真正的卡死」的那次交互之后。
def _active_id(page):
    """当前焦点元素的读数。#btn-continue-check 之外的回落目标(<body>)没有 id,
    故读法固定为 `id || tagName` —— 只读 id 会打印空串,把两种状态读成同一个。"""
    return page.evaluate(
        "() => document.activeElement "
        "? (document.activeElement.id || document.activeElement.tagName) : null")


def _g4_enter_and_choose(page, item, tag, tmp_root, mutate_focus):
    """进 phase5_awaiting_tier →(控制支:置空交还调用)→ 真实点击档位按钮 → 读数。

    返回 {"before": 点击前的焦点, "after": {...}};任一步前提不成立时记 blocked 并返回
    None —— 前提不成立时那条断言什么都没测到,记 PASS 就是把空转当证据。
    """
    c05.enter_project(page, _awaiting_tier_fixture(tmp_root))
    page.wait_for_timeout(500)
    if page.evaluate("document.getElementById('tier-modal').classList.contains('hidden')"):
        blocked(item, f"g4 {tag} 选档路径可达(断言前提,防假绿)", "#tier-modal 可见",
                "hidden=true", "phase5_awaiting_tier 下档位弹窗未自动打开 ⇒ 本项无法判定")
        return None
    before = _active_id(page)
    if mutate_focus:
        # 判别控制:把实例方法置空 = 把待修的那一行变成 no-op(变异测试)
        page.evaluate("document.getElementById('btn-continue-check').focus = function(){}")
    try:
        # 真实 POST,不是伪造响应;包住点击以确认请求真的发出去了
        with page.expect_response(lambda r: "/api/checks/tier" in r.url, timeout=8000):
            page.click("#btn-tier-loose")
    except Exception as exc:  # noqa: BLE001 — 请求没发出 ⇒ 交还路径没被走到,记 blocked
        blocked(item, f"g4 {tag} 真实 POST /api/checks/tier", "收到响应",
                f"无响应({exc.__class__.__name__})", "档位按钮点击未触发请求")
        return None
    page.wait_for_timeout(2000)  # 等 refreshChecksAfterStream() 落地(含 disabled 复位)
    after = page.evaluate("""() => {
        const b = document.getElementById('btn-continue-check');
        return {
            modalHidden: document.getElementById('tier-modal').classList.contains('hidden'),
            active: document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null,
            disabled: !!b.disabled,
            rects: b.getClientRects().length,
        };
    }""")
    return {"before": before, "after": after}


def g4(page, tmp_root):
    item = "g4"
    print("\n=== g4: F1-d 成功路径 —— 选档成功后焦点交还 #btn-continue-check ===", flush=True)

    # —— 实例 1/2:正向(本项的判定对象)——
    r1 = _g4_enter_and_choose(page, item, "实例 1/2 正向", tmp_root, mutate_focus=False)
    if r1 is not None:
        if r1["before"] == "btn-tier-loose":
            info("g4 缺陷前提:点击前焦点在弹窗内", str(r1["before"]))
        else:
            blocked(item, "g4 实例 1/2 缺陷前提:焦点此刻在弹窗内、即将因隐藏而失效",
                    "btn-tier-loose", str(r1["before"]),
                    "焦点不在档位按钮上 ⇒ 本项要断言的「丢失」不在现场,不可记 PASS")
        ok_true(item, "g4 实例 1/2 选档后 #tier-modal 已隐藏",
                r1["after"]["modalHidden"] is True, "hidden=true",
                f"hidden={r1['after']['modalHidden']}")
        if r1["after"]["disabled"] or r1["after"]["rects"] <= 0:
            # 禁用按钮上的 .focus() 是 no-op:此时记 PASS 会交付一个静默失效的修复
            blocked(item, "g4 实例 1/2 交还时 #btn-continue-check 可聚焦(断言前提,防 no-op 假绿)",
                    "disabled=false 且可见",
                    f"disabled={r1['after']['disabled']} rects={r1['after']['rects']}",
                    "目标不可聚焦 ⇒ 下一条断言会空转,故记 BLOCKED 而不是放行")
        else:
            ok_true(item, "g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径)",
                    r1["after"]["active"] == "btn-continue-check",
                    "btn-continue-check", str(r1["after"]["active"]))

    # —— 实例 2/2:判别控制(证明上面的绿不是恒绿)——
    # 必须先 reload:模块级 tierModalShown 在第一次进入之后仍为 true,不 reload 时第二个
    # 项目的档位弹窗根本不会自动打开,控制会退化成空转(规划期实测)。
    page.reload(wait_until="domcontentloaded")
    r2 = _g4_enter_and_choose(page, item, "实例 2/2 判别控制", tmp_root, mutate_focus=True)
    if r2 is not None:
        ok_true(item, "g4 判别控制:交还调用被置空后焦点不再落在 #btn-continue-check(证明实例 1 的绿非恒绿)",
                r2["after"]["active"] != "btn-continue-check",
                "active != btn-continue-check", str(r2["after"]["active"]))


ITEMS = {"g1": g1, "g2": g2, "g3": g3, "g4": g4}


def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="idi-08 Nyquist 缺口补齐 harness")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:g1 / g2 / g3 / g4(可重复,或逗号分隔)")
    ap.add_argument("--keep", action="store_true", help="保留临时工作目录供排查")
    return ap.parse_args()


def main():
    args = parse_args()
    items = []
    for chunk in (args.item or []):
        items.extend(p.strip() for p in chunk.split(",") if p.strip())
    if not items:
        items = list(ITEMS)
    bad = [i for i in items if i not in ITEMS]
    if bad:
        raise SystemExit(f"ERROR: 未知项 {bad}(可用:{sorted(ITEMS)})")

    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi08-gap-"))
    info("tmp", f"临时工作目录 {tmp_root}(--keep 可保留)")
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        # 捆绑 chromium(与 check-06 同款):本机 x86_64 venv 下 chrome 路线的 headless 会挂死
        browser = pw.chromium.launch(headless=True)
        info("browser.version", browser.version)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)
        for name in items:
            ITEMS[name](page, tmp_root)
    finally:
        if browser is not None:
            browser.close()
        if pw is not None:
            pw.stop()
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except Exception:
                server.kill()
            info("server", "已关闭本次自起的 uvicorn")
        if not args.keep:
            shutil.rmtree(tmp_root, ignore_errors=True)

    print("\n=== 逐项结论 ===", flush=True)
    verdicts = {}
    for i in items:
        v = c05.item_verdict(i)
        verdicts[i] = v
        rows = [r for r in c05.ROWS if r["item"] == i]
        fails = len([r for r in rows if r["verdict"] == "FAIL"])
        blocks = len([r for r in rows if r["verdict"] == "BLOCKED"])
        print(f"item {i}: {v.upper()}  ({len(rows)} 条断言,{fails} FAIL,{blocks} BLOCKED)", flush=True)
    any_fail = any(v == "fail" for v in verdicts.values())
    any_blocked = any(v == "blocked" for v in verdicts.values())
    code = 1 if any_fail else (2 if any_blocked else 0)
    print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())