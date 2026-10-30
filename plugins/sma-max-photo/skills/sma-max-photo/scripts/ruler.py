"""Draw a pixel ruler over a frame so you can read where the people and Max stand (QA check 4, resize_max.py).

Usage:  python3 scripts/ruler.py FRAME.png OUT.jpg [x0,y0,x1,y1]
- red lines every 100 px (labelled, yellow), pink every 25 px, blue columns every 100 px (labelled); numbers are
  FULL-FRAME pixels, also inside a crop box
- give a box around the adult and Max to read crowns and shoes to ~10 px; without a box the whole frame is drawn
Read: the adult's crown and shoe line, Max's crown and paw line, and x of where his paws should stand.
Then: sitting height target P = 0.55 x (adult shoes y - adult crown y); --feet X,(adult shoes y).
"""
import sys
if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'): print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 1)
from PIL import Image, ImageDraw, ImageFont
im = Image.open(sys.argv[1]).convert('RGB')
box = [int(v) for v in sys.argv[3].split(',')] if len(sys.argv) > 3 else [0, 0, im.width, im.height]
im = im.crop(box); d = ImageDraw.Draw(im)
fs = max(14, im.width // 45)
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', fs)
except OSError:
    try: f = ImageFont.truetype('DejaVuSans.ttf', fs)
    except OSError: f = ImageFont.load_default()
for y in range((box[1] // 25 + 1) * 25, box[3], 25):
    yy = y - box[1]; major = y % 100 == 0
    d.line([(0, yy), (im.width, yy)], fill=(255, 0, 0) if major else (255, 170, 170), width=2 if major else 1)
    if y % (50 if box != [0, 0, *Image.open(sys.argv[1]).size] else 100) == 0:
        d.text((4, yy + 1), str(y), fill=(255, 255, 0), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
step = 100 if box[2] - box[0] <= 1500 else 200
for x in range((box[0] // step + 1) * step, box[2], step):
    d.line([(x - box[0], 0), (x - box[0], im.height)], fill=(0, 200, 255), width=1)
    d.text((x - box[0] + 3, 3), str(x), fill=(0, 255, 255), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
im.thumbnail((1400, 1400)); im.save(sys.argv[2], quality=88)
print('ruler written:', sys.argv[2], '| box', ','.join(map(str, box)))
