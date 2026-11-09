# -*- coding: utf-8 -*-
"""生成两张静态数据图（900x540 画布，2x 输出）。"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(r"D:\微信公众号\tools\_state\gif62")
OUT.mkdir(parents=True, exist_ok=True)
W, H = 900, 540

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:900px;height:540px;font-family:"Microsoft YaHei","微软雅黑",sans-serif;
     background:linear-gradient(180deg,#ffffff 0%,#fdfaf5 100%);overflow:hidden;}
.title{position:absolute;left:48px;top:30px;font-size:23px;font-weight:700;color:#2f2a24;}
.sub{position:absolute;left:48px;top:66px;font-size:13px;color:#8b8176;}
.foot{position:absolute;left:48px;bottom:14px;font-size:12px;color:#a89c8d;}
"""


def html_time():
    rows = [
        ("Muse Wonder (Max)", 12.6, "#d8d2ca"),
        ("GPT-6.2 Sol (Max)", 18.7, "#c07a3d"),
        ("GPT-6.1 Sol (Max)", 20.4, "#b9b3ab"),
        ("GPT-6 Astra (Max)", 20.7, "#b9b3ab"),
        ("Claude Opus 5.5 (Max)", 25.3, "#b9b3ab"),
        ("Gemini 4 Carbon (high)", 31.1, "#cdc7bf"),
    ]
    vmax, bar_max = 31.1, 440
    y0 = 130
    step = 58
    parts = []
    for i, (name, v, color) in enumerate(rows):
        top = y0 + i * step
        wpx = v / vmax * bar_max
        parts.append(f"""
        <div style="position:absolute;left:48px;top:{top}px;width:230px;font-size:13.5px;color:#5b5248;">{name}</div>
        <div style="position:absolute;left:284px;top:{top - 1}px;width:{wpx:.1f}px;height:24px;
             background:{color};border-radius:3px;"></div>
        <div style="position:absolute;left:{284 + wpx + 10:.1f}px;top:{top - 2}px;font-size:15px;font-weight:700;color:#2f2a24;">{v}</div>""")
    # 中位数虚线（20.7）
    med_x = 284 + 20.7 / vmax * bar_max
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
#med{{position:absolute;left:{med_x:.1f}px;top:112px;width:0;height:332px;border-left:1px dashed #c9a06a;}}
#medlbl{{position:absolute;left:{med_x + 8:.1f}px;top:94px;font-size:12.5px;color:#a8663a;}}
#tag{{position:absolute;left:284px;top:470px;font-size:12.5px;color:#a8663a;background:#fbf1e6;
      border:1px solid #ecdcc6;border-radius:4px;padding:5px 10px;}}
</style></head><body>
<div class="title">18.7 分钟其实排第三，12.6 也不是中位数</div>
<div class="sub">跑完一整套智能指数需要的推理时间 · 越低越好 · 单位：分钟</div>
<div id="med"></div><div id="medlbl">9 个可见模型的中位数 20.7</div>
{''.join(parts)}
<div id="tag">12.6 是 Muse Wonder 这一根柱子的值，被当成了“全场中位数”</div>
<div class="foot">数据来源：Artificial Analysis 公开榜单</div>
</body></html>"""


def html_costsplit():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
.panel{{position:absolute;top:118px;background:#fdf8f1;border:1px solid #eee2cf;border-radius:8px;}}
.p1{{left:48px;width:250px;height:290px;}}
.p2{{left:325px;width:250px;height:290px;}}
.p3{{left:602px;width:250px;height:290px;}}
.ph{{font-size:13.5px;color:#8b8176;margin:18px 0 0 18px;}}
.big{{font-size:30px;font-weight:700;color:#2f2a24;margin:12px 0 0 18px;}}
.mid{{font-size:15px;color:#5b5248;margin:10px 0 0 18px;}}
.arrow{{font-size:15px;color:#b8ab99;margin:6px 0 0 18px;}}
.hl{{font-size:30px;font-weight:700;color:#c07a3d;margin:12px 0 0 18px;}}
.chg{{font-size:13px;margin:10px 0 0 18px;}}
.keep{{color:#7a8c74;}}
.down{{color:#a8663a;}}
#concl{{position:absolute;left:48px;bottom:52px;right:48px;font-size:14px;color:#a8663a;background:#fbf1e6;
        border:1px solid #ecdcc6;border-radius:5px;padding:10px 14px;}}
</style></head><body>
<div class="title">单价没动，账单砍半：省下来的是推理</div>
<div class="sub">GPT-6 Sol（上一代）与 GPT-6.2 Sol 的逐项对比</div>

<div class="panel p1">
  <div class="ph">API 单价（每百万 token）</div>
  <div class="big">$2 / $10</div>
  <div class="mid">输入 / 输出</div>
  <div class="arrow">↓ 与上一代完全相同</div>
  <div class="chg keep">单价变动 0%</div>
</div>

<div class="panel p2">
  <div class="ph">跑完整套指数用的输出</div>
  <div class="big">6510 万</div>
  <div class="mid">→ 5890 万 token</div>
  <div class="chg down">用量只少约 10%</div>
</div>

<div class="panel p3">
  <div class="ph">单任务成本</div>
  <div class="big">$2.47</div>
  <div class="mid">→ $1.19</div>
  <div class="hl">−52%</div>
</div>

<div id="concl">单价零变化、用量少一成，账单却少了五成——差的那部分只能是推理 token，也就是模型动笔之前“想”的那一段。</div>
<div class="foot">数据来源：Artificial Analysis 公开榜单与 OpenAI API 定价</div>
</body></html>"""


def shoot(html, out_png):
    tmp = OUT / "static.html"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out_png))
        w, h = pg.evaluate("[document.body.scrollWidth, document.body.scrollHeight]")
        b.close()
    return out_png, w, h


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "time"
    if which == "time":
        p1, w, h = shoot(html_time(), OUT / "03-time.png")
        print(f"time ok {p1.name} {p1.stat().st_size} bytes  css={w}x{h}")
    else:
        p2, w, h = shoot(html_costsplit(), OUT / "04-costsplit.png")
        print(f"cost ok {p2.name} {p2.stat().st_size} bytes  css={w}x{h}")
