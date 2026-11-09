# -*- coding: utf-8 -*-
"""GPT-6.2 测评稿：第二批图（矩阵表 / 对照翻面 / 决策卡 / 时间轴）。
路线同 build_static.py：HTML -> Playwright 截图（静态，dsf=2）。
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(r"D:\微信公众号\tools\_state\gif62")
W, H = 900, 640

BASE = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:900px;height:100%;font-family:"Microsoft YaHei","微软雅黑",sans-serif;
     background:linear-gradient(180deg,#ffffff 0%,#fdfaf5 100%);overflow:hidden;position:relative;}
.title{position:absolute;left:48px;top:30px;font-size:23px;font-weight:700;color:#2f2a24;letter-spacing:.3px;}
.sub{position:absolute;left:48px;top:66px;font-size:12.5px;color:#8b8176;}
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


# ---------- 07 矩阵表：九个模型 × 三指标 ----------
def matrix():
    rows = [
        ("GPT-6.2 Sol (Max)", "60", "18.7", "$1.19", "1 / 2 / 1", True),
        ("Gemini 4 Carbon (high)", "60", "31.1", "$7.76", "1 / 8 / 5", False),
        ("Claude Opus 5.5 (Max)", "59", "25.3", "$10.04", "3 / 7 / 7", False),
        ("GPT-6 Astra", "57", "20.7", "$6.24", "4 / 4 / 3", False),
        ("GPT-6.1 Sol (Max)", "55", "20.4", "$1.27", "5 / 3 / 2", False),
        ("Muse Wonder (Full)", "50", "—", "—", "6 / — / —", False),
        ("Claude Fable 5.1 (Max)", "49", "22.6", "$12.99", "7 / 5 / 8", False),
        ("Muse Wonder (Max)", "44", "12.6", "$6.95", "8 / 1 / 4", False),
        ("Grok 4.7 (xhigh)", "35", "24.8", "$7.77", "9 / 6 / 6", False),
    ]
    trs = []
    for i, (name, s, t, c, rk, hot) in enumerate(rows):
        bg = "#fbf1e6" if hot else ("#ffffff" if i % 2 == 0 else "#faf8f4")
        cw = "#c07a3d" if hot else "#3f3a33"
        nm_c = "#a8663a" if hot else "#5b5248"
        trs.append(f"""
        <tr style="background:{bg};">
          <td style="padding:11px 0 11px 14px;font-size:14px;color:{nm_c};">{name}</td>
          <td style="text-align:center;font-size:19px;font-weight:700;color:{cw};">{s}</td>
          <td style="text-align:center;font-size:19px;font-weight:700;color:{cw};">{t}</td>
          <td style="text-align:center;font-size:19px;font-weight:700;color:{cw};">{c}</td>
          <td style="text-align:center;font-size:13px;color:#8b8176;">{rk}</td>
        </tr>""")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .wrap{{position:absolute;left:48px;right:48px;top:108px;border:1px solid #e6ddd0;border-radius:6px;overflow:hidden;background:#fff;}}
    table{{width:100%;border-collapse:collapse;}}
    thead td{{background:#f6ece2;font-size:12.5px;color:#8b8176;padding:9px 0;text-align:center;}}
    thead td:first-child{{text-align:left;padding-left:14px;}}
    .note{{position:absolute;left:48px;right:48px;top:566px;font-size:11.5px;color:#a89c8d;line-height:1.6;}}
    </style></head><body>
    <div class="title">九个模型，一张表：它到底几个第一</div>
    <div class="sub">数值列来自 Artificial Analysis 三张公开榜单 · 名次列按可见模型计 · 2026-11-09 快照</div>
    <div class="wrap">
      <table>
        <thead><tr><td>模型</td><td>智能指数</td><td>耗时（分钟）</td><td>单任务成本</td><td>三项名次</td></tr></thead>
        <tbody>{''.join(trs)}</tbody>
      </table>
    </div>
    <div class="note">名次按有数值的可见模型计：智能指数 9 个、耗时与成本各 8 个。能看见的柱子里，没有一个做到三项全第一。榜单原文对 Muse Wonder 两行的标注不一致，此处按原样列出，缺项以「—」表示。</div>
    <div class="foot">数据来源：Artificial Analysis 公开榜单</div>
    </body></html>"""
    return shot("07-matrix", html)


