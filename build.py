#!/usr/bin/env python3
"""Builds yorha.theme.json from yorha.css and the palettes below, plus static HTML previews."""
import json, re, sys, pathlib

here = pathlib.Path(__file__).parent
css = (here / "yorha.css").read_text()
mini = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
mini = re.sub(r"\s*\n\s*", "", mini).strip()

LIGHT = dict(
    canvas="#c8c3ab", chrome="#bdb8a0", toolbar="#bdb8a0", toolbarForeground="#454138",
    toolbarBorder="#a09b86", toolbarControl="#b4af9a", toolbarControlForeground="#454138",
    toolbarControlHover="#a8a38e",
    surface="#dad4bb", surfaceRaised="#e0dac2", surfaceOverlay="#dad4bb",
    text="#454138", textMuted="#555147", border="#a09b86", input="#b0ab96", focus="#cd664d",
    accent="#4e4b42", accentForeground="#dad4bb",
    secondary="#b4af9a", secondaryForeground="#454138", muted="#beb9a2", mutedForeground="#555147",
    placeholder="#777262", secondaryLabel="#555147", iconMuted="#676355",
    error="#a03c28", errorForeground="#7a2a1a", errorSurface="#d6b39c",
    warning="#7d5f17", warningForeground="#5e4610", warningSurface="#e4dbad",
    update="#3b6860", updateForeground="#2a4d47", updateSurface="#c3ccb5",
    accentSurface="#b4af9a", accentSurfaceForeground="#454138",
    messageSurface="#4e4b42", messageForeground="#dad4bb",
    messageAction="#676355", messageActionForeground="#dad4bb", messageActionHover="#777262",
    codeBackground="#d6d0b8", codeForeground="#454138",
    searchMatchBackground="#e4dbad", searchMatchForeground="#2b2923",
    searchMatchActiveBackground="#cd664d", searchMatchActiveForeground="#2b2923",
    sidebar="#bdb8a0", sidebarForeground="#454138", sidebarMutedForeground="#555147",
    sidebarControlSurface="#b4af9a", sidebarRowHover="#b4af9a", sidebarRowActive="#a8a38e",
    sidebarRowSelected="#b4af9a", sidebarBorder="#a09b86",
    terminalBackground="#d0cab2", terminalForeground="#454138", terminalCursor="#cd664d",
    terminalSelection="#b4af9a", terminalScrollbar="#a09b86", terminalScrollbarHover="#676355",
)
DARK = dict(
    canvas="#38352d", chrome="#302e27", toolbar="#302e27", toolbarForeground="#dad4bb",
    toolbarBorder="#5f5b4e", toolbarControl="#454138", toolbarControlForeground="#dad4bb",
    toolbarControlHover="#55524a",
    surface="#403d34", surfaceRaised="#4a463c", surfaceOverlay="#454138",
    text="#dad4bb", textMuted="#aaa590", border="#5f5b4e", input="#55524a", focus="#cd664d",
    accent="#dad4bb", accentForeground="#38352d",
    secondary="#454138", secondaryForeground="#dad4bb", muted="#403d34", mutedForeground="#aaa590",
    placeholder="#8a8573", secondaryLabel="#aaa590", iconMuted="#9a9581",
    error="#e58a72", errorForeground="#f2b3a1", errorSurface="#553528",
    warning="#d9b45b", warningForeground="#e9cf92", warningSurface="#4f4428",
    update="#9dbfb2", updateForeground="#bdd6cc", updateSurface="#364840",
    accentSurface="#4d493e", accentSurfaceForeground="#dad4bb",
    messageSurface="#dad4bb", messageForeground="#38352d",
    messageAction="#bab5a1", messageActionForeground="#38352d", messageActionHover="#a8a38e",
    codeBackground="#2e2c25", codeForeground="#dad4bb",
    searchMatchBackground="#6b6759", searchMatchForeground="#f3ecd6",
    searchMatchActiveBackground="#cd664d", searchMatchActiveForeground="#2e2c25",
    sidebar="#302e27", sidebarForeground="#dad4bb", sidebarMutedForeground="#a39e89",
    sidebarControlSurface="#3d3a32", sidebarRowHover="#3d3a32", sidebarRowActive="#4d493e",
    sidebarRowSelected="#4d493e", sidebarBorder="#5f5b4e",
    terminalBackground="#2e2c25", terminalForeground="#dad4bb", terminalCursor="#cd664d",
    terminalSelection="#6b6759", terminalScrollbar="#5f5b4e", terminalScrollbarHover="#9a9581",
)

def rest(d):
    return {k: v for k, v in d.items() if k not in ("canvas", "accent")}

theme = dict(version=1, name="YoRHa", appearance="light", canvas=LIGHT["canvas"],
             accent=LIGHT["accent"], colors=rest(LIGHT), variants=dict(dark=DARK), css=mini)
(here / "yorha.theme.json").write_text(json.dumps(theme, indent=1))
print("css chars:", len(mini))

