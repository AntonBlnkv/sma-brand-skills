"""Make Max smaller (or move him to a person's ground line) WITHOUT a model: cut him out of the frame WITH him (B)
using the frame WITHOUT him (A, the same framing), scale him, and paste him back onto A.

Usage:  python3 scripts/resize_max.py A.png B.png OUT.png --scale S | --height P [--feet X,Y] [--green G.png] [--person P.png --side right] [--at X,Y] [--mask-out MASK.png]
- A.png      the same frame without Max: prompt 5.1 ("remove the golden dog") run on B
- B.png      the frame with Max; A must keep its framing (no zoom, no crop)
- --scale S  size factor, e.g. 0.75 (lying poses); for sitting and standing use --height
- --height P  his final height in pixels (crown to paws), instead of --scale. Sitting: 0.55 x the height of the
             standing adult whose ground line he is on (approved SC-1 frame: 0.55-0.57)
- --feet X,Y where the bottom-centre of Max (his paws / contact shadow) should land, in pixels; default = where it is now.
             Use the y of the nearest person's shoes to put him on their ground line.
- --green G.png  the model's "replace the dog with a flat green silhouette" edit of B (exact outline; use it
             whenever the check image shows background patches, halos or a clipped nose)
- --person P.png  the model's "replace {person} with a flat magenta silhouette" edit of A: sets --height and --feet
             from that adult (crown, shoe line), so nothing is read by eye. With --side left|right|keep (which side of
             the adult he sits on; keep = where the model put him), --person-pose stand|seated|crouch, --max-pose sit|stand
- --at X,Y   a point on Max (if the script picks the wrong golden thing, e.g. a dog-coloured bag)
- --mask-out save the mask used (white = Max + his shadow); always check it on the printed overlay
Writes OUT.png and OUT_check.jpg (the mask in red over B). Prints Max's box before and after.
Why: text prompts keep setting Max in front of the people, so he reads too big (control set, 26 Oct: 6 of 10 frames).
Scaling the pixels keeps his face, fur and light exactly; only size and position change.
"""
import sys
if len(sys.argv) < 4 or sys.argv[1] in ('-h', '--help'): print(__doc__); sys.exit(0 if len(sys.argv) > 1 else 1)
import numpy as np
from collections import deque
from PIL import Image, ImageFilter

args = []; opts = {}; argv = sys.argv[1:]; i = 0
while i < len(argv):
    if argv[i].startswith('--'):
        if i + 1 >= len(argv): sys.exit('option %s needs a value' % argv[i])
        opts[argv[i]] = argv[i + 1]; i += 2
    else: args.append(argv[i]); i += 1
A = Image.open(args[0]).convert('RGB'); B = Image.open(args[1]).convert('RGB')
if B.size != A.size: B = B.resize(A.size, Image.LANCZOS)
out = args[2]; scale = float(opts.get('--scale', 1.0))  # or --height, see step 2
a = np.asarray(A).astype(np.float32); b = np.asarray(B).astype(np.float32)
W, H = A.size

