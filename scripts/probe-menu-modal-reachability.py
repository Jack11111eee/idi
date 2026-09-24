#!/usr/bin/env python3
"""一次性探针:验证 UI-REVIEW 优先级修复 2 的可达性。

主张(UI-REVIEW.md 优先级 2):`#selection-menu` 逃过 `inert` 且 `--z-selection-menu (200) >
--z-overlay (100)`,故「确认弹窗打开时菜单仍可见、Tab 一步就落到菜单上」。

本探针实测该前提是否可达:拖拽产生选区使菜单打开 ⇒ 点击 `#btn-authorize` 打开确认弹窗 ⇒
读弹窗与菜单的可见性。

来源级反证(读码所得):`openConfirmModal()` 全文件只有 **一个** 调用点(app.js:559,在
`#btn-authorize` 的 click 处理里),而 app.js:1489 有一个 document 级 `mousedown` 处理器
「点菜单外 ⇒ hideSelectionMenu()」。mousedown 先于 click 触发 ⇒ 菜单在弹窗打开前就已关闭。
本探针把这套推理落成一次实测。

用后即弃,不进 check-07。
"""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "check05_ui_uat", ROOT / "scripts" / "check-05-ui-uat.py")
c05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c05)

# 复用 check-07 已验证可用的拖拽助手 —— 自己重写会踩「坐标落到视口边缘/面板外 ⇒
# 静默空选区」的坑(探针期实测:自写的 <p> 外框拖拽起点 y=900 恰在视口下沿,菜单不弹)。
spec7 = importlib.util.spec_from_file_location(
    "check07_idi08", ROOT / "scripts" / "check-07-idi08-validation.py")
c07 = importlib.util.module_from_spec(spec7)
spec7.loader.exec_module(c07)


def main():
    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="probe-menu-modal-"))
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)

        # p3 样本:#btn-authorize 在此样本是 enabled 且可见(check-07 g1 已用同一前提)
        proj = c05.make_fixture("p3", tmp_root)
        c05.enter_project(page, proj)
        page.wait_for_timeout(400)

        # 1) 拖拽选中正文 ⇒ 菜单应打开(复用 check-07 的已验证助手)
        r = c07._drag_select(page, 0)
        print(f"STEP 1: _drag_select -> {r}")
        page.wait_for_timeout(400)

        menu_open = not page.evaluate(
            "document.getElementById('selection-menu').classList.contains('hidden')")
        sel_len = page.evaluate("window.getSelection().toString().length")
        print(f"STEP 2: 拖拽后 菜单可见={menu_open}  选区长度={sel_len}")
        if not menu_open:
            print("BLOCKED: 拖拽没能打开菜单(前提不成立,无法判定可达性)")
            return 2

        # 2) 点击 #btn-authorize 打开确认弹窗(唯一调用路径)
        print("STEP 3: 点击 #btn-authorize(openConfirmModal 的唯一调用路径)")
        page.click("#btn-authorize")
        page.wait_for_timeout(500)

        modal_open = not page.evaluate(
            "document.getElementById('confirmation-modal').classList.contains('hidden')")
        menu_now = not page.evaluate(
            "document.getElementById('selection-menu').classList.contains('hidden')")
        app_inert = page.evaluate("document.getElementById('app').inert")
        active = page.evaluate(
            "document.activeElement ? (document.activeElement.id || document.activeElement.tagName) : null")
        print(f"STEP 4: 确认弹窗可见={modal_open}  菜单可见={menu_now}  #app.inert={app_inert}  activeElement={active}")

        if not modal_open:
            print("BLOCKED: 确认弹窗没打开(前提不成立)")
            return 2

        print()
        if menu_now:
            print("RESULT: 修复 2 的前提【可达】—— 弹窗打开时菜单仍可见(UI-REVIEW 主张成立)")
            return 1
        print("RESULT: 修复 2 的前提【不可达】—— 弹窗打开时菜单已隐藏(UI-REVIEW 主张不成立)")
        return 0
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
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
