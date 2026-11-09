# -*- coding: utf-8 -*-
"""把公众号版/头条版 md 处理成归档版（frontmatter 改为 published）。"""
import re
from pathlib import Path

VAULT = Path(r"D:\微信公众号\微信公众号\微信公众号")
DRAFT = VAULT / "02_草稿" / "GPT62测评"
ARCH = VAULT / "03_已发布" / "GPT62测评"
ARCH.mkdir(parents=True, exist_ok=True)

COVER_CDN = "https://cdn.jsdelivr.net/gh/jiafengchen100/wechat-img2@main/gpt62/cover.jpg"


def rebuild_fm(text, extra):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        raise SystemExit("no frontmatter")
    fm_lines = [l for l in m.group(1).splitlines() if l.strip()]
    keys = {l.split(":", 1)[0].strip(): l for l in fm_lines}
    order = []
    for k in ["title", "status", "platform", "cover", "published_at", "tags", "topic_source"]:
        if k in keys:
            order.append(keys[k])
    for k, v in extra.items():
        line = f"{k}: {v}"
        keys[k] = line
        if k not in [o.split(":", 1)[0].strip() for o in order]:
            order.append(line)
            keys[k] = line
    # 用新值覆盖
    final = []
    for line in order:
        k = line.split(":", 1)[0].strip()
        final.append(keys[k])
    body = text[m.end():]
    return "---\n" + "\n".join(final) + "\n---\n" + body


# 公众号版
src = (DRAFT / "GPT62测评-公众号版.md").read_text(encoding="utf-8")
src = re.sub(r"^status:.*$", "status: published", src, count=1, flags=re.M)
src = re.sub(r"^cover:.*$", f"cover: {COVER_CDN}", src, count=1, flags=re.M)
src = re.sub(r"^published_at:.*$", "published_at: 2026-11-09", src, count=1, flags=re.M)
src = re.sub(r"^topic_source:.*$",
             "topic_source: https://mp.weixin.qq.com/s/OEfLzzoBIyHYns5psZVPHQ", src, count=1, flags=re.M)
if "\ntags:" not in src:
    src = src.replace("published_at: 2026-11-09",
                      "published_at: 2026-11-09\ntags: [人工智能, 大模型, GPT, Claude, AI测评]", 1)
(ARCH / "GPT62测评-公众号版.md").write_text(src, encoding="utf-8")
print("pub md ok", len(src))

# 头条版
tt = (DRAFT / "GPT62测评-头条版.md").read_text(encoding="utf-8")
tt = re.sub(r"^status:.*$", "status: published", tt, count=1, flags=re.M)
tt = re.sub(r"^cover:.*$", f"cover: {COVER_CDN}", tt, count=1, flags=re.M)
if "published_at:" in tt:
    tt = re.sub(r"^published_at:.*$", "published_at: 2026-11-09", tt, count=1, flags=re.M)
else:
    tt = tt.replace("platform: toutiao", "platform: toutiao\npublished_at: 2026-11-09", 1)
(ARCH / "GPT62测评-头条版.md").write_text(tt, encoding="utf-8")
print("tt md ok", len(tt))

for f in ["GPT62测评-公众号版.md", "GPT62测评-头条版.md"]:
    head = (ARCH / f).read_text(encoding="utf-8").split("---")[1]
    print("=====", f)
    print(head.strip())
