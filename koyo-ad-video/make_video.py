#!/usr/bin/env python3
"""向洋ハウジング Meta/Instagram リール広告（仮版）を書き出す。
1080x1920 / 30fps / 約18秒。冒頭フックだけ差し替えた3本を出力する。
使い方: python3 make_video.py  → out/ に mp4 とサムネイル png
写真は実写素材が届いたら PHOTOS の中身を差し替えるだけでよい。
"""
import os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "edge-asset", "img")
OUT = os.path.join(HERE, "out")
W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
YELLOW = (255, 221, 0)
WHITE = (255, 255, 255)
NAVY = (12, 28, 56)

PHOTOS = {
    "president": "tanioka.jpg",      # 谷岡社長（実写）
    "frame": "4UVtFIfK1eo.jpg",      # 構造（仮：ストック写真→自社の構造現場に差し替え）
    "house": "-MVSfkR4xz4.jpg",      # 外観（仮：ストック写真→自社の施工事例に差し替え）
}

HOOKS = {
    "A_nobeoka": [("延岡で家を建てる人へ", 84, WHITE), ("ちょっと待って！", 150, YELLOW)],
    "B_jishin":  [("南海トラフに備える", 84, WHITE), ("家の選び方", 150, YELLOW)],
    "C_koumuten": [("工務店選び", 96, WHITE), ("ここ見てますか？", 130, YELLOW)],
}

# (開始秒, 終了秒, 写真, テキスト行, ズーム方向)
def scenes(hook):
    return [
        (0.0, 2.6, "president", hook, "in"),
        (2.6, 6.2, "frame", [("その家", 96, WHITE), ("地震の“計算”", 130, YELLOW), ("してますか？", 96, WHITE)], "in"),
        (6.2, 10.4, "president", [("向洋ハウジングは", 88, WHITE), ("全棟", 170, YELLOW), ("許容応力度計算", 118, YELLOW)], "out"),
        (10.4, 14.4, "house", [("木造の住まいやすさ", 80, WHITE), ("×", 90, YELLOW), ("鉄骨梁の強さ", 110, YELLOW), ("パナソニック テクノストラクチャー工法", 46, WHITE)], "in"),
        (14.4, 18.4, "president", [("完成見学会", 130, WHITE), ("予約受付中", 150, YELLOW)], "cta"),
    ]

def font(size):
    return ImageFont.truetype(FONT, size)

def cover(img, scale, cx=0.5, cy=0.42):
    """9:16 に cover でクロップしつつ scale 倍ズーム"""
    iw, ih = img.size
    base = max(W / iw, H / ih) * scale
    nw, nh = int(iw * base), int(ih * base)
    im = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - W) * cx); y = int((nh - H) * cy)
    x = max(0, min(x, nw - W)); y = max(0, min(y, nh - H))
    return im.crop((x, y, x + W, y + H))

