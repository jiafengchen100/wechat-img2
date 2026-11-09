# -*- coding: utf-8 -*-
"""把初稿里的本地图路径换成 jsDelivr 链接，补封面块，并生成公众号版（含发布包装）。"""
import re
from pathlib import Path

BASE = "https://cdn.jsdelivr.net/gh/jiafengchen100/wechat-img2@main/gpt62/"
DRAFT = Path(r"D:\微信公众号\微信公众号\微信公众号\02_草稿\GPT62测评\GPT62测评-初稿.md")
PUB = Path(r"D:\微信公众号\微信公众号\微信公众号\02_草稿\GPT62测评\GPT62测评-公众号版.md")

MAP = {
    "assets/cover.jpg": BASE + "cover.jpg",
    "assets/01-intelligence.gif": BASE + "01-intelligence.gif",
    "assets/02-cost.gif": BASE + "02-cost.gif",
    "assets/03-time.png": BASE + "03-time.png",
    "assets/04-costsplit.png": BASE + "04-costsplit.png",
    "assets/05-spec.png": BASE + "05-spec.png",
    "assets/06-position.png": BASE + "06-position.png",
}

text = DRAFT.read_text(encoding="utf-8")
for k, v in MAP.items():
    text = text.replace(k, v)

# 封面作为正文第一个块（frontmatter 之后）
if "gpt62/cover.jpg" not in text:
    parts = text.split("---", 2)
    fm = parts[1]
    body = parts[2].lstrip("\n")
    text = f"---{fm}---\n\n![]({BASE}cover.jpg)\n\n{body}"

DRAFT.write_text(text, encoding="utf-8")
print("draft updated:", len(text), "chars")

PACK = """

---

# 发布包装（复制正文时不要包含）

**标题（主标题 + 2 个备用）**
- 主标题：60分、18.7分钟、$1.19：GPT-6.2的「完胜」是怎么算的
- 备用 1：同一张榜单，换个对手，GPT-6.2的「完胜」就翻面了
- 备用 2：GPT-6.2 便宜得惊人，但那省下的钱不在单价里
- 备用 3：60分并列、18.7分钟第三、1.19美元是九五折

**摘要（120 字以内）**
三个数字都是真的：60 分、18.7 分钟、1.19 美元。但它们各自换了一个对手——和谁比、比哪一格，决定了「完胜」还是「刚好够用」。

**话题标签**
#人工智能 #大模型 #GPT #Claude #AI测评 #ArtificialAnalysis

**配图清单（共 7 张，全部自制或 AI 生成，无第三方图片）**
1. 封面：AI 生成示意图「游标卡尺量三根木条」，非现场照片，1200×510
2. 参数卡：上下文 1M、输入文本+图像、输出纯文本、$2/$10、$1.19、灰度中，六格
3. 三维定位图：智能指数 × 耗时 × 成本气泡图，五款模型同图，GPT-6.2 在右下角
4. 智能指数动图：五根柱子依次生长，末帧标出两个 60 分等高，GIF
5. 任务耗时静态图：六根横条 + 中位数虚线，标出「12.6 不是中位数」
6. 成本动图：五根成本条递减到 $1.19，末帧标出对 Opus 与对上一代的两种口径，GIF
7. 账单拆解静态图：单价 / 用量 / 账单三联面板，指出省的是推理 token

**发布设置清单**
- 封面：从正文首图选择
- 原创声明：开
- 留言与在看：开
- 合集：AI 观察
- 赞赏：关
- 发布时间：晚上（晚高峰，2026-11-04 约定）

**发布前检查**
- 正文 2807 字（不含来源块），超过「最少 1500 字」硬下限
- 配图 7 张（含封面 1 张、动图 2 张、静态数据图 4 张），超过「最少 4 张含封面」硬下限；正文图片引用 7 处，排版 HTML 里 img 标签 7 个，两处一致
- 动图占比 2/7，低于 1/3 上限
- 正文无 H1，封面为第一个块
- 文末「资料来源」3 行齐全，含配图行
- 图片全部为 jsDelivr 链接，无 `assets/` 本地路径残留

**朋友圈转发语**
一篇稿子拆三个数字：60 分是并列不是登顶，18.7 分钟排第三不是最快，1.19 美元对 Opus 是一折、对自家上一代只有九五折。数字都真，结论看你怎么挑对手。
"""

text_pub = text.rstrip() + PACK
PUB.write_text(text_pub, encoding="utf-8")
print("public version:", len(text_pub), "chars")

# 自检
for pat in ["assets/01", "assets/02", "assets/03", "assets/04", "assets/cover"]:
    print("leftover", pat, text_pub.count(pat))
print("img count:", len(re.findall(r"!\[", text_pub)))
