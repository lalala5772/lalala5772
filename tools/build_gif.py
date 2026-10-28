"""tools/frames/*.png → assets/nabibobetttau.gif (공용 팔레트로 깜빡임 없이)"""
import glob
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frames = [Image.open(f).convert("RGB") for f in sorted(glob.glob(os.path.join(ROOT, "tools", "frames", "*.png")))]
w, h = frames[0].size
sheet = Image.new("RGB", (w, h * 4))
for i, f in enumerate(frames[::max(1, len(frames) // 4)][:4]):
    sheet.paste(f, (0, h * i))
palette = sheet.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
out = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
dst = os.path.join(ROOT, "assets", "nabibobetttau.gif")
out[0].save(dst, save_all=True, append_images=out[1:], duration=80, loop=0, optimize=True, disposal=1)
print(f"{dst}: {len(out)} frames, {os.path.getsize(dst) / 1024:.0f} KB")
