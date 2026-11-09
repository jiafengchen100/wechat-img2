# -*- coding: utf-8 -*-
"""封面压图：原始图中心裁切后缩到 1200x510，输出到草稿 assets。System.Drawing 路线（无 Pillow）。"""
import clr
clr.AddReference("System.Drawing")
from System.Drawing import Bitmap, Graphics, Image, Rectangle, GraphicsUnit
from System.Drawing.Drawing2D import InterpolationMode, CompositingQuality, SmoothingMode
from System.Drawing.Imaging import ImageFormat
import os

SRC = r"D:\微信公众号\tools\_state\gif62\cover_raw.jpg"
DST = r"D:\微信公众号\微信公众号\微信公众号\02_草稿\GPT62测评\assets\cover.jpg"
TW, TH = 1200, 510

src = Image.FromFile(SRC)
print("src", src.Width, src.Height, round(src.Width / src.Height, 3))

target_ratio = TW / TH
r = src.Width / src.Height
if r > target_ratio:
    cw, ch = int(src.Height * target_ratio), src.Height
    sx, sy = (src.Width - cw) // 2, 0
else:
    cw, ch = src.Width, int(src.Width / target_ratio)
    sx, sy = 0, (src.Height - ch) // 2

dst = Bitmap(TW, TH)
g = Graphics.FromImage(dst)
g.InterpolationMode = InterpolationMode.HighQualityBicubic
g.CompositingQuality = CompositingQuality.HighQuality
g.SmoothingMode = SmoothingMode.HighQuality
g.DrawImage(src, Rectangle(0, 0, TW, TH), sx, sy, cw, ch, GraphicsUnit.Pixel)
g.Dispose()
dst.Save(DST, ImageFormat.Jpeg)
dst.Dispose()
src.Dispose()
print("out", DST, os.path.getsize(DST), "bytes")