def text_block(lines):
    """テロップ（太字風：縁取り＋影）を透明レイヤーで返す"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    heights = []
    for t, s, c in lines:
        f = font(s); bb = d.textbbox((0, 0), t, font=f, stroke_width=max(3, s // 22))
        heights.append(bb[3] - bb[1])
    gap = 26
    total = sum(heights) + gap * (len(lines) - 1)
    y = int(H * 0.44 - total / 2)
    for (t, s, c), h in zip(lines, heights):
        f = font(s); sw = max(3, s // 22)
        bb = d.textbbox((0, 0), t, font=f, stroke_width=sw)
        tw = bb[2] - bb[0]
        if tw > W - 80:  # はみ出し防止
            s2 = int(s * (W - 80) / tw); f = font(s2); sw = max(3, s2 // 22)
            bb = d.textbbox((0, 0), t, font=f, stroke_width=sw); tw = bb[2] - bb[0]
        x = (W - tw) // 2 - bb[0]
        # 影
        d.text((x + 6, y + 8 - bb[1]), t, font=f, fill=(0, 0, 0, 170), stroke_width=sw + 6, stroke_fill=(0, 0, 0, 170))
        # 本体（同色ストロークで太字化）＋黒縁
        d.text((x, y - bb[1]), t, font=f, fill=c, stroke_width=sw + 3, stroke_fill=(0, 0, 0))
        d.text((x, y - bb[1]), t, font=f, fill=c, stroke_width=sw // 2, stroke_fill=c)
        y += h + gap
    return layer

def footer(d, cta=False, pulse=1.0):
    # ロゴ帯（上部）
    d.rectangle([0, 150, W, 230], fill=(*NAVY, 210))
    f = font(46)
    t = "延岡市の工務店｜向洋ハウジング"
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, 165), t, font=f, fill=WHITE, stroke_width=1, stroke_fill=WHITE)
    if cta:
        bw, bh = int(760 * pulse), int(150 * pulse)
        x0, y0 = (W - bw) // 2, int(H * 0.70) - bh // 2
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=30, fill=YELLOW, outline=(0, 0, 0), width=6)
        f2 = font(int(66 * pulse)); t2 = "▼ 下のボタンから予約"
        tw2 = d.textlength(t2, font=f2)
        d.text(((W - tw2) / 2, y0 + (bh - 66 * pulse) / 2 - 6), t2, font=f2, fill=(0, 0, 0), stroke_width=2, stroke_fill=(0, 0, 0))
        f3 = font(40); t3 = "〇月〇日（〇）〜〇日（〇）　延岡市〇〇町"
        tw3 = d.textlength(t3, font=f3)
        d.text(((W - tw3) / 2, y0 + bh + 30), t3, font=f3, fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))

def ease_out(x):
    return 1 - (1 - x) ** 3

def render(name, hook):
    os.makedirs(OUT, exist_ok=True)
    photos = {k: Image.open(os.path.join(IMG, v)).convert("RGB") for k, v in PHOTOS.items()}
    sc = scenes(hook)
    layers = [text_block(s[3]) for s in sc]
    total = sc[-1][1]
    path = os.path.join(OUT, f"koyo_reel_{name}.mp4")
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
        "-c:a", "aac", "-movflags", "+faststart", path], stdin=subprocess.PIPE)
    n = int(total * FPS)
    thumb = None
    for i in range(n):
        t = i / FPS
        idx = next(k for k, s in enumerate(sc) if s[0] <= t < s[1]) if t < total else len(sc) - 1
        t0, t1, ph, _, mode = sc[idx]
        p = (t - t0) / (t1 - t0)
        if mode == "in":
            scale = 1.0 + 0.12 * p
        elif mode == "out":
            scale = 1.14 - 0.12 * p
        else:
            scale = 1.06 + 0.03 * math.sin(p * math.pi)
        cy = 0.30 if ph == "president" else 0.5
        bg = cover(photos[ph], scale, cy=cy)
        # シーン頭の0.18秒だけ横ブレ（国分型の“動き”）
        lt = t - t0
        if lt < 0.18 and idx > 0:
            r = int(40 * (1 - lt / 0.18))
            bg = bg.filter(ImageFilter.BoxBlur(r))
        # 暗幕で文字を読ませる
        arr = np.asarray(bg).astype(np.float32)
        grad = np.linspace(0.55, 0.75, H)[:, None, None]
        arr = arr * (1 - grad * 0.75)
        frame = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert("RGBA")
        # テロップのポップイン
        k = ease_out(min(1.0, lt / 0.25))
        s = 0.82 + 0.18 * k
        L = layers[idx]
        if s < 0.999:
            Ls = L.resize((int(W * s), int(H * s)), Image.BILINEAR)
            L2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            L2.paste(Ls, ((W - Ls.width) // 2, int(H * 0.44 - H * 0.44 * s)))
            L = L2
        if k < 1:
            a = np.asarray(L).copy(); a[..., 3] = (a[..., 3] * k).astype(np.uint8); L = Image.fromarray(a)
        frame.alpha_composite(L)
        d = ImageDraw.Draw(frame)
        footer(d, cta=(mode == "cta"), pulse=1.0 + 0.04 * math.sin(lt * 2 * math.pi * 1.5) if mode == "cta" else 1.0)
        out = frame.convert("RGB")
        if thumb is None and t >= 1.0:
            thumb = out.copy()
        ff.stdin.write(out.tobytes())
    ff.stdin.close(); ff.wait()
    thumb.save(os.path.join(OUT, f"koyo_reel_{name}_thumb.png"))
    return path

if __name__ == "__main__":
    for name, hook in HOOKS.items():
        print(render(name, hook))