# 1. find Max: golden-fur pixels that are new in B (the edit also redraws bushes, cars, people a little,
#    so "largest difference" alone can pick the wrong thing). --at X,Y picks the piece under that point instead.
s = 4
def small(x): return np.asarray(Image.fromarray(x.astype(np.uint8) * 255).resize((W // s, H // s))).astype(np.float32) / 255 > 0.3
def pieces(M):
    h, w = M.shape; lab = np.zeros((h, w), np.int32); sizes = [0]; n = 0
    for y in range(h):
        for x in range(w):
            if M[y, x] and not lab[y, x]:
                n += 1; c = 0; q = deque([(y, x)]); lab[y, x] = n
                while q:
                    yy, xx = q.popleft(); c += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        Y, X = yy + dy, xx + dx
                        if 0 <= Y < h and 0 <= X < w and M[Y, X] and not lab[Y, X]: lab[Y, X] = n; q.append((Y, X))
                sizes.append(c)
    return lab, sizes
d = np.abs(a - b).mean(-1)
hsv = np.asarray(B.convert('HSV')).astype(np.float32)
gold = (hsv[..., 0] >= 12) & (hsv[..., 0] <= 38) & (hsv[..., 1] > 60) & (hsv[..., 2] > 70)   # PIL hue 0-255: ~17-54 degrees
seedM = np.asarray(Image.fromarray(small(gold & (d > 18)).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))) > 127
lab, sizes = pieces(seedM)
if len(sizes) == 1: sys.exit('no new golden-fur area in B: is Max really only in B?')
if '--at' in opts:
    ax, ay = [int(v) // s for v in opts['--at'].split(',')]
    ys_, xs_ = np.where(lab > 0); k = int(np.argmin((xs_ - ax) ** 2 + (ys_ - ay) ** 2)); seed = lab == lab[ys_[k], xs_[k]]
else: seed = lab == int(np.argmax(sizes))
h, w = seed.shape
# the navy collar cuts the fur in two (head / body): add every other golden piece that sits next to this one
for _ in range(2):
    sy, sx = np.where(seed); bx0, bx1, by0, by1 = sx.min(), sx.max(), sy.min(), sy.max()
    gx, gy = int(0.25 * (bx1 - bx0)) + 3, int(0.4 * (by1 - by0)) + 3
    near = np.zeros_like(seed); near[max(0, by0 - gy):by1 + 3, max(0, bx0 - gx):bx1 + gx + 1] = True
    big_n = sizes[int(lab[seed].max())]
    keep = [k for k in np.unique(lab[near & (lab > 0)]) if sizes[k] >= 0.02 * big_n]
    seed = np.isin(lab, keep) | seed
sy, sx = np.where(seed); bx0, bx1, by0, by1 = sx.min(), sx.max(), sy.min(), sy.max()
# around the fur, add only what belongs to Max: dark pixels (collar, eyes, nose, inner ears) and pink ones (tongue)
# that are new in B and touch the fur. Background between his legs or behind him is never taken.
darkish = (hsv[..., 2] < 95) | ((hsv[..., 0] < 12) | (hsv[..., 0] > 235)) & (hsv[..., 1] > 50)
def grow(x, k): return np.asarray(Image.fromarray(x.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(k))) > 127
def shrink(x, k): return np.asarray(Image.fromarray(x.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(k))) > 127
# whole dark/pink blobs that touch the fur (the nose sticks out past it; eyes, collar), but not his old contact
# shadow: a wide blob lying along the ground line under his paws, and not big dark things like a navy jacket
px_, py_ = int(0.15 * (bx1 - bx0)) + 2, int(0.15 * (by1 - by0)) + 2
roi = np.zeros_like(seed); roi[max(0, by0 - py_):by1 + 1, max(0, bx0 - px_):bx1 + px_ + 1] = True
dk = small(darkish & (d > 18)) & roi
dlab, dsz = pieces(dk)
touch = np.unique(dlab[grow(seed, 3) & (dlab > 0)])
keep_d = []
for k in touch:
    yy, xx = np.where(dlab == k)
    if dsz[k] > 0.15 * seed.sum(): continue
    if yy.max() >= by1 - 0.03 * (by1 - by0) and (xx.max() - xx.min()) > 0.3 * (bx1 - bx0): continue
    keep_d.append(k)
M = seed | np.isin(dlab, keep_d)
M = shrink(grow(M, 5), 5) | seed                       # closes the collar line between head and body
lab, sizes = pieces(M)
cl = np.isin(lab, np.unique(lab[seed & (lab > 0)]))
# fill only tiny holes (a pupil, the tag); bigger ones are background seen between his legs or under his chin
inv, isz = pieces(~cl)
area = cl.sum(); edge = set(inv[0]) | set(inv[-1]) | set(inv[:, 0]) | set(inv[:, -1])
bg = np.isin(inv, [k for k in range(1, len(isz)) if k in edge or isz[k] > 0.003 * area])
mask = Image.fromarray(((~bg) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.5))
if '--green' in opts:
    # exact outline from the model's "replace the dog with a flat green silhouette" edit of B (best: nose, collar,
    # gaps between the legs). Only the green piece that overlaps the fur found above is kept.
    E = np.asarray(Image.open(opts['--green']).convert('RGB').resize((W, H))).astype(np.int32)
    g = (E[..., 1] - np.maximum(E[..., 0], E[..., 2])) > 60
    g = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
    gl, gsz = pieces(np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((W // s, H // s))) > 127)
    near_fur = np.unique(gl[grow(seed, 5) & (gl > 0)])
    if len(near_fur) == 0: sys.exit('the green edit has no green shape where Max is: check GREEN.png (framing moved?)')
    gs = np.isin(gl, near_fur)
    # the green edit often leaves the collar (and sometimes the eyes) unpainted: add the dark parts found above,
    # but only right next to the green shape, then close tiny holes
    navy = small((b[..., 2] > b[..., 0] + 15) & (hsv[..., 2] < 140) | (hsv[..., 2] < 70))   # collar, nose, eyes
    # add a dark piece only if it BRIDGES two green pieces (the collar between head and body); a dark piece that
    # touches the dog on one side only is someone's jacket or a shadow, and stays out
    cand = (~bg | navy) & grow(gs, 9) & shrink(grow(gs, 21), 21) & ~gs
    cand = shrink(grow(cand, 3), 3) & ~gs                       # one collar piece, not a row of dots
    glab, _ = pieces(gs); clab, csz = pieces(cand); add = []
    for k in range(1, len(csz)):
        touch_g = np.unique(glab[grow(clab == k, 3) & (glab > 0)])
        if len(touch_g) >= 2 and csz[k] < 0.08 * gs.sum(): add.append(k)
    cs = gs | np.isin(clab, add)
    inv2, isz2 = pieces(~cs); edge2 = set(inv2[0]) | set(inv2[-1]) | set(inv2[:, 0]) | set(inv2[:, -1])
    cs = cs | np.isin(inv2, [k for k in range(1, len(isz2)) if k not in edge2 and isz2[k] < 0.01 * cs.sum()])
    extra = np.asarray(Image.fromarray(((cs & ~gs) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)) > 127
    gsoft = (E[..., 1] - np.maximum(E[..., 0], E[..., 2])) > 30                    # half-green edge pixels count
    keepf = np.asarray(Image.fromarray((gs * 255).astype(np.uint8)).resize((W, H))) > 127
    keepf = np.asarray(Image.fromarray((keepf * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 127
    full = (gsoft & keepf) | extra                    # smooth outline from the edit; collar from the bridge pieces
    navyf = (b[..., 2] > b[..., 0] + 15) & (np.asarray(B.convert('HSV'))[..., 2] < 140)
    near_collar = np.asarray(Image.fromarray((extra * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15))) > 127
    full = full | (navyf & near_collar & keepf)        # collar edge pixels the edit left half-painted (collar only)
    mask = Image.fromarray((full * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
m = np.asarray(mask).astype(np.float32) / 255
ys, xs = np.where(m > 0.5)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
if (x1 - x0) * (y1 - y0) > 0.6 * W * H: sys.exit('the difference covers most of the frame: B was reframed or relit, so A and B do not line up')

# 1b. --person: read the adult's crown and shoe line from the model's "replace {person} with a flat magenta
#     silhouette" edit of A, and set --height / --feet from it (eye-reading a ruler was off by 60-90 px, 26 Oct)
if '--person' in opts:
    P = np.asarray(Image.open(opts['--person']).convert('RGB').resize((W, H))).astype(np.int32)
    pm = (P[..., 0] > 170) & (P[..., 2] > 170) & (P[..., 1] < 110)
    pm = np.asarray(Image.fromarray((pm * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))) > 127
    if pm.sum() < 500: sys.exit('no magenta person in ' + opts['--person'])
    pys, pxs = np.where(pm); ptop, pbot = int(np.percentile(pys, 0.2)), int(np.percentile(pys, 99.8))
    rows = pm[max(ptop, pbot - int(0.06 * (pbot - ptop))):pbot + 1].any(0); fxs = np.where(rows)[0]
    pl, pr = int(fxs.min()), int(fxs.max())                      # where the shoes are, left and right
    ppose, mpose = opts.get('--person-pose', 'stand'), opts.get('--max-pose', 'sit')
    ph = pbot - ptop
    if ppose == 'stand': target = (0.55 if mpose == 'sit' else 0.47) * ph
    else: target = None                                            # seated / crouching: crown below the shoulders
    print('person crown %d  shoes %d  height %d  shoes x %d-%d  (%s)' % (ptop, pbot, ph, pl, pr, ppose))
    if target: opts['--height'] = str(int(target))
    elif '--height' not in opts and '--scale' not in opts:
        shoulder = ptop + 0.22 * ph
        opts['--height'] = str(int(pbot - (shoulder + 0.06 * ph)))
    mw = (x1 - x0) * float(opts['--height']) / (y1 - y0)
    gap = 0.08 * mw
    fx_ = pr + gap + mw / 2 if opts.get('--side', 'right') == 'right' else pl - gap - mw / 2
    if opts.get('--side') == 'keep': fx_ = (x0 + x1) / 2          # stay where the model put him sideways (e.g. beyond a high chair)
    opts['--feet'] = '%d,%d' % (fx_, pbot)
    print('-> --height %s --feet %s' % (opts['--height'], opts['--feet']))

# 2. cut out, scale about the bottom-centre, put a soft contact shadow under the paws, paste on A
# edge decontamination: along his outline, take the colour from his own fur just inside, not from B's old
# background (a dark doorway behind his tail left a dark fringe on a white step)
inner = np.asarray(Image.fromarray(((m > 0.5) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))).astype(np.float32) / 255
num = np.dstack([np.asarray(Image.fromarray((b[..., c] * inner).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) for c in range(3)])
den = np.asarray(Image.fromarray((inner * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32)[..., None] / 255
fill = num / np.maximum(den, 1e-3)
# only edge pixels clearly DARKER than the fur right inside them are old background; fur strands and the nose stay
dark_edge = b.mean(-1, keepdims=True) < 0.85 * fill.mean(-1, keepdims=True)
band = ((m > 0.02) & (inner < 0.5))[..., None] & (den > 0.05) & dark_edge
bc = np.where(band, fill, b)
# un-mix the outline against the known background: B = alpha*fur + (1-alpha)*A at the same spot (A is B without him)
edge = (m > 0.02) & (inner < 0.5)
fa = fill - a; den2 = (fa ** 2).sum(-1)
alpha_e = np.clip(((b - a) * fa).sum(-1) / np.maximum(den2, 1), 0, 1)
usable = edge & (den2 > 45 ** 2) & (den[..., 0] > 0.05)                 # fur and background clearly differ here
m = np.where(usable, np.minimum(m, alpha_e * 1.15), m)
bc = np.where(usable[..., None], np.where((alpha_e > 0.85)[..., None], b, fill), bc)
cut = Image.fromarray(np.dstack([bc.clip(0, 255), m * 255]).astype(np.uint8)).crop((x0, y0, x1 + 1, y1 + 1))
if '--height' in opts: scale = float(opts['--height']) / cut.height
nw, nh = max(1, round(cut.width * scale)), max(1, round(cut.height * scale))
cut = cut.resize((nw, nh), Image.LANCZOS)
fx, fy = ((x0 + x1) // 2, y1) if '--feet' not in opts else [int(v) for v in opts['--feet'].split(',')]
px, py = int(fx - nw / 2), int(fy - nh)
if '--person' in opts and opts.get('--side') != 'keep':
    # slide him sideways, away from the adult, until he no longer covers them (he is drawn in front of everything)
    ca = np.asarray(cut)[..., 3] > 128; step = 1 if opts.get('--side', 'right') == 'right' else -1
    for _ in range(80):
        X0, Y0 = max(0, px), max(0, py); X1, Y1 = min(W, px + nw), min(H, py + nh)
        if X1 <= X0 or Y1 <= Y0: break
        ov = (pm[Y0:Y1, X0:X1] & ca[Y0 - py:Y1 - py, X0 - px:X1 - px]).sum()
        if ov <= 0.003 * ca.sum(): break
        px += step * max(4, nw // 50); fx += step * max(4, nw // 50)
    print('placed %d px from the adult (overlap %.1f%%)' % (abs(fx - (pr if step > 0 else pl)), 100.0 * ov / max(1, ca.sum())))
res = A.copy().convert('RGBA')
sh = Image.new('L', (W, H), 0); sw, shh = int(nw * 0.42), max(4, int(nw * 0.06))
from PIL import ImageDraw
ImageDraw.Draw(sh).ellipse((fx - sw, fy - shh, fx + sw, fy + shh), fill=255)
sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(max(4, nw * 0.07)))).astype(np.float32) / 255
ra = np.asarray(res).astype(np.float32); ra[..., :3] *= (1 - 0.42 * sh[..., None])
# contact darkening right under every paw that touches the ground (the soft ellipse alone left a trotting paw floating)
al = np.zeros((H, W), np.float32); ca_ = np.asarray(cut)[..., 3].astype(np.float32) / 255
X0, Y0 = max(0, px), max(0, py); X1, Y1 = min(W, px + nw), min(H, py + nh)
if X1 > X0 and Y1 > Y0: al[Y0:Y1, X0:X1] = ca_[Y0 - py:Y1 - py, X0 - px:X1 - px]
rows_ = np.where((al > 0.5).any(1))[0]; fy = int(rows_.max()) if len(rows_) else fy   # his real paw line
yy_ = np.arange(H, dtype=np.float32)[:, None]
low = np.clip(1 - (fy - yy_) / (0.12 * nh), 0, 1) * (yy_ <= fy + 2)             # strongest at the paws, fading up
dn = max(3, int(0.006 * nh)); sh2 = np.zeros_like(al); sh2[dn:] = (al * low)[:-dn]
sh2 = np.asarray(Image.fromarray((sh2 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(3, 2 * dn)))).astype(np.float32) / 255
ra[..., :3] *= (1 - 0.6 * np.clip(sh2 - al, 0, 1)[..., None])
# cast shadow: his silhouette laid on the ground, leaning the way the people's shadows fall (read from the
# ground next to the adult's shoes when --person is given; otherwise straight back), then softened
lean = 0.0
if '--person' in opts:
    lum = np.asarray(A.convert('L')).astype(np.float32); sw_ = max(20, (pr - pl) // 2)
    band = lum[max(0, pbot - 25):min(H, pbot + 15)]
    left_d, right_d = band[:, max(0, pl - sw_):pl].mean(), band[:, pr:min(W, pr + sw_)].mean()
    far = np.r_[band[:, max(0, pl - 4 * sw_):max(1, pl - 3 * sw_)].ravel(), band[:, min(W - 1, pr + 3 * sw_):min(W, pr + 4 * sw_)].ravel()].mean()
    if abs(left_d - right_d) > 0.08 * far: lean = -0.9 if left_d < right_d else 0.9
    print('people\'s shadows fall to the %s' % ({-0.9: 'left', 0.9: 'right'}.get(lean, 'back (not found)')))
cs_h = max(4, int(0.36 * nh)); cast = np.zeros((H, W), np.float32)
sil = np.asarray(cut.split()[3].resize((nw, cs_h)).transpose(Image.FLIP_TOP_BOTTOM)).astype(np.float32) / 255
for r in range(cs_h):                                          # shear: farther from the paws = farther along the lean
    yy = int(fy - 0.02 * nh + r * 0.45); dx = int(lean * r * 2.2) + px
    if not (0 <= yy < H): continue
    xa, xb = max(0, dx), min(W, dx + nw)
    if xb > xa: cast[yy, xa:xb] = np.maximum(cast[yy, xa:xb], sil[r, xa - dx:xb - dx] * (1 - 0.5 * r / cs_h))
cast = np.asarray(Image.fromarray((cast * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(2, nw * 0.008)))).astype(np.float32) / 255
ra[..., :3] *= (1 - (0.6 if lean else 0.4) * np.clip(cast - al, 0, 1)[..., None])
# his OWN shadow from B: where the ground next to him is darker in B than in the clean plate A (same place),
# carried along with him. It has the scene's real light direction and softness; the synthetic one is only a fallback.
la, lb = np.asarray(A.convert('L')).astype(np.float32), np.asarray(B.convert('L')).astype(np.float32)
bw, bh = x1 - x0, y1 - y0
rx0, rx1 = max(0, int(x0 - 0.6 * bw)), min(W, int(x1 + 0.6 * bw)); ry0, ry1 = max(0, int(y1 - 0.45 * bh)), min(H, int(y1 + 0.25 * bh))
dk_ = 1 - np.clip((lb[ry0:ry1, rx0:rx1] + 6) / (la[ry0:ry1, rx0:rx1] + 6), 0.25, 1)
inm = m[ry0:ry1, rx0:rx1] > 0.05
dk_[inm] = 0
dk_ = np.where(dk_ < 0.08, 0, dk_)
# under his own outline the shadow is unknown: fill it from the shadow just around him, so no lit rim is left
dil = np.asarray(Image.fromarray((dk_ * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15))).astype(np.float32) / 255
dk_ = np.where(inm, dil, dk_)
dimg = Image.fromarray((dk_ * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(2))
own = dk_.sum() > 0.02 * bw * bh * 255 / 255
if own:
    sw2, sh2_ = max(1, round((rx1 - rx0) * scale)), max(1, round((ry1 - ry0) * scale))
    dimg = np.asarray(dimg.resize((sw2, sh2_), Image.BILINEAR)).astype(np.float32) / 255
    ox, oy = px + int((rx0 - x0) * scale), py + int((ry0 - y0) * scale)
    canvas = np.zeros((H, W), np.float32)
    X0, Y0, X1, Y1 = max(0, ox), max(0, oy), min(W, ox + sw2), min(H, oy + sh2_)
    if X1 > X0 and Y1 > Y0: canvas[Y0:Y1, X0:X1] = dimg[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
    yyc = np.arange(H, dtype=np.float32)[:, None]                              # ground near the paws only, faded in
    canvas *= np.clip((yyc - (fy - 0.16 * nh)) / (0.06 * nh), 0, 1)
    if '--person' in opts:                                                      # never on a person; soft edge
        canvas *= 1 - np.asarray(Image.fromarray((pm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    canvas = np.asarray(Image.fromarray((np.clip(canvas, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255
    ra = np.asarray(A.convert('RGBA')).astype(np.float32)          # restart from A: his own shadow replaces the synthetic ones
    ra[..., :3] *= (1 - canvas[..., None])
    ra[..., :3] *= (1 - 0.4 * np.clip(sh2 - al, 0, 1)[..., None])    # plus a soft contact line right under the paws
    under = canvas[max(0, fy - 5):min(H, fy + int(0.04 * nh)), max(0, px):min(W, px + nw)]
    if under.size and under.mean() < 0.05:                          # moved to a new surface: his old shadow did not come along
        near = np.clip(1 - (yyc - fy) / (0.05 * nh), 0, 1) * (yyc >= fy - 0.05 * nh)   # short: only around the paws
        ra[..., :3] *= (1 - 0.45 * np.clip(cast * near - al, 0, 1)[..., None])
        print('shadow: his own was too weak under the paws here, the synthetic cast shadow was added')
    print('shadow: his own, carried over from B')
else: print('shadow: synthetic (no shadow found next to him in B)')
res = Image.fromarray(ra.clip(0, 255).astype(np.uint8))
res.alpha_composite(cut, (max(0, px), max(0, py)), (max(0, -px), max(0, -py)))
res.convert('RGB').save(out)
if opts.get('--mask-out'): mask.save(opts['--mask-out'])
ov = b * (1 - 0.5 * m[..., None]) + np.array([255, 0, 0], np.float32) * 0.5 * m[..., None]
chk = out.rsplit('.', 1)[0] + '_check.jpg'; Image.fromarray(ov.astype(np.uint8)).save(chk, quality=85)
print('Max box before %d,%d,%d,%d  after %d,%d,%d,%d  scale %.2f  | check the mask: %s' % (x0, y0, x1, y1, px, py, px + nw, py + nh, scale, chk))
print('Check: the new box must not cover a person (he is drawn in front of everything); move --feet sideways if it does.')
