"""Review board for the twin method: up to 4 takes of one scene, plus a strip with Max cut from the approved
twin (green frame) next to Max cut from every take, so the reviewer compares the dog to the dog.

Usage (from the skill folder):
  python3 scripts/twin_board.py OUT.jpg TWIN "Title" TAKE1.png [TAKE2.png TAKE3.png TAKE4.png]
TWIN is the twin key (G1, G3, F1, L02, L05, L06, L08, G4); its crop is assets/twins/max-TWIN.jpg.
Max is found by his golden fur (largest golden area); if a take has two dogs the strip shows the larger one,
and two dogs is a reject anyway.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def font(size):
    for p in ('/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def golden_mask(im, step):
    small = im.convert('RGB').resize((max(1, im.width // step), max(1, im.height // step)))
    hsv = np.asarray(small.convert('HSV')).astype(int)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1], hsv[..., 2]
    return (h >= 18) & (h <= 45) & (s > 90) & (v > 110)


def largest_box(m):
    """Bounding box of the largest 4-connected True area (iterative flood fill, no SciPy)."""
    seen = np.zeros_like(m, bool); best = (0, None)
    H, W = m.shape
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]; seen[y0, x0] = True; n = 0; ys = []; xs = []
        while stack:
            y, x = stack.pop(); n += 1; ys.append(y); xs.append(x)
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True; stack.append((yy, xx))
        if n > best[0]:
            best = (n, (min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return best[1]


def dilate(m, r):
    """Grow the mask by r cells so the navy collar no longer splits the head from the body."""
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def crop_max(im, step=8):
    b = largest_box(dilate(golden_mask(im, step), 3))
    if not b:
        return im
    x0, y0, x1, y1 = [v * step for v in b]
    m = int(0.08 * max(x1 - x0, y1 - y0))
    return im.crop((max(0, x0 - m), max(0, y0 - m), min(im.width, x1 + m), min(im.height, y1 + m)))


def main():
    if len(sys.argv) < 5 or sys.argv[1] in ('-h', '--help'):
        print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 1)
    out, twin, title, takes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:8]
    W, H, CH = 1264, 848, 560
    B = Image.new('RGB', (2 * W + 30, 90 + 2 * (H + 60) + CH + 80), 'white'); d = ImageDraw.Draw(B)
    d.text((10, 20), f'{title} · twin {twin}', font=font(44), fill=(0, 52, 105))
    ims = [Image.open(t).convert('RGB') for t in takes]
    for i, im in enumerate(ims):
        x, y = 10 + (i % 2) * (W + 10), 90 + (i // 2) * (H + 60)
        d.text((x, y), f'take {i + 1}: {os.path.basename(takes[i])}', font=font(32), fill='black')
        B.paste(im.resize((W, H)), (x, y + 44))
    y = 90 + 2 * (H + 60) + 20
    d.text((10, y), 'Max close up: approved twin (green frame), then each take', font=font(32), fill='black'); y += 44
    crops = [Image.open(os.path.join(HERE, 'assets', 'twins', f'max-{twin}.jpg')).convert('RGB')] + [crop_max(im) for im in ims]
    x = 10
    for j, c in enumerate(crops):
        c.thumbnail((500, CH)); B.paste(c, (x, y))
        if j == 0:
            d.rectangle([x, y, x + c.width, y + c.height], outline=(25, 167, 85), width=8)
        x += c.width + 15
    B.save(out, quality=88); print(out)


if __name__ == '__main__':
    main()