# ---------- 08 对照翻面：一个分子，两个分母 ----------
def flip():
    groups = [
        ("成本：每次 $1.19",
         ("原文的对照组", "Claude Opus 5.5", "$10.04", "11.8%", "打一折"),
         ("换一个对照组", "自家上一代 GPT-6.1 Sol", "$1.27", "6%", "九五折")),
        ("速度：跑完 18.7 分钟",
         ("原文的对照组", "Claude Opus 5.5", "25.3 分", "快 26%", "快四分之一"),
         ("换一个对照组", "最慢的 Gemini 4 Carbon", "31.1 分", "快 40%", "快四成")),
        ("分数：60 分",
         ("原文的对照组", "Claude Opus 5.5", "59 分", "+1", "领先 1 分"),
         ("换一个对照组", "Gemini 4 Carbon", "60 分", "0", "并列")),
    ]
    blocks = []
    y = 116
    for head, a, b in groups:
        blocks.append(f"""
        <div class="grp" style="top:{y}px;">
          <div class="gh">{head}</div>
          <div class="cards">
            <div class="c c1">
              <div class="cl">{a[0]}</div>
              <div class="cn">{a[1]}</div>
              <div class="cv">{a[2]}</div>
              <div class="cr"><span class="pct">{a[3]}</span><span class="say">{a[4]}</span></div>
            </div>
            <div class="arrow">→</div>
            <div class="c c2">
              <div class="cl">{b[0]}</div>
              <div class="cn">{b[1]}</div>
              <div class="cv">{b[2]}</div>
              <div class="cr"><span class="pct2">{b[3]}</span><span class="say2">{b[4]}</span></div>
            </div>
          </div>
        </div>""")
        y += 168
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .grp{{position:absolute;left:48px;right:48px;height:150px;}}
    .gh{{font-size:14.5px;font-weight:700;color:#2f2a24;margin-bottom:10px;}}
    .cards{{display:flex;align-items:stretch;}}
    .c{{width:368px;border-radius:7px;padding:12px 14px;}}
    .c1{{background:#fbf1e6;border:1px solid #ecdcc6;}}
    .c2{{background:#f4f1ec;border:1px solid #e2dcd2;}}
    .cl{{font-size:11.5px;color:#a89c8d;margin-bottom:5px;}}
    .cn{{font-size:13.5px;font-weight:700;color:#2f2a24;margin-bottom:3px;}}
    .cv{{font-size:12.5px;color:#8b8176;margin-bottom:8px;}}
    .cr{{display:flex;align-items:baseline;}}
    .pct{{font-size:20px;font-weight:700;color:#a8663a;margin-right:10px;}}
    .say{{font-size:12.5px;color:#a8663a;}}
    .pct2{{font-size:20px;font-weight:700;color:#6d6459;margin-right:10px;}}
    .say2{{font-size:12.5px;color:#8b8176;}}
    .arrow{{width:44px;display:flex;align-items:center;justify-content:center;
           font-size:18px;color:#c9c2b8;}}
    </style></head><body>
    <div class="title">同一个数字，换个分母，结论就翻面</div>
    <div class="sub">每行左边＝原文用的对照组，右边＝换一个对照组以后的样子 · 分子始终是它自己的成绩</div>
    {''.join(blocks)}
    <div class="foot">数据来源：Artificial Analysis 公开榜单</div>
    </body></html>"""
    return shot("08-flip", html)


# ---------- 09 决策卡：什么活该用它 ----------
def decision():
    left = [
        ("写可运行的 3D / 可视化代码", "一次生成要同时写对几何、材质、光照、相机"),
        ("前端脚手架、组件、交互原型", "错了立刻能看见，不用等验证"),
        ("批量生成、批量改写", "单任务便宜，量一大差距拉开"),
        ("有明确验收标准的代码活", "跑一遍就知道对不对"),
    ]
    right = [
        ("长链推演、严谨论证", "省推理的代价会在答案深度上还回来"),
        ("多轮反复修正的任务", "它倾向于一次给完，不擅长得寸进尺"),
        ("需要官方支持的生产环境", "灰度、无 API 文档、无法复测"),
        ("依赖多模态输出的活", "能读图，但只吐纯文本"),
    ]
    ls = "".join(
        f"""<div class="it"><div class="it-t">{a}</div><div class="it-d">{b}</div></div>""" for a, b in left)
    rs = "".join(
        f"""<div class="it"><div class="it-t">{a}</div><div class="it-d">{b}</div></div>""" for a, b in right)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .col{{position:absolute;top:112px;width:378px;}}
    .col.l{{left:48px;}} .col.r{{right:48px;}}
    .ch{{font-size:15px;font-weight:700;margin-bottom:12px;padding-left:10px;border-left:4px solid #c07a3d;}}
    .ch.r{{border-left-color:#b9b3ab;color:#6d6459;}}
    .it{{background:#fbf1e6;border-radius:6px;padding:11px 12px;margin-bottom:11px;border:1px solid #ecdcc6;}}
    .col.r .it{{background:#f4f1ec;border-color:#e2dcd2;}}
    .it-t{{font-size:13.5px;font-weight:700;color:#2f2a24;margin-bottom:4px;}}
    .col.r .it-t{{color:#a8663a;}}
    .it-d{{font-size:11.5px;color:#8b8176;line-height:1.55;}}
    </style></head><body>
    <div class="title">什么活现在就该用它，什么活先别碰</div>
    <div class="sub">依据：本轮实测演示的任务类型 + 三个指标的对照组 + 推理 token 的代价 · 属本文判断，非厂商结论</div>
    <div class="col l"><div class="ch">顺手的那一侧</div>{ls}</div>
    <div class="col r"><div class="ch">别急着换的那一侧</div>{rs}</div>
    <div style="position:absolute;left:48px;top:436px;font-size:12px;color:#a89c8d;">判断依据见正文「省下来的是思考，代价也在思考」一节</div>
    </body></html>"""
    return shot("09-decision", html, W, 500)


# ---------- 10 时间轴 ----------
def timeline():
    ev = [
        ("9 月 28 日", "GPT-6.1 Astra 被 OpenAI 自己取消", "内部测试发现它会做出超出用户授权范围的动作", False),
        ("11 月 3 日", "GPT-6.2 Astra 静默灰度被曝", "用量统计里出现 gpt-6.2-astra 标识，最高占单账户当日请求 19.8%", False),
        ("11 月 9 日 12:56", "三张 AA 榜单在中文圈刷屏", "60 分、18.7 分钟、1.19 美元，被读成「完胜 Opus 5.5」", True),
        ("11 月 9 日 下午", "OpenAI 的 API 目录里仍然没有它", "没有公告、没有文档、拿不到公开端点复测", False),
    ]
    items = []
    y0 = 140
    for i, (t, h, d, hot) in enumerate(ev):
        dot = "#c07a3d" if hot else "#c9c2b8"
        tc = "#a8663a" if hot else "#6d6459"
        hc = "#2f2a24" if hot else "#5b5248"
        items.append(f"""
        <div class="ev" style="top:{y0 + i * 108}px;">
          <div class="dot" style="background:{dot};"></div>
          <div class="ln"></div>
          <div class="tm" style="color:{tc};">{t}</div>
          <div class="hd" style="color:{hc};">{h}</div>
          <div class="ds">{d}</div>
        </div>""")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}
    .rail{{position:absolute;left:118px;top:132px;bottom:60px;width:1px;background:#e6ddd0;}}
    .ev{{position:absolute;left:48px;right:48px;height:104px;}}
    .dot{{position:absolute;left:64px;top:2px;width:12px;height:12px;border-radius:50%;}}
    .tm{{position:absolute;left:96px;top:-1px;font-size:13px;font-weight:700;}}
    .hd{{position:absolute;left:96px;top:24px;font-size:15px;font-weight:700;}}
    .ds{{position:absolute;left:96px;top:50px;font-size:12px;color:#8b8176;line-height:1.6;}}
    </style></head><body>
    <div class="title">从被撤掉到被吹爆，只隔了一个半月</div>
    <div class="sub">按时间顺序 · 只有中间那一步是「好数据」，前后两步都是「拿不到」</div>
    <div class="rail"></div>
    {''.join(items)}
    <div class="foot">依据：OpenAI 官方说明、《华尔街日报》报道、钛媒体 2026-11-03 报道、Artificial Analysis 榜单</div>
    </body></html>"""
    return shot("10-timeline", html)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "matrix"):
        print("07", matrix())
    if which in ("all", "flip"):
        print("08", flip())
    if which in ("all", "decision"):
        print("09", decision())
    if which in ("all", "timeline"):
        print("10", timeline())
