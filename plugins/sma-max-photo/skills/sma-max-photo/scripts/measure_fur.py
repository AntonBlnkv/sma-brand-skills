"""Measure Max's fur colour in a frame (read-only: writes nothing). Use it to check the colour bands.

Usage:  python3 scripts/measure_fur.py FRAME.png x0,y0,x1,y1 [--mask MASK.png] [--style day|cin|eve]
- x0,y0,x1,y1  a box around Max (use the box crop.py printed)
- --mask       whole-silhouette mask from max_mask.py for that box (recommended; without it every
               golden-ish pixel in the box counts, so keep the box tight around Max)
- --style      prints whether the frame is inside the band for that treatment
Prints the median hue H (degrees) and saturation S of the mid-tone fur, and the hue on the lit side
(the brightest quarter of the fur pixels, which is what the Evening band is checked on).
Bands (references/prompts.md §3c): Daylight 28–33° · Cinema 26.5–30.5° · Evening 19–28° on the lit side.
Below 19° reads red-brown. Master BO-6 measures about H 30–31°, S 0.58. Always also judge by eye next to BO-6.
"""
import sys
if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'): print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 1)
import numpy as np
from PIL import Image
args = []; opts = {}; argv = sys.argv[1:]; i = 0
while i < len(argv):
    if argv[i].startswith('--'):
        if i + 1 >= len(argv): sys.exit('option %s needs a value' % argv[i])
        opts[argv[i]] = argv[i + 1]; i += 2
    else: args.append(argv[i]); i += 1
frame, box = args[:2]
x0, y0, x1, y1 = map(int, box.split(','))
b = np.asarray(Image.open(frame).convert('RGB').crop((x0, y0, x1, y1))).astype(np.float32) / 255
mx = b.max(-1); mn = b.min(-1); d = mx - mn; r, g, bl = b[..., 0], b[..., 1], b[..., 2]; dd = np.where(d == 0, 1, d)
h = np.where(mx == r, ((g - bl) / dd) % 6, np.where(mx == g, (bl - r) / dd + 2, (r - g) / dd + 4)) * 60
s = np.where(mx == 0, 0, d / np.where(mx == 0, 1, mx)); v = mx
fur = (s > 0.2) & (h > 10) & (h < 55) & (v > 0.2)          # same fur selection idea as recolor_max.py
if opts.get('--mask'):
    m = np.asarray(Image.open(opts['--mask']).convert('L').resize((x1 - x0, y1 - y0))) > 127
    fur &= m
if fur.sum() < 50: sys.exit('too few fur pixels in the box: check the box and the mask')
lit = fur & (v >= np.quantile(v[fur], 0.75))
H, S, HL = np.median(h[fur]), np.median(s[fur]), np.median(h[lit])
print('fur H %.1f  S %.2f  lit-side H %.1f  (%d fur pixels)' % (H, S, HL, fur.sum()))
band = {'day': (28, 33, H), 'cin': (26.5, 30.5, H), 'eve': (19, 28, HL)}
st = opts.get('--style')
if st and st not in band: sys.exit('--style must be day, cin or eve')
if st:
    lo, hi, val = band[st]
    print('%s band %.1f–%.1f: %s' % (st, lo, hi, 'INSIDE' if lo <= val <= hi else 'OUTSIDE (fix with recolor_max.py, then judge by eye next to BO-6)'))
chk = HL if st == 'eve' else H   # Evening is judged on the lit side
if chk < 19: print('WARNING: below 19 degrees%s reads red-brown: reject or fix' % (' on the lit side' if st == 'eve' else ''))
