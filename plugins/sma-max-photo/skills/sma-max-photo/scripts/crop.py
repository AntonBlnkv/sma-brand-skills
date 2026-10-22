"""Cut a box out of a full-resolution frame (step 1 of crop -> edit -> paste).

Usage:  python3 scripts/crop.py FULL.png x0,y0,x1,y1 CROP.png [--ratio 3:2]
- x0,y0,x1,y1  the box in FULL.png pixels: Max's whole head AND the collar with the tag, with margin
- --ratio W:H  grow the box (never shrink it) to this aspect, centred, kept inside the frame (default 3:2;
               use --ratio none to keep the box exactly)
Prints the final box: pass exactly that box to paste_crop.py, recolor_max.py and max_mask.py.
"""
import sys as _s
if len(_s.argv) < 4 or _s.argv[1] in ('-h', '--help'): print(__doc__); _s.exit(0 if len(_s.argv) > 1 else 1)
import sys
from PIL import Image
args = [a for a in sys.argv[1:]]
ratio = '3:2'
if '--ratio' in args:
    i = args.index('--ratio'); ratio = args[i + 1]; del args[i:i + 2]
full, box, out = args[:3]
im = Image.open(full); W, H = im.size
x0, y0, x1, y1 = map(int, box.split(','))
if ratio != 'none':
    rw, rh = map(float, ratio.split(':'))
    w, h = x1 - x0, y1 - y0
    if w / h < rw / rh: w = round(h * rw / rh)
    else: h = round(w * rh / rw)
    if w > W: w, h = W, round(W * rh / rw)   # too wide for the frame: shrink, keeping the ratio
    if h > H: w, h = round(H * rw / rh), H
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0 = int(min(max(cx - w / 2, 0), W - w)); y0 = int(min(max(cy - h / 2, 0), H - h)); x1, y1 = x0 + w, y0 + h
im.crop((x0, y0, x1, y1)).save(out)
print(out, 'box', f'{x0},{y0},{x1},{y1}', 'size', (x1 - x0, y1 - y0))
