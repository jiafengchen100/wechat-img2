# -*- coding: utf-8 -*-
"""生成 GPT-6.2 测评稿的动图（HTML 逐帧 -> ffmpeg 合成 GIF）。"""
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

FFMPEG = r"D:\ProgramFiles\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
OUT = Path(r"D:\微信公众号\tools\_state\gif62")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 900, 540

CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
body{width:900px;height:540px;font-family:"Microsoft YaHei","微软雅黑",sans-serif;
     background:linear-gradient(180deg,#ffffff 0%,#fdfaf5 100%);overflow:hidden;}
.title{position:absolute;left:48px;top:32px;font-size:24px;font-weight:700;color:#2f2a24;letter-spacing:.4px;}
.sub{position:absolute;left:48px;top:70px;font-size:13.5px;color:#8b8176;}
.chart{position:absolute;left:48px;right:48px;top:126px;height:278px;}
.cols{display:flex;align-items:flex-end;justify-content:space-around;height:278px;}
.col{position:relative;width:112px;display:flex;justify-content:center;align-items:flex-end;height:278px;}
.bar{width:56px;border-radius:3px 3px 0 0;}
.val{position:absolute;font-size:23px;font-weight:700;color:#2f2a24;text-align:center;width:112px;}
.names{position:absolute;left:48px;right:48px;top:416px;display:flex;justify-content:space-around;}
.nm{width:112px;font-size:13px;color:#5b5248;text-align:center;line-height:1.4;}
.baseline{position:absolute;left:0;right:0;bottom:0;border-top:1px solid #e2d8c8;}
.grid{position:absolute;left:0;right:0;bottom:270px;border-top:1px dashed #e6dccb;}
.gl{position:absolute;left:0;bottom:280px;font-size:11.5px;color:#b3a795;}
.foot{position:absolute;left:48px;bottom:14px;font-size:12px;color:#a89c8d;}
#note{position:absolute;right:0;top:-34px;font-size:13.5px;color:#a8663a;background:#fbf1e6;
      border:1px solid #ecdcc6;border-radius:4px;padding:5px 10px;opacity:0;}
"""


def frame_html_a():
    cols = [
        ("GPT-6.2<br>Sol (Max)", 60, "#c07a3d", 270),
        ("Gemini 4<br>Carbon (high)", 60, "#b9b3ab", 270),
        ("Claude Opus<br>5.5 (Max)", 59, "#b9b3ab", 265),
        ("GPT-6<br>Astra", 57, "#cdc7bf", 256),
        ("GPT-6.1<br>Sol (Max)", 55, "#d8d2ca", 247),
    ]
    parts = []
    names = []
    for i, (name, score, color, hpx) in enumerate(cols):
        parts.append(f"""
        <div class="col">
          <div class="bar" data-h="{hpx}" style="height:0px;background:{color};"></div>
          <div class="val" data-v="{i}" style="bottom:{hpx + 6}px;opacity:0;">{score}</div>
        </div>""")
        names.append(f'<div class="nm">{name}</div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="title">智能指数：60 分是并列，不是独自登顶</div>
<div class="sub">Artificial Analysis Intelligence Index v5.0.1 · 越高越好 · 2026-11-09 快照</div>
<div class="chart">
  <div id="note">两个 60 分，等高</div>
  <div class="cols">{''.join(parts)}</div>
  <div class="baseline"></div>
  <div class="grid"></div>
  <div class="gl">60 分线</div>
</div>
<div class="names">{''.join(names)}</div>
<div class="foot">数据来源：Artificial Analysis 公开榜单</div>
<script>
function setFrame(t){{
  document.querySelectorAll('.col').forEach(function(col,i){{
    var bar = col.querySelector('.bar');
    var val = col.querySelector('.val');
    var h = parseFloat(bar.dataset.h);
    var start = i*0.09;
    var p = Math.min(1, Math.max(0,(t-start)/0.34));
    bar.style.height = (h*p).toFixed(1)+'px';
    val.style.opacity = p>0.92?1:0;
  }});
  var n = document.querySelector('#note');
  n.style.opacity = t>0.88 ? Math.min(1,(t-0.88)/0.12) : 0;
}}
setFrame(0);
</script></body></html>"""


def frame_html_b():
    rows = [
        ("Claude Fable 5.1 (Max)", 12.99, "#d8d2ca"),
        ("Claude Opus 5.5 (Max)", 10.04, "#cdc7bf"),
        ("Gemini 4 Carbon (high)", 7.76, "#c3bcb3"),
        ("GPT-6 Astra (Max)", 6.24, "#b9b3ab"),
        ("GPT-6.2 Sol (Max)", 1.19, "#c07a3d"),
    ]
    bar_max = 470
    vmax = 12.99
    parts = []
    for i, (name, cost, color) in enumerate(rows):
        wpx = cost / vmax * bar_max
        parts.append(f"""
        <div class="row">
          <div class="rname">{name}</div>
          <div class="rtrack"><div class="rbar" data-w="{wpx:.1f}"
               style="width:0px;background:{color};"></div></div>
          <div class="rval" data-v="{i}" style="opacity:0;">${cost:.2f}</div>
        </div>""")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
.rows{{position:absolute;left:48px;right:48px;top:120px;}}
.row{{display:flex;align-items:center;margin-bottom:24px;}}
.rname{{width:196px;font-size:14px;color:#5b5248;}}
.rtrack{{position:relative;width:470px;height:28px;}}
.rbar{{height:28px;border-radius:3px;}}
.rval{{width:74px;text-align:right;font-size:16px;font-weight:700;color:#2f2a24;margin-left:12px;}}
#sum{{position:absolute;left:48px;top:388px;font-size:14.5px;color:#a8663a;background:#fbf1e6;
      border:1px solid #ecdcc6;border-radius:4px;padding:9px 14px;opacity:0;}}
</style></head><body>
<div class="title">单任务成本：对 Opus 是一折，对自家上一代是九五折</div>
<div class="sub">每跑完一整套智能指数的加权平均成本 · 越低越好 · 单位：美元</div>
<div class="rows">{''.join(parts)}</div>
<div id="sum">对 Opus 5.5：11.8%　|　对自家上一代 GPT-6.1 Sol（$1.27）：6%</div>
<div class="foot">数据来源：Artificial Analysis 公开榜单</div>
<script>
function setFrame(t){{
  document.querySelectorAll('.row').forEach(function(row,i){{
    var bar = row.querySelector('.rbar');
    var val = row.querySelector('.rval');
    var w = parseFloat(bar.dataset.w);
    var start = i*0.10;
    var p = Math.min(1, Math.max(0,(t-start)/0.32));
    bar.style.width = (w*p).toFixed(1)+'px';
    val.style.opacity = p>0.92?1:0;
  }});
  var s = document.querySelector('#sum');
  s.style.opacity = t>0.82 ? Math.min(1,(t-0.82)/0.18) : 0;
}}
setFrame(0);
</script></body></html>"""


def shoot(html, frames_dir, n_frames=26):
    """首帧存终态：GIF 被抓成静态图时也有完整画面，不会是一张空柱图。"""
    frames_dir.mkdir(parents=True, exist_ok=True)
    for f in frames_dir.glob("*.png"):
        f.unlink()
    tmp_html = OUT / "frame.html"
    tmp_html.write_text(html, encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(tmp_html.as_uri())
        pg.wait_for_timeout(300)
        # 000 = 终态
        pg.evaluate("setFrame(1.0)")
        pg.wait_for_timeout(50)
        pg.screenshot(path=str(frames_dir / "000.png"))
        # 001.. = 动画
        for i in range(n_frames):
            t = i / (n_frames - 1)
            pg.evaluate(f"setFrame({t:.4f})")
            pg.wait_for_timeout(30)
            pg.screenshot(path=str(frames_dir / f"{i+1:03d}.png"))
        b.close()
    return len(list(frames_dir.glob("*.png")))


def to_gif(frames_dir, out_gif, fps=13):
    cmd = [
        FFMPEG, "-y", "-framerate", str(fps),
        "-i", str(frames_dir / "%03d.png"),
        "-vf", "split[s0][s1];[s0]palettegen=max_colors=180:stats_mode=full[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4",
        "-loop", "0", str(out_gif),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG FAIL")
        print(r.stderr[-1200:])
        sys.exit(1)
    return out_gif.stat().st_size


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "a"
    if which == "a":
        n = shoot(frame_html_a(), OUT / "framesA")
        size = to_gif(OUT / "framesA", OUT / "01-intelligence.gif")
        print(f"A ok frames={n} gif={size/1024/1024:.2f}MB path={OUT/'01-intelligence.gif'}")
    else:
        n = shoot(frame_html_b(), OUT / "framesB")
        size = to_gif(OUT / "framesB", OUT / "02-cost.gif")
        print(f"B ok frames={n} gif={size/1024/1024:.2f}MB path={OUT/'02-cost.gif'}")
