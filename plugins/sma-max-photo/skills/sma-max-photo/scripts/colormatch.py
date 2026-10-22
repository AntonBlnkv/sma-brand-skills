"""Undo the colour drift a model adds when it re-renders a whole frame (NOT a grade).

Usage:  python3 scripts/colormatch.py APPROVED_FRAME RESULT OUT.jpg
Fits a robust per-channel curve RESULT -> APPROVED_FRAME on all pixels that did not change
(the new Max is ignored as an outlier) and applies it to RESULT, so the frame keeps the approved colours.
Use only when an edit/re-add came back with a colour cast (e.g. pink/magenta whites) versus the approved frame.
Prints mean error before/after; after should be ~3 or less.
"""
import sys as _s
if len(_s.argv) < 4 or _s.argv[1] in ('-h', '--help'): print(__doc__); _s.exit(0 if len(_s.argv) > 1 else 1)
import sys,warnings,numpy as np
warnings.simplefilter("ignore")
from PIL import Image
P=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
Rimg=Image.open(sys.argv[2]).convert('RGB').resize((P.shape[1],P.shape[0]),Image.LANCZOS); R=np.asarray(Rimg).astype(np.float32)
s=6; p=P[::s,::s].reshape(-1,3); r=R[::s,::s].reshape(-1,3); keep=np.ones(len(p),bool)
for it in range(4):
    C=[np.polyfit(r[keep,c],p[keep,c],3) for c in range(3)]
    pred=np.stack([np.polyval(C[c],r[:,c]) for c in range(3)],1); err=np.abs(pred-p).mean(1); keep=err<np.percentile(err,70)
lut=[np.clip(np.polyval(C[c],np.arange(256)),0,255) for c in range(3)]
Rfull=np.asarray(Image.open(sys.argv[2]).convert('RGB'))  # apply to the result at its own full resolution
O=np.stack([lut[c][Rfull[...,c]] for c in range(3)],-1)
Image.fromarray(O.astype(np.uint8)).save(sys.argv[3],quality=95)
q=np.stack([lut[c][R[...,c].astype(np.uint8)] for c in range(3)],-1)[::s,::s].reshape(-1,3)
print(sys.argv[2],'mean before',np.abs(r-p)[keep].mean().round(2),'after',np.abs(q-p)[keep].mean().round(2),'means',q.mean(0).round(1),p.mean(0).round(1))
