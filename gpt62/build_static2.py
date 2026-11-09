# -*- coding: utf-8 -*-
"""补两张静态图：规格卡、三维定位气泡图。"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import math

OUT = Path(r"D:\微信公众号\tools\_state\gif62")
W, H = 900, 540

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:900px;height:540px;font-family:"Microsoft YaHei","微软雅黑",sans-serif;
     background:linear-gradient(180deg,#ffffff 0%,#fdfaf5 100%);overflow:hidden;}
.title{position:absolute;left:48px;top:30px;font-size:23px;font-weight:700;color:#2f2a24;}
.sub{position:absolute;left:48px;top:66px;font-size:13px;color:#8b8176;}
.foot{position:absolute;left:48px;bottom:14px;font-size:12px;color:#a89c8d;}
"""


def html_spec():
    cells = [
        ("上下文窗口", "1,000,000", "token，约等于 150 万字"),
        ("输入模态", "文本 + 图像", "能读图，不只能读字"),
        ("输出模态", "纯文本", "不生成图片或视频"),
        ("API 定价", "$2 / $10", "每百万输入 / 输出 token"),
        ("单任务成本", "$1.19", "跑完一整套智能指数"),
        ("当前状态", "灰度中", "API 目录查不到，未正式发布"),
    ]
    parts = []
    for i, (k, v, note) in enumerate(cells):
        col = i % 3
        row = i // 3
        x = 48 + col * 272
        y = 116 + row * 172
        hl = "color:#c07a3d;" if k in ("单任务成本", "当前状态") else "color:#2f2a24;"
        parts.append(f"""
        <div style="position:absolute;left:{x}px;top:{y}px;width:248px;height:148px;
             background:#fdf8f1;border:1px solid #eee2cf;border-radius:8px;">
          <div style="position:absolute;left:18px;top:18px;font-size:12.5px;color:#8b8176;">{k}</div>
          <div style="position:absolute;left:18px;top:42px;font-size:23px;font-weight:700;{hl}">{v}</div>
          <div style="position:absolute;left:18px;top:84px;width:212px;font-size:12px;color:#8b8176;line-height:1.5;">{note}</div>
        </div>""")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="title">GPT-6.2 Sol 的六格参数</div>
<div class="sub">能读图、不产图，上下文一百万 token，至今没有公开 API</div>
{''.join(parts)}
<div class="foot">数据来源：Artificial Analysis 公开榜单与 OpenAI 定价页</div>
</body></html>"""


def html_position():
    # 坐标轴范围
    x0, x1 = 54.0, 62.0
    y0, y1 = 10.0, 33.0
    px0, px1 = 132, 800
    py0, py1 = 96, 420   # py1 = 底（y 越小越靠下）

    def sx(v):
        return px0 + (v - x0) / (x1 - x0) * (px1 - px0)

    def sy(v):
        return py1 - (v - y0) / (y1 - y0) * (py1 - py0)

    pts = [
        ("GPT-6.2 Sol", 60, 18.7, 1.19, "#c07a3d", "right"),
        ("Gemini 4 Carbon", 60, 31.1, 7.76, "#b9b3ab", "left"),
        ("Claude Opus 5.5", 59, 25.3, 10.04, "#b9b3ab", "left"),
        ("GPT-6 Astra", 57, 20.7, 6.24, "#cdc7bf", "left"),
        ("GPT-6.1 Sol", 55, 20.4, 1.27, "#d8d2ca", "up"),
    ]
    bubbles = []
    labels = []
    for name, idx, mins, cost, color, side in pts:
        cx, cy = sx(idx), sy(mins)
        r = 7 + math.sqrt(cost) * 5.2
        a = 0.95 if name == "GPT-6.2 Sol" else 0.72
        bubbles.append(
            f'<div style="position:absolute;left:{cx - r:.0f}px;top:{cy - r:.0f}px;'
            f'width:{2 * r:.0f}px;height:{2 * r:.0f}px;border-radius:50%;background:{color};opacity:{a};"></div>')
        if side == "right":
            lx, tx, ta = cx + r + 8, cy - 9, "left"
        elif side == "up":
            lx, tx, ta = cx - 63, cy - r - 52, "left"
        else:
            lx, tx, ta = cx - r - 128, cy - 9, "left"
        weight = "700" if name == "GPT-6.2 Sol" else "400"
        lc = "#a8663a" if name == "GPT-6.2 Sol" else "#5b5248"
        labels.append(
            f'<div style="position:absolute;left:{lx:.0f}px;top:{tx:.0f}px;width:126px;text-align:right;'
            f'font-size:12.5px;font-weight:{weight};color:{lc};">{name}<br><span style="font-weight:400;color:#8b8176;">{mins} 分钟 / ${cost:.2f}</span></div>')

    # 网格与刻度
    grid = []
    for v in [55, 57, 59, 61]:
        x = sx(v)
        grid.append(f'<div style="position:absolute;left:{x:.0f}px;top:{py0}px;width:0;height:{py1 - py0}px;border-left:1px dashed #ece3d4;"></div>')
        grid.append(f'<div style="position:absolute;left:{x - 12:.0f}px;top:{py1 + 8}px;font-size:11.5px;color:#a89c8d;">{v}</div>')
    for v in [15, 20, 25, 30]:
        y = sy(v)
        grid.append(f'<div style="position:absolute;left:{px0}px;top:{y:.0f}px;width:{px1 - px0}px;height:0;border-top:1px dashed #ece3d4;"></div>')
        grid.append(f'<div style="position:absolute;left:{px0 - 34}px;top:{y - 8:.0f}px;font-size:11.5px;color:#a89c8d;">{v}</div>')

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
.axisx{{position:absolute;left:{px0}px;top:{py1}px;width:{px1 - px0}px;height:0;border-top:1.5px solid #ddd2c0;}}
.axisy{{position:absolute;left:{px0}px;top:{py0}px;width:0;height:{py1 - py0}px;border-left:1.5px solid #ddd2c0;}}
.xlbl{{position:absolute;left:{px0}px;top:{py1 + 26}px;width:{px1 - px0}px;text-align:center;font-size:12px;color:#8b8176;}}
.ylbl{{position:absolute;left:44px;top:{py0 - 6}px;width:60px;font-size:12px;color:#8b8176;}}
.quad{{position:absolute;left:180px;top:366px;width:240px;font-size:11.5px;color:#a89c8d;line-height:1.6;text-align:left;}}
</style></head><body>
<div class="title">把三个指标放到一张图上，它站在右下角</div>
<div class="sub">横轴智能指数（越右越强）· 纵轴耗时（越下越快）· 气泡大小＝单任务成本</div>
<div class="quad">右上：又强又慢又贵<br>左下：又快又省，分数略低</div>
<div class="axisx"></div><div class="axisy"></div>
<div class="xlbl">智能指数（分）</div>
<div class="ylbl">分钟</div>
{''.join(grid)}
{''.join(bubbles)}
{''.join(labels)}
<div class="foot">数据来源：Artificial Analysis 公开榜单</div>
</body></html>"""


def shoot(html, out_png):
    tmp = OUT / "static2.html"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(out_png))
        b.close()
    return out_png


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "spec"
    if which == "spec":
        p1 = shoot(html_spec(), OUT / "05-spec.png")
        print("spec ok", p1.name, p1.stat().st_size)
    else:
        p2 = shoot(html_position(), OUT / "06-position.png")
        print("position ok", p2.name, p2.stat().st_size)
