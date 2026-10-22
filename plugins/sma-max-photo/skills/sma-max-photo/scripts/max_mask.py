"""Build a mask of Max's whole silhouette from a crop WITH him and the same crop with him REMOVED.

Usage:  python3 scripts/max_mask.py WITH.png WITHOUT.png MASK.png [EXTRA.png]
- WITH.png     the crop around Max from the approved frame (the box you will pass to recolor_max.py)
- WITHOUT.png  the model's "remove the dog" edit of that crop (prompt 5.1); any size, resized to WITH.
               Check it: if the dog is still there, run the removal again.
- MASK.png     white = Max, black = the rest; small stray pieces are dropped (pieces under 4% of the
               largest), so people the removal touched by accident usually drop out, holes filled, edge feathered a few pixels
- EXTRA.png    optional: either a white-on-black mask of the same crop, or the model's "replace the dog with a flat
               green shape of the same outline" edit of it (the green is keyed automatically), for parts the
               removal left looking alike (fur next to a wood floor of the same colour)
Also writes MASK_check.jpg: the crop with the mask in red. The red must cover his whole body, ears and tail.
Why: a mask taken from a colour edit only covers the parts the edit changed, so the recolour came out
patchy (21 Oct: red-looking ear and haunch on T3). Removing Max changes almost every pixel of him.
The mask works for the Cinema / Evening relights of the same frame too (same composition).
"""
import sys as _s
if len(_s.argv) < 4 or _s.argv[1] in ('-h', '--help'): print(__doc__); _s.exit(0 if len(_s.argv) > 1 else 1)
import sys, numpy as np
from collections import deque
from PIL import Image, ImageFilter
a=Image.open(sys.argv[1]).convert('RGB'); b=Image.open(sys.argv[2]).convert('RGB').resize(a.size, Image.LANCZOS)
d=np.abs(np.asarray(a).astype(np.float32)-np.asarray(b).astype(np.float32)).mean(-1)
m=Image.fromarray(((d>22)*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))
if len(sys.argv)>4:
    # EXTRA may be a white-on-black mask, or the model's "replace the dog with a flat green shape" edit of the crop
    E=np.asarray(Image.open(sys.argv[4]).convert('RGB').resize(a.size)).astype(np.int32)
    green=(E[...,1]-np.maximum(E[...,0],E[...,2]))>40
    ex=green if green.mean()>0.005 else (E.mean(-1)>127)
    m=Image.fromarray(np.maximum(np.asarray(m),ex*255).astype(np.uint8))
# work at 1/4 size: open (break thin links), keep the largest piece, close, fill holes
W,H=a.size; s=4
sm=m.resize((W//s,H//s)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
M=np.asarray(sm)>127; h,w=M.shape
lab=np.zeros((h,w),np.int32); sizes=[0]; n=0
for y in range(h):
    for x in range(w):
        if M[y,x] and not lab[y,x]:
            n+=1; c=0; q=deque([(y,x)]); lab[y,x]=n
            while q:
                yy,xx=q.popleft(); c+=1
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    Y,X=yy+dy,xx+dx
                    if 0<=Y<h and 0<=X<w and M[Y,X] and not lab[Y,X]: lab[Y,X]=n; q.append((Y,X))
            sizes.append(c)
sz=np.array(sizes); keep=[i for i in range(1,len(sz)) if sz[i]>=0.04*sz.max()]
big=np.isin(lab,keep)   # every piece at least 4% of the largest (a tail behind a chair leg stays)
cl=Image.fromarray((big*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
F=np.asarray(cl)>127
bg=np.zeros_like(F); q=deque()
for x in range(w):
    for y in (0,h-1):
        if not F[y,x]: bg[y,x]=True; q.append((y,x))
for y in range(h):
    for x in (0,w-1):
        if not F[y,x] and not bg[y,x]: bg[y,x]=True; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        Y,X=y+dy,x+dx
        if 0<=Y<h and 0<=X<w and not F[Y,X] and not bg[Y,X]: bg[Y,X]=True; q.append((Y,X))
out=Image.fromarray(((~bg)*255).astype(np.uint8)).resize((W,H),Image.BILINEAR)
# back at full size: keep the fine edge from the full-res difference, inside a slightly grown envelope
env=np.asarray(out.filter(ImageFilter.MaxFilter(9)))>127
fine=np.asarray(m.filter(ImageFilter.MaxFilter(5)))>127
core=np.asarray(out.filter(ImageFilter.MinFilter(9)))>127
fin=(core|(fine&env))
Image.fromarray((fin*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)).save(sys.argv[3])
# red overlay for the visual check: the red must cover his whole body, ears and tail and nothing else
ov=np.asarray(a).astype(np.float32); r=np.asarray(Image.open(sys.argv[3])).astype(np.float32)[...,None]/255
ov=ov*(1-0.5*r)+np.array([255,0,0],np.float32)*0.5*r
chk=sys.argv[3].rsplit('.',1)[0]+'_check.jpg'; Image.fromarray(ov.astype(np.uint8)).save(chk,quality=88)
print(sys.argv[3],'Max = %.0f%% of the crop'%(100*fin.mean()),'| check the red overlay:',chk)
