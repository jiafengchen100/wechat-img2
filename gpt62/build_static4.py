# -*- coding: utf-8 -*-
"""GPT-6.2 测评稿：第三批图（九项评测构成 / 定价两步走）。"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(r"D:\微信公众号\tools\_state\gif62")
W, H = 900, 560

BASE = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:900px;height:100%;font-family:"Microsoft YaHei","微软雅黑",sans-serif;
     background:linear-gradient(180deg,#ffffff 0%,#fdfaf5 100%);overflow:hidden;position:relative;}
.title{position:absolute;left:48px;top:30px;font-size:23px;font-weight:700;color:#2f2a24;}
.sub{position:absolute;left:48px;top:68px;font-size:12.5px;color:#8b8176;}
.foot{position:absolute;left:48px;bottom:14px;font-size:12px;color:#a89c8d;}
"""


def shot(name, html, w=W, h=H):
    tmp = OUT / f"_tmp_{name}.html"
    tmp.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(350)
        pg.screenshot(path=str(OUT / f"{name}.png"))
        b.close()
    return (OUT / f"{name}.png").stat().st_size


# ---------- 12 九项评测构成 ----------
def nine():
    evals = [
        ("AA-Briefcase v1.1", "按真实工作交付物打分，不是选择题"),
        ("AutomationBench-AA", "跨多个应用跑完整业务流程"),
        ("Terminal-Bench 4.0", "命令行里完成多步专业任务"),
        ("FrontierCode 2.0", "代码改动够不够格被合并"),
        ("AA-Omniscience v1.1", "知识广度，以及会不会编"),
        ("GDP.pdf", "从一份 PDF 里做出专业产出"),
        ("HLE-Diamond", "专家级跨学科难题"),
        ("CritPt v2（Hard）", "物理研究级推导"),
        ("Terminal-Bench-Science 0.1", "数据分析、模拟、定理证明"),
    ]
    cards = []
    for i, (n, d) in enumerate(evals):
        hot = i < 9
        cards.append(f"""
        <div class="ev">
          <div class="no">{i + 1:02d}</div>
          <div class="nm">{n}</div>
          <div class="ds">{d}</div>
        </div>""")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .grid{{position:absolute;left:48px;right:48px;top:112px;display:flex;flex-wrap:wrap;gap:10px;}}
    .ev{{width:258px;height:96px;background:#fff;border:1px solid #e6ddd0;border-radius:7px;
         padding:12px 14px;position:relative;}}
    .no{{position:absolute;right:12px;top:10px;font-size:11px;color:#d6cbba;font-weight:700;}}
    .nm{{font-size:13px;font-weight:700;color:#2f2a24;margin-bottom:7px;padding-right:26px;line-height:1.3;}}
    .ds{{font-size:11.5px;color:#8b8176;line-height:1.6;}}
    .concl{{position:absolute;left:48px;right:48px;top:496px;background:#fbf1e6;
            border-left:4px solid #c07a3d;border-radius:0 6px 6px 0;padding:11px 14px;
            font-size:13px;color:#5b5248;line-height:1.7;}}
    </style></head><body>
    <div class="title">那个 60 分，是这九项的加权</div>
    <div class="sub">Artificial Analysis 智能指数 v5.0.1 的构成 · 半页榜单不会告你这件事</div>
    <div class="grid">{''.join(cards)}</div>
    <div class="concl">它考的是「能不能把活干完」，不是「会不会做题」。这也是为什么一个把 3D 场景一次写对的能力，比它在常识问答上多考两分更值得看。</div>
    <div class="foot">依据：Artificial Analysis 智能指数方法论说明</div>
    </body></html>"""
    return shot("12-nineevals", html, W, 590)


# ---------- 13 定价两步走 ----------
def pricing():
    steps = [
        ("2026-09-22", "GPT-6 Sol 发布", "输入 $4 → $2，输出 $20 → $10",
         "OpenAI 官方说法：相对 GPT-5.6 的 API 价格下调 50%", "这一刀，在半年前就砍完了", True),
        ("2026-09-29", "GPT-6.1 Sol 发布", "单价不变，仍是 $2 / $10",
         "官方定位：接近 Astra 的智能，价格是 Astra 的五分之一", "同样的价，卖更好的脑子", False),
        ("2026-11 灰度", "GPT-6.2 Sol 出现", "单价还是 $2 / $10",
         "没有新价格公告，使用统计里先出现模型名", "这一代，没有降价", False),
    ]
    items = []
    y = 122
    for date, name, price, note, verdict, hot in steps:
        bg = "#fbf1e6" if hot else "#ffffff"
        bd = "#ecdcc6" if hot else "#e6ddd0"
        pc = "#a8663a" if hot else "#2f2a24"
        items.append(f"""
        <div class="st" style="top:{y}px;background:{bg};border-color:{bd};">
          <div class="dt">{date}</div>
          <div class="nm">{name}</div>
          <div class="pr" style="color:{pc};">{price}</div>
          <div class="nt">{note}</div>
          <div class="vd">{verdict}</div>
        </div>""")
        y += 150
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .st{{position:absolute;left:48px;right:48px;height:132px;border:1px solid;border-radius:7px;padding:13px 16px;}}
    .dt{{font-size:11.5px;color:#a89c8d;}}
    .nm{{position:absolute;left:16px;top:36px;font-size:14.5px;font-weight:700;color:#2f2a24;}}
    .pr{{position:absolute;left:16px;top:64px;font-size:15px;font-weight:700;}}
    .nt{{position:absolute;left:16px;top:94px;font-size:11.5px;color:#8b8176;}}
    .vd{{position:absolute;right:16px;top:64px;font-size:13px;font-weight:700;color:#c07a3d;width:220px;text-align:right;}}
    .arrow{{position:absolute;left:494px;font-size:15px;color:#c9c2b8;}}
    </style></head><body>
    <div class="title">它便宜，不是因为降价了</div>
    <div class="sub">同一家人的三次定价 · 单价那条线在 9 月就砍完，10 月以后没再动</div>
    {''.join(items)}
    <div class="foot">依据：OpenAI 官方模型发布页与定价说明、Artificial Analysis 定价字段</div>
    </body></html>"""
    return shot("13-pricing", html, W, 590)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "nine"):
        print("12", nine())
    if which in ("all", "pricing"):
        print("13", pricing())
