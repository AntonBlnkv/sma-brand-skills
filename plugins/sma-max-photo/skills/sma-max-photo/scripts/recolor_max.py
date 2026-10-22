"""Recolour Max's fur in an approved frame WITHOUT redrawing him (no model involved).

Usage:  python3 scripts/recolor_max.py BASE.png MASKREF.png x0,y0,x1,y1 STYLE OUT.png [--hue H] [--smin S] [--smax S]
- BASE.png     the approved frame (full resolution). Its pixels are kept: face, eyes, fur markings, pose,
               light and shadows stay exactly as they are. Only the hue and saturation of Max's fur move.
- MASKREF.png  `x` when --mask is given. Otherwise any version of the same frame in which Max's fur colour differs (e.g. a model's colour edit,
               pasted with paste_crop.py). Used ONLY to find where Max is: |BASE - MASKREF| inside the box.
- x0,y0,x1,y1  a box around Max (the crop box used for the edit).
- STYLE        day | cin | eve. Master BO-6 fur: median H 31, S 0.58. The fur's median hue is moved to the
               target and the spread of hue around it is narrowed to 60% (red shadows are what reads orange);
               saturation is only capped (or lifted when Max came out grey):
               day -> H 29.5, S 0.45-0.58 · cin -> H 27.5, S 0.48-0.60 · eve -> H 22.5, S 0.46-0.55
               --mask MASK.png (from max_mask.py, the crop's size) is the reliable way to say where Max is.
               --hue / --smax / --smin override. --maskpair A,B finds Max from |A-B| instead of |BASE-MASKREF|.
Why: a model colour edit on a crop redraws the dog (21 Oct: cream bibs, white muzzles, a realistic head).
A hue/saturation shift on the fur pixels cannot change his design.
Prints the fur hue and saturation before and after.
"""
import sys as _s
if len(_s.argv) < 6 or _s.argv[1] in ('-h', '--help'): print(__doc__); _s.exit(0 if len(_s.argv) > 1 else 1)
import sys, numpy as np
from PIL import Image, ImageFilter

def rgb2hsv(a):
    mx=a.max(-1); mn=a.min(-1); d=mx-mn
    r,g,b=a[...,0],a[...,1],a[...,2]; dd=np.where(d==0,1,d)
    h=np.where(mx==r,((g-b)/dd)%6,np.where(mx==g,(b-r)/dd+2,(r-g)/dd+4))/6.0
    h=np.where(d==0,0,h); s=np.where(mx==0,0,d/np.where(mx==0,1,mx)); return h,s,mx

def hsv2rgb(h,s,v):
    i=np.floor(h*6)%6; f=h*6-np.floor(h*6); p=v*(1-s); q=v*(1-f*s); t=v*(1-(1-f)*s)
    out=np.zeros(h.shape+(3,),np.float32)
    for k,(R,G,B) in enumerate([(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]):
        m=i==k; out[...,0][m]=R[m]; out[...,1][m]=G[m]; out[...,2][m]=B[m]
    return out

TARGET={'day':(29.5,0.45,0.58),'cin':(27.5,0.48,0.60),'eve':(22.5,0.46,0.55)}
# options (--mask, --maskpair, --hue, --smin, --smax) each take one value and may go anywhere on the line
args=[]; opts={}; argv=sys.argv[1:]; i=0
while i<len(argv):
    if argv[i].startswith('--'):
        if i+1>=len(argv): _s.exit('option %s needs a value'%argv[i])
        opts[argv[i]]=argv[i+1]; i+=2
    else: args.append(argv[i]); i+=1
base,maskref,box,style,out=args[:5]
th,smin,smax=TARGET[style]; th=float(opts.get('--hue',th)); smin=float(opts.get('--smin',smin)); smax=float(opts.get('--smax',smax))
x0,y0,x1,y1=map(int,box.split(','))
B=Image.open(base).convert('RGB')
# --maskpair A,B: find Max from two other versions of the same composition (e.g. a relight of a frame whose mask you know)
b=np.asarray(B.crop((x0,y0,x1,y1))).astype(np.float32)/255
if opts.get('--mask'):
    # preferred: Max's whole silhouette from max_mask.py (crop-size)
    area=np.asarray(Image.open(opts['--mask']).convert('L').resize((x1-x0,y1-y0))).astype(np.float32)/255
else:
    # fallback: pixels a colour edit changed (can be patchy: 21 Oct T3)
    mp=opts.get('--maskpair'); A0=Image.open(mp.split(',')[0]).convert('RGB').resize(B.size) if mp else B
    M=Image.open(mp.split(',')[1] if mp else maskref).convert('RGB').resize(B.size)
    a0=np.asarray(A0.crop((x0,y0,x1,y1))).astype(np.float32)/255; m=np.asarray(M.crop((x0,y0,x1,y1))).astype(np.float32)/255
    diff=(np.abs(a0-m).mean(-1)*255>10).astype(np.uint8)*255
    mk=Image.fromarray(diff).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.MinFilter(25))
    mk=mk.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(12))
    area=np.asarray(mk).astype(np.float32)/255
h,s,v=rgb2hsv(b); H=h*360
fur=np.clip((s-0.12)/0.08,0,1)*np.clip((H-5)/5,0,1)*np.clip((60-H)/5,0,1)*np.clip((v-0.12)/0.08,0,1)
w=area*fur
sel=w>0.5; q=np.quantile(v[sel],0.75); lit=sel&(v>=q)
h0=np.median(H[sel]); s0=np.median(s[sel])
Hn=th+(H-h0)*0.6                      # move the median to the target, narrow the spread
k=min(1.0,smax/s0) if s0>smin else smin/s0
h2=((H+(Hn-H)*w)/360)%1; s2=np.clip(s*(1+(k-1)*w),0,1)
o=hsv2rgb(h2,s2,v)
O=np.asarray(B).astype(np.float32).copy(); O[y0:y1,x0:x1]=o*255
Image.fromarray(np.clip(O,0,255).astype(np.uint8)).save(out)
hh,ss,vv=rgb2hsv(o)
print(out,'fur H %.1f S %.2f -> H %.1f S %.2f (lit %.1f -> %.1f), target H %.1f, Max area %.0f%% of box'%(h0,s0,np.median(hh[sel]*360),np.median(ss[sel]),np.median(H[lit]),np.median(hh[lit]*360),th,100*(area>0.5).mean()))