def mock(mode):
    c = LIGHT if mode == "light" else DARK
    v = {"--background": c["canvas"], "--sidebar": c["sidebar"]}
    root = ";".join(f"{k}:{val}" for k, val in v.items())
    cls = "dark" if mode == "dark" else ""
    sel = "b" if mode == "light" else "b"
    return f"""<!doctype html><html class="{cls}"><head><meta charset="utf-8"><style>
html,body{{margin:0}} html{{padding:0!important;{root}}}
.app{{display:grid;grid-template-columns:250px 1fr;height:640px;font:13px/1.5 var(--font-sans);color:{c['text']};background:{c['canvas']};border:1px solid {c['border']}}}
[data-slot=sidebar-inner]{{background:{c['sidebar']};height:100%;padding:10px 12px 10px 8px;box-sizing:border-box;color:{c['sidebarForeground']}}}
.proj{{display:flex;gap:8px;align-items:center;margin:12px 0 4px;color:{c['sidebarMutedForeground']};font-size:12px}}
li{{list-style:none}} ul{{margin:0;padding:0}}
.row{{display:flex;justify-content:space-between;padding:5px 8px;color:{c['sidebarMutedForeground']}}}
.row:hover{{background:{c['sidebarRowHover']}}}
.row[data-active=true]{{background:{c['sidebarRowSelected']};color:{c['sidebarForeground']};font-weight:500}}
main{{position:relative;display:flex;flex-direction:column;min-width:0}}
[data-chat-header]{{position:relative;height:40px;box-sizing:border-box;padding:0 16px;display:flex;justify-content:space-between;align-items:center;background:{c['canvas']}}}
.tl{{flex:1;padding:18px 40px 18px 250px;overflow:hidden}}
[data-user-message-bubble]{{background:{c['messageSurface']};color:{c['messageForeground']};padding:9px 13px;max-width:70%;margin-left:auto;width:fit-content}}
.chat-markdown{{max-width:620px;margin-top:18px}} .chat-markdown h2{{font-size:16px;margin:0 0 8px}}
.chat-markdown p{{margin:8px 0}} .chat-markdown code{{background:{c['codeBackground']};padding:1px 4px;font-size:12px}}
.chat-markdown-codeblock{{background:{c['codeBackground']};color:{c['codeForeground']};padding:10px 12px;font:12px/1.5 ui-monospace,monospace;margin:10px 0}}
.muted{{color:{c['textMuted']}}}
[data-slot=composer-host]{{margin:0 40px 22px 250px;background:{c['surface']};padding:10px 12px}}
.composer-tiptap{{color:{c['placeholder']};min-height:38px}}
.bar{{display:flex;gap:6px;justify-content:space-between}}
[data-slot=button]{{border:1px solid {c['border']};background-color:transparent;color:{c['text']};padding:3px 9px;font:inherit;font-size:12px;cursor:pointer}}
[data-slot=button].pri{{background-color:{c['accent']};color:{c['accentForeground']};border-color:{c['accent']}}}
[data-slot=menu-popup]{{position:absolute;right:56px;top:58px;background:{c['surfaceOverlay']};width:190px;padding:4px}}
[data-slot=menu-popup] div{{padding:5px 9px}}
.err{{color:{c['error']}}} .ok{{color:{c['update']}}} .warn{{color:{c['warning']}}}
{css}
/* previews are static: freeze the animations */
*,*::before,*::after{{animation:none!important}}
</style></head><body><div class="app" style="position:relative">
<div data-slot="sidebar"><div data-slot="sidebar-inner">
 <div style="display:flex;justify-content:space-between;align-items:center"><b style="letter-spacing:.08em">T3 Code</b><button data-slot="button">New thread</button></div>
 <div class="proj"><span data-slot="project-monogram" style="display:inline-grid;place-items:center;width:18px;height:18px;background:{c['secondary']};font-size:9px">AT</span>atlas</div>
 <ul><li data-thread-item><div class="row" aria-current="page"><span>YoRHa theme</span><span>2m</span></div></li>
 <li data-thread-item><div class="row"><span>Fix the login redirect</span><span>1h</span></div></li>
 <li data-thread-item><div class="row"><span>Weekly metrics report</span><span>3h</span></div></li></ul>
 <div class="proj"><span data-slot="project-monogram" style="display:inline-grid;place-items:center;width:18px;height:18px;background:{c['secondary']};font-size:9px">BC</span>beacon</div>
 <ul><li data-thread-item><div class="row"><span>Migrate the job queue</span><span>1d</span></div></li>
 <li data-thread-item><div class="row"><span>Review pull request #212</span><span>2d</span></div></li></ul>
</div></div>
<main data-workspace-area="conversation">
 <div data-chat-header><span>YoRHa theme</span><span style="display:flex;gap:6px"><button data-slot="button">Diff</button><button data-slot="button">Terminal</button></span></div>
 <div class="tl">
  <div data-user-message-bubble>Make a custom theme inspired by NieR: Automata.</div>
  <div class="chat-markdown">
   <h1 style='font-size:19px;margin:0 0 12px'>YoRHa</h1><h2>Theme applied</h2><blockquote style='margin:8px 0;padding:4px 0'>Systematic and sterile, but also beautiful.</blockquote><h3 style='font-size:13px;margin:10px 0 4px'>How to undo</h3>
   <p>The <code>yorha</code> theme changes the palette and squares every corner. <span class="muted">The selected sidebar row is inverted.</span></p>
   <div class="chat-markdown-codeblock">python3 build.py<br><span class="ok">ok</span> theme built &nbsp; <span class="warn">1 warning</span> &nbsp; <span class="err">0 errors</span></div>
   <p>To go back, pick a <a href='#'>built-in theme</a> in the settings.</p>
  </div>
 </div>
 <div data-slot="composer-host"><div class="composer-tiptap">Ask for a change…</div>
  <div class="bar"><span style="display:flex;gap:6px"><button data-slot="button">Fable 5.2</button><button data-slot="button">High</button></span><button data-slot="button" class="pri">Send</button></div></div>
</main>
<div data-slot="menu-popup"><div>Rename</div><div data-highlighted>Pin thread</div><div>Archive</div></div>
</div></body></html>"""

(here / "preview").mkdir(exist_ok=True)
for m in ("light", "dark"):
    (here / "preview" / f"{m}.html").write_text(mock(m))
