import re, io, sys
p = r"D:\微信公众号\微信公众号\微信公众号\02_草稿\GPT62测评\GPT62测评-初稿.md"
t = open(p, encoding="utf-8").read()
parts = t.split("---", 2)
head, fm, body = parts[0], parts[1], parts[2]
# 正文里成对的半角双引号 -> 中文引号
body2 = re.sub(r'"([^"\n]{1,60})"', "\u201c\\1\u201d", body)
open(p, "w", encoding="utf-8", newline="").write(head + "---" + fm + "---" + body2)
n1 = body2.count("\u201c")
print("pairs replaced:", n1)
print("leftover ascii quote:", body2.count('"'))