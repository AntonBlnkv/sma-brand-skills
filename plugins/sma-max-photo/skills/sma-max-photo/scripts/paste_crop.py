"""Paste an edited crop back into the full frame (crop -> edit -> paste method).

Usage:  FULL=1 python3 scripts/paste_crop.py FULL.png x0,y0,x1,y1 EDITED_CROP.png OUT.png
- FULL.png      the full frame the crop was cut from (native resolution)
- x0,y0,x1,y1   the crop box in FULL.png pixels (3:2 box, the same one you uploaded)
- EDITED_CROP   the model's output for that crop (any size; it is resized to the box)
Always run with FULL=1: the whole crop is replaced, with an 80 px fade at the edges.
Never blend two versions of a face (double edges / ghosting).
The script also finds the best +-12 px shift on the border band (the model sometimes nudges the image).
Check the printed 'border diff': below ~15 is a clean fit; above ~30 means the model reframed the crop -> discard that output.
Use exactly the box that crop.py printed.
REGION=x0,y0,x1,y1 (in CROP pixels, origin = top-left of the crop) pastes back only a soft ellipse inside that box,
e.g. only Max's head, when the edit also repainted parts of the background (an object moved or appeared). Use instead of FULL=1. Optional 5th argument MASK_OUT.png saves the blend mask used.
Env T=6 (default) is the change threshold used only without FULL=1.
"""
import sys as _s
if len(_s.argv) < 5 or _s.argv[1] in ('-h', '--help'): print(__doc__); _s.exit(0 if len(_s.argv) > 1 else 1)
import sys,numpy as np
from PIL import Image,ImageFilter
full=Image.open(sys.argv[1]).convert('RGB'); x0,y0,x1,y1=map(int,sys.argv[2].split(','))
orig=full.crop((x0,y0,x1,y1)); W,H=orig.size
ed=Image.open(sys.argv[3]).convert('RGB').resize((W,H),Image.LANCZOS)
o=np.asarray(orig).astype(np.float32); e=np.asarray(ed).astype(np.float32)
# best integer shift on a border band
best=None
band=np.zeros((H,W),bool); b=60; band[:b,:]=band[-b:,:]=True; band[:,:b]=band[:,-b:]=True
for dy in range(-12,13,2):
  for dx in range(-12,13,2):
    es=np.roll(np.roll(e,dy,0),dx,1); d=np.abs(es-o).mean(2)[band].mean()
    if best is None or d<best[0]: best=(d,dx,dy)
_,dx,dy=best; e=np.roll(np.roll(e,dy,0),dx,1)
diff=np.abs(e-o).mean(2)
m=Image.fromarray(np.clip((diff-float(__import__("os").environ.get("T","6")))*12,0,255).astype(np.uint8)).filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(18))
m=np.asarray(m).astype(np.float32)/255
# fade to zero at crop border
yy,xx=np.mgrid[0:H,0:W]; edge=np.minimum.reduce([xx,yy,W-1-xx,H-1-yy]).astype(np.float32)
m=m*np.clip(edge/80,0,1)
if __import__('os').environ.get('FULL'): m=np.clip(edge/80,0,1)
REG=__import__('os').environ.get('REGION')
if REG:   # paste back ONLY an ellipse inside this box (crop pixels): use it when the edit also repainted the background
    rx0,ry0,rx1,ry1=map(float,REG.split(','))
    cx,cy,ax,ay=(rx0+rx1)/2,(ry0+ry1)/2,(rx1-rx0)/2,(ry1-ry0)/2
    ell=((((xx-cx)/ax)**2+((yy-cy)/ay)**2)<=1).astype(np.uint8)*255
    m=np.asarray(Image.fromarray(ell).filter(ImageFilter.GaussianBlur(max(6,min(ax,ay)*0.15)))).astype(np.float32)/255
out=o*(1-m[...,None])+e*m[...,None]
F=np.asarray(full).astype(np.float32).copy(); F[y0:y1,x0:x1]=out
Image.fromarray(np.clip(F,0,255).astype(np.uint8)).save(sys.argv[4])
if len(sys.argv)>5: Image.fromarray((m*255).astype(np.uint8)).save(sys.argv[5])
print('shift',dx,dy,'border diff',round(best[0],2),'mask mean',round(float(m.mean()),3))
